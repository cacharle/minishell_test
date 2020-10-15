# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/06/16 21:48:50 by charles           #+#    #+#              #
#    Updated: 2020/10/15 08:50:05 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import subprocess

import config
from test.captured import Captured
from test.result import Result
import sandbox


class Test:
    def __init__(self,
                 cmd: str,
                 setup: str = "",
                 files: [str] = [],
                 exports: {str: str} = {},
                 timeout: float = config.TIMEOUT,
                 signal=None,
                 hook=[],
                 hook_status=[]):
        """ Test class
            cmd:         command to execute
            setup:       command to execute before tested command
            files:       files to watch (check content after test)
            exports:     exported variables
            timeout:     maximum amount of time taken by the test
            signal:      signal to send to the test
            hook:        function to execute on the output of the test
            hook_status: function to execute on status code
        """
        self.cmd = cmd
        self.setup = setup
        self.files = files
        self.exports = exports
        self.result = None
        self.timeout = timeout
        self.signal = signal
        self.hook = hook
        self.hook_status = hook_status
        if type(self.hook) is not list:
            self.hook = [self.hook]
        if type(self.hook_status) is not list:
            self.hook_status = [self.hook_status]

    def run(self, index: int):
        """ Run the test for minishell and the reference shell and print the result out """

        if config.CHECK_LEAKS:
            self.hook = []
            self.hook_status = []
            captured = self._run_sandboxed([*config.VALGRIND_CMD, "-c"])
            if config.VERBOSE_LEVEL == 2:
                print(captured.output)
            self.result = Result.leak(self.full_cmd, captured.output)
            self.result.put(index)
            return

        expected = self._run_sandboxed([config.REFERENCE_PATH, *config.REFERENCE_ARGS, "-c"])
        actual   = self._run_sandboxed([config.MINISHELL_PATH, "-c"])
        self.result = Result(self.full_cmd, self.files, expected, actual)
        self.result.put(index)

    def _run_sandboxed(self, shell_cmd: [str]) -> Captured:
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

    def _run_capture(self, shell_cmd: [str]) -> Captured:
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
        # if self.signal is not None:
        #     time.sleep(0.1)
        #     process.send_signal(self.signal)

        # https://docs.python.org/3/library/subprocess.html#subprocess.Popen.communicate
        try:
            stdout, _ = process.communicate(timeout=(self.timeout if not config.CHECK_LEAKS else 10))
        except subprocess.TimeoutExpired:
            process.kill()
            # _, _ = process.communicate(timeout=2)
            return Captured.timeout()
        try:
            output = stdout.decode()
        except UnicodeDecodeError:
            output = "UNICODE ERROR: {}".format(process.stdout)

        # capture watched files content
        files_content = []
        for file_name in self.files:
            try:
                with open(os.path.join(config.SANDBOX_PATH, file_name), "rb") as f:
                    files_content.append(f.read().decode())
            except FileNotFoundError:
                files_content.append(None)

        # apply output/status hooks
        for h in self.hook:
            output = h(output)
        for h in self.hook_status:
            process.returncode = h(process.returncode)
        return Captured(output, process.returncode, files_content)

    @property
    def full_cmd(self):
        """ Return the command prefixed by the setup and exports """
        s = self.cmd
        if self.setup != "":
            s = "[SETUP {}] {}".format(self.setup, s)
        if len(self.exports) != 0:
            s = "[EXPORTS {}] {}".format(
                ' '.join(["{}='{:.20}'".format(k, v) for k, v in self.exports.items()]), s)
        return s
