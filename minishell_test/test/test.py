# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/06/16 21:48:50 by charles           #+#    #+#              #
#    Updated: 2021/02/05 18:35:12 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import subprocess
from typing import Optional, List, Dict, Union, Callable

import minishell_test.config as config
from minishell_test.test.captured import Captured
from minishell_test.test.result import Result, LeakResult
import minishell_test.sandbox as sandbox

HookType       = Union[Callable[[str], str], List[Callable[[str], str]]]
HookStatusType = Union[Callable[[int], int], List[Callable[[int], int]]]


class Test:
    def __init__(
        self,
        cmd:         str,
        setup:       str            = "",
        files:       List[str]      = [],
        exports:     Dict[str, str] = {},
        timeout:     float          = config.TIMEOUT,
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
        self.timeout = timeout
        if not isinstance(hook, list):
            hook = [hook]
        if not isinstance(hook_status, list):
            hook_status = [hook_status]
        self.hook = hook
        self.hook_status = hook_status

    def run(self, index: int) -> None:
        """ Run the test for minishell and the reference shell and print the result out """

        if config.CHECK_LEAKS:
            self.hook = []
            self.hook_status = []
            captured = self._run_sandboxed([*config.VALGRIND_CMD, "-c"])
            if config.VERBOSE_LEVEL == 2:
                print(captured.output)
            self.result = LeakResult(self.full_cmd, captured)
            self.result.put(index)
            return

        expected = self._run_sandboxed([config.REFERENCE_PATH, *config.REFERENCE_ARGS, "-c"])
        actual   = self._run_sandboxed([config.MINISHELL_PATH, "-c"])
        self.result = Result(self.full_cmd, self.files, expected, actual)
        self.result.put(index)

    def _run_sandboxed(self, shell_cmd: List[str]) -> Captured:
        """ Run the command in a sandbox environment """
        with sandbox.context():
            if self.setup != "":
                try:
                    subprocess.run(
                        self.setup,
                        shell=True,
                        cwd=config.SANDBOX_PATH,
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

    def _run_capture(self, shell_cmd: List[str]) -> Captured:
        """ Capture the output (stdout and stderr)
            Capture the content of the watched files after the command is run
        """
        # run the command in the sandbox
        process = subprocess.Popen(
            [*shell_cmd, self.cmd],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=config.SANDBOX_PATH,
            env={
                'PATH': config.PATH_VARIABLE,
                'TERM': 'xterm-256color',
                **self.exports,
            },
        )

        # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
        try:
            stdout, _ = process.communicate(
                timeout=(self.timeout if not config.CHECK_LEAKS else config.CHECK_LEAKS_TIMEOUT))
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
                with open(os.path.join(config.SANDBOX_PATH, file_name), "rb") as f:
                    files_content.append(f.read().decode())
            except FileNotFoundError:
                files_content.append(None)

        # apply output/status hooks
        for hook in self.hook:
            output = hook(output)
        for hook_status in self.hook_status:
            process.returncode = hook_status(process.returncode)
        return Captured(output, process.returncode, files_content)

    @property
    def full_cmd(self):
        """ Return the command prefixed by the setup and exports """
        s = self.cmd
        if len(self.exports) != 0:
            s = "[EXPORTS {}] {}".format(
                ' '.join(["{}='{}'".format(k, v) for k, v in self.exports.items()]), s)
        if self.setup != "":
            s = "[SETUP {}] {}".format(self.setup, s)
        return s
