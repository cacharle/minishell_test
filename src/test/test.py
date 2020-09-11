# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/06/16 21:48:50 by charles           #+#    #+#              #
#    Updated: 2020/09/11 20:39:52 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import subprocess
import time

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
                 hook=None):
        """Test class
           cmd: command to execute
           setup: command to execute before tested command
           files: files to watch (check content after test)
           exports: exported variables
           timeout: maximum amount of time taken by the test
           signal: signal to send to the test
           hook: function to execute on the output of the test
        """
        self.cmd = cmd
        self.setup = setup
        self.files = files
        self.exports = exports
        self.result = None
        self.timeout = timeout
        self.signal = signal
        self.hook = hook

    def run(self):
        """Run the test for minishell and the reference shell and print the result out"""
        expected = self._run_sandboxed(config.REFERENCE_PATH, "-c")
        actual   = self._run_sandboxed(config.MINISHELL_PATH, "-c")
        s = self.cmd
        if self.setup != "":
            s = "[SETUP {}] {}".format(self.setup, s)
        if len(self.exports) != 0:
            s = "[EXPORTS {}] {}".format(
                ' '.join(["{}='{:.20}'".format(k, v) for k, v in self.exports.items()]), s)
        self.result = Result(s, self.files, expected, actual)
        self.result.put()

    def _run_sandboxed(self, shell_path: str, shell_option: str) -> Captured:
        """ Run the command in a sandbox environment
            Capture the output (stdout and stderr)
            Capture the content of the watched files after the command is run
        """

        # create and setup sandbox
        sandbox.create()
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
                              "no stderr" if e.stdout is None else e.stdout.decode().strip()))
                sys.exit(1)

        # run the command in the sandbox
        process = subprocess.Popen(
            [shell_path, shell_option, self.cmd],
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            cwd=config.SANDBOX_PATH,
            env={
                'PATH': config.PATH_VARIABLE,
                'TERM': 'xterm-256color',
                **self.exports,
            },
        )
        if self.signal is not None:
            time.sleep(0.2)
            process.send_signal(self.signal)
        else:
            try:
                process.wait(timeout=self.timeout)
            except subprocess.TimeoutExpired:
                return Captured.timeout()

        # get command output
        try:
            stdout, _ = process.communicate()
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

        sandbox.remove()
        if self.hook is not None:
            output = self.hook(output)
        return Captured(output, process.returncode, files_content)
