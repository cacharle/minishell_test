# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/06/16 21:48:50 by charles           #+#    #+#              #
#    Updated: 2020/06/17 08:52:48 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import subprocess
import shutil
import config

import utils

class Result:
    def __init__(self, output: str, files_content: [str]):
        self.output = output
        self.files_content = files_content

    def __eq__(self, other: 'Result') -> bool:
        return (self.output == other.output and
                all([x == y for x, y in zip(self.files_content, other.files_content)]))


class Test:
    def __init__(self, cmd: str, setup: str = "", files: [str] = [], exports: {str: str} = {}):
        self.cmd = cmd
        self.setup = setup
        self.files = files
        self.exports = exports

    def run(self):
        self.expected = self._run_sandboxed(config.REFERENCE_PATH)
        self.actual   = self._run_sandboxed(config.MINISHELL_PATH)

        self._put_result()

        # if not verbose:
        #     put_result(passed, cmd)
        # if verbose:
        #     if not passed:
        #         print(diff(cmd, expected, actual, files, expected_files, actual_files, color=True))
        #     else:
        # self._put_line_result(passed)

    def _run_sandboxed(self, shell_path: str) -> Result:
        """ run the command in a sandbox environment, return the output (stdout and stderr) of it """

        try:
            os.mkdir(config.SANDBOX_PATH)
        except OSError:
            pass
        if self.setup != "":
            try:
                setup_status = subprocess.run(self.setup,
                                              shell=True,
                                              cwd=config.SANDBOX_PATH,
                                              check=True)
            except subprocess.CalledProcessError as e:
                print("Error: `{}` setup command failed for `{}`\n\twith '{}'"
                      .format(setup, cmd, e.stderr.decode().strip()))
                sys.exit(1)

        # TODO: add timeout
        # https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module
        process_status = subprocess.run([shell_path, "-c", self.cmd],
                                        stderr=subprocess.STDOUT,
                                        stdout=subprocess.PIPE,
                                        cwd=config.SANDBOX_PATH,
                                        env={'PATH': config.PATH_VARIABLE, **self.exports})
        output = process_status.stdout.decode()

        files_content = []
        for file_name in self.files:
            try:
                with open(os.path.join(config.SANDBOX_PATH, file_name), "rb") as f:
                    files_content.append(f.read().decode())
            except FileNotFoundError as e:
                files_content.append(None)

        shutil.rmtree(config.SANDBOX_PATH)
        return Result(output, files_content)

    def _put_result(self):
        passed = self.actual == self.expected
        if config.VERBOSE_LEVEL == 0:
            sys.stdout.write(utils.green('.') if passed else utils.red('!'))
            sys.stdout.flush()
        elif config.VERBOSE_LEVEL == 1:
            printed = self.cmd
            if len(printed) > 70:
                printed = printed[:67] + "..."
            fmt = utils.green("{:74} [PASS]") if passed else utils.red("{:74} [FAIL]")
            print(fmt.format(printed))
        elif config.VERBOSE_LEVEL == 2:
            pass
            # print(diff(cmd, expected, actual, files, expected_files, actual_files, color=True))
        else:
            raise RuntimeError
