# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/06/16 21:48:50 by charles           #+#    #+#              #
#    Updated: 2021/03/03 12:23:59 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Union, Callable, TypeVar

from minishell_test.config import Config
from minishell_test.test.captured import CapturedCommand, CapturedTimeout, CapturedType
from minishell_test.test.result import Result, LeakResult
from minishell_test import sandbox


HookType       = Union[Callable[[str], str], List[Callable[[str], str]]]
HookStatusType = Union[Callable[[int], int], List[Callable[[int], int]]]

T = TypeVar('T')


class Test:
    __test__ = False  # Tell pytest to ignore this class

    def __init__(
        self,
        cmd:          str,
        setup:        str                   = "",
        files:        Union[str, List[str]] = [],
        exports:      Dict[str, str]        = {},
        timeout:      float                 = -1,
        hooks:        HookType              = [],
        hooks_status: HookStatusType        = [],
    ):
        """
            :param cmd:
                Command to test
            :param setup:
                Command to execute before tested command
            :param files:
                Files to watch, content of each file is check after the test
            :param exports:
                Exported variables to :param:`cmd`
            :param timeout:
                Maximum amount of time taken by the test
            :param hooks:
                Function to execute on the test output
            :param hooks_status:
                Function to execute on the test status code
        """
        self._cmd = cmd
        self._setup = setup
        self._files = Test._coerce_into_list(files)
        self._exports = exports
        if Config.check_leaks:
            self._timeout = Config.timeout_leaks
        elif timeout <= 0:
            self._timeout = Config.timeout_test
        else:
            self._timeout = timeout
        self._hooks = Test._coerce_into_list(hooks)
        self._hooks_status = Test._coerce_into_list(hooks_status)

    @staticmethod
    def _coerce_into_list(x: Union[T, List[T]]) -> List[T]:
        if not isinstance(x, list):
            return [x]
        return x

    def run(self) -> Union[Result, LeakResult]:
        """ Run the test for minishell and the reference shell and print the result out """
        if Config.check_leaks:
            captured = self._run_sandboxed(*Config.valgrind_cmd, "-c")
            return LeakResult(self._extended_cmd, captured)
        expected = self._run_sandboxed(Config.shell_reference_path, *Config.shell_reference_args, "-c")
        actual   = self._run_sandboxed(Config.minishell_exec_path, "-c")
        return Result(self._extended_cmd, self._files, expected, actual)

    def _run_sandboxed(self, *argv: Union[str, Path]) -> CapturedType:
        """ Run the command in a sandbox environment """
        with sandbox.context():
            if self._setup != "":
                try:
                    subprocess.run(
                        self._setup,
                        shell=True,
                        cwd=Config.sandbox_dir,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        check=True
                    )
                except subprocess.CalledProcessError as e:
                    raise TestSetupException(self._setup, self._cmd, e.stdout)
            return self._run_capture(*argv)

    def _run_capture(self, *argv: Union[str, Path]) -> CapturedType:
        """ Capture the output (stdout and stderr)
            Capture the content of the watched files after the command is run
        """
        # run the command in the sandbox
        process = subprocess.Popen(
            [*argv, self._cmd],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=Config.sandbox_dir,
            env={
                'PATH': Config.shell_path_variable,
                'TERM': 'xterm-256color',
                **self._exports,
            },
        )

        # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
        try:
            stdout, _ = process.communicate(timeout=self._timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            return CapturedTimeout()
        try:
            output = stdout.decode()
        except UnicodeDecodeError:
            output = "UNICODE DECODE ERROR: {process.stdout}"

        # capture watched files content
        files_content: List[Optional[str]] = []
        for file_name in self._files:
            try:
                with open(Config.sandbox_dir / file_name, "rb") as f:
                    files_content.append(f.read().decode())
            except FileNotFoundError:
                files_content.append(None)

        output             = Test._apply_hooks(output, self._hooks)
        process.returncode = Test._apply_hooks(process.returncode, self._hooks_status)

        # replace reference prefix with minishell prefix
        lines = output.split('\n')
        for i, line in enumerate(lines):
            lines[i] = line = re.sub("line [01]: ", "", lines[i], 1)
            if line.startswith(Config.shell_reference_prefix):
                lines[i] = Config.minishell_prefix + line[len(Config.shell_reference_prefix):]
        output = '\n'.join(lines)

        return CapturedCommand(output, process.returncode, files_content)

    @staticmethod
    def _apply_hooks(origin: T, hooks: List[Callable[[T], T]]) -> T:
        if Config.check_leaks:
            return origin
        for hook in hooks:
            origin = hook(origin)
        return origin

    @property
    def _extended_cmd(self) -> str:
        """ Return the command prefixed by the setup and exports """
        s = self._cmd
        if len(self._exports) != 0:
            exports = ' '.join(f"{k}='{v}'" for k, v in self._exports.items())
            s = f"[EXPORTS {exports}] {s}"
        if self._setup != "":
            s = f"[SETUP {self._setup}] {s}"
        return s

    @classmethod
    def try_run(cls, cmd: str) -> str:
        test = Test(cmd)
        result = test.run()
        if isinstance(result, LeakResult):
            return str(result)
        elif isinstance(result, Result):
            return str(result)
        else:
            return "No output"


class TestSetupException(Exception):
    __test__ = False

    def __init__(self, setup: str, cmd: str, stdout: Optional[bytes]):
        self._setup = setup
        self._cmd = cmd
        if stdout is None or stdout.decode().strip() == "":
            stdout = b"no output"
        self._setup_output = stdout.decode().strip()

    def __str__(self):
        return f"Error: `{self._setup}` setup command failed for `{self._cmd}`\n\twith '{self._setup_output}'"
