# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/06/16 21:48:50 by charles           #+#    #+#              #
#    Updated: 2021/03/01 16:02:35 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Union, Callable

from minishell_test.config import Config
from minishell_test.test.captured import Captured
from minishell_test.test.result import Result, LeakResult
from minishell_test import sandbox

HookType       = Union[Callable[[str], str], List[Callable[[str], str]]]
HookStatusType = Union[Callable[[int], int], List[Callable[[int], int]]]


class Test:
    def __init__(
        self,
        cmd:         str,
        setup:       str            = "",
        files:       List[str]      = [],
        exports:     Dict[str, str] = {},
        timeout:     float          = -1,
        hook:        HookType       = [],
        hook_status: HookStatusType = [],
    ):
        """ Test class
            cmd:         command to execute
            setup:       command to execute before tested command
            files:       files to watch (check content after test)
            exports:     exported variables
            timeout:     maximum amount of time taken by the test
            hook:        function to execute on the output of the test
            hook_status: function to execute on status code
        """
        self.cmd = cmd
        self.setup = setup
        self.files = files
        self.exports = exports
        self.result: Optional[Union[Result, LeakResult]] = None
        self.timeout = timeout if timeout > 0 else Config.timeout_test
        if not isinstance(hook, list):
            hook = [hook]
        if not isinstance(hook_status, list):
            hook_status = [hook_status]
        self.hook = hook
        self.hook_status = hook_status

    def run(self, index: int) -> None:
        """ Run the test for minishell and the reference shell and print the result out """

        if Config.check_leaks:
            self.hook = []
            self.hook_status = []
            captured = self._run_sandboxed([*Config.valgrind_cmd, "-c"])
            self.result = LeakResult(self.full_cmd, captured)
            self.result.put(index)
            return

        expected = self._run_sandboxed([Config.shell_reference_path, *Config.shell_reference_args, "-c"])
        actual   = self._run_sandboxed([Config.minishell_exec_path, "-c"])
        self.result = Result(self.full_cmd, self.files, expected, actual)
        self.result.put(index)

    def _run_sandboxed(self, shell_cmd: List[Union[str, Path]]) -> Captured:
        """ Run the command in a sandbox environment """
        with sandbox.context():
            if self.setup != "":
                try:
                    subprocess.run(
                        self.setup,
                        shell=True,
                        cwd=Config.sandbox_dir,
                        stderr=subprocess.STDOUT,
                        stdout=subprocess.PIPE,
                        check=True
                    )
                except subprocess.CalledProcessError as e:
                    print("Error: `{}` setup command failed for `{}`\n\twith '{}'"
                          .format(self.setup,
                                  self.cmd,
                                  "no stderr" if e.stdout is None
                                  else e.stdout.decode().strip()))
                    sys.exit(1)
            return self._run_capture(shell_cmd)

    def _run_capture(self, shell_cmd: List[Union[str, Path]]) -> Captured:
        """ Capture the output (stdout and stderr)
            Capture the content of the watched files after the command is run
        """
        # run the command in the sandbox
        process = subprocess.Popen(
            [*shell_cmd, self.cmd],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=Config.sandbox_dir,
            env={
                'PATH': Config.shell_path_variable,
                'TERM': 'xterm-256color',
                **self.exports,
            },
        )

        # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
        try:
            stdout, _ = process.communicate(
                timeout=(self.timeout if not Config.check_leaks else Config.timeout_leaks))
        except subprocess.TimeoutExpired:
            process.kill()
            # _, _ = process.communicate(timeout=2)
            return Captured.timeout()
        try:
            output = stdout.decode()
        except UnicodeDecodeError:
            output = "UNICODE ERROR: {}".format(process.stdout)

        # capture watched files content
        files_content: List[Optional[str]] = []
        for file_name in self.files:
            try:
                with open(os.path.join(Config.sandbox_dir, file_name), "rb") as f:
                    files_content.append(f.read().decode())
            except FileNotFoundError:
                files_content.append(None)

        # apply output/status hooks
        for hook in self.hook:
            output = hook(output)
        for hook_status in self.hook_status:
            process.returncode = hook_status(process.returncode)

        # replace reference prefix with minishell prefix
        lines = output.split('\n')
        for i, line in enumerate(lines):
            lines[i] = line = re.sub("line [01]: ", "", lines[i], 1)
            if line.startswith(Config.shell_reference_prefix):
                lines[i] = Config.minishell_prefix + line[len(Config.shell_reference_prefix):]
        output = '\n'.join(lines)

        return Captured(output, process.returncode, files_content)

    @property
    def full_cmd(self) -> str:
        """ Return the command prefixed by the setup and exports """
        s = self.cmd
        if len(self.exports) != 0:
            s = "[EXPORTS {}] {}".format(
                ' '.join(["{}='{}'".format(k, v) for k, v in self.exports.items()]), s)
        if self.setup != "":
            s = "[SETUP {}] {}".format(self.setup, s)
        return s

    @classmethod
    def try_run(cls, cmd: str) -> str:
        test = Test(cmd)
        test.run(0)
        if isinstance(test.result, LeakResult):
            return test.result.captured.output
        elif isinstance(test.result, Result):
            return test.result.actual.output
        else:
            return "No output"
