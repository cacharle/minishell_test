# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/06/16 21:48:50 by charles           #+#    #+#              #
#    Updated: 2020/07/15 18:14:28 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import subprocess
import shutil
import config

class Captured:
    def __init__(self, output: str, status: int, files_content: [str], is_timeout: bool = False):
        lines = output.split('\n')
        for i, l in enumerate(lines):
            if l.find(config.REFERENCE_ERROR_BEGIN) == 0:
                lines[i] = l.replace(config.REFERENCE_ERROR_BEGIN, config.MINISHELL_ERROR_BEGIN, 1)
            elif l.find(config.REFERENCE_PATH + ": ") == 0:
                lines[i] = l.replace(config.REFERENCE_PATH + ": ", config.MINISHELL_ERROR_BEGIN, 1)

        self.output = '\n'.join(lines)

        self.status = status
        self.files_content = files_content
        self.is_timeout = is_timeout

    def __eq__(self, other: 'Result') -> bool:
        if self.is_timeout and other.is_timeout:
            return True
        return (self.output == other.output and
                self.status == other.status and
                all([x == y for x, y in zip(self.files_content, other.files_content)]))

    @staticmethod
    def timeout():
        return Captured("", 0, [], is_timeout = True)

class Result:
    RED_CHARS   = "\033[31m"
    GREEN_CHARS = "\033[32m"
    BLUE_CHARS  = "\033[34m"
    BOLD_CHARS  = "\033[1m"
    CLOSE_CHARS = "\033[0m"

    def __init__(self, cmd: str, file_names: [str], expected: Captured, actual: Captured):
        self.cmd = cmd
        self.file_names = file_names
        self.expected = expected
        self.actual = actual
        self.colored = True
        self.set_colors()

    def toggle_colors(self):
        self.colored = not self.colored

    def set_colors(self):
        if self.colored:
            self.color_red   = self.RED_CHARS
            self.color_green = self.GREEN_CHARS
            self.color_blue  = self.BLUE_CHARS
            self.color_bold  = self.BOLD_CHARS
            self.color_close = self.CLOSE_CHARS
        else:
            self.color_red   = ""
            self.color_green = ""
            self.color_blue  = ""
            self.color_bold  = ""
            self.color_close = ""

    def green(self, s):
        return self.color_green + s + self.color_close

    def red(self, s):
        return self.color_red + s + self.color_close

    def blue(self, s):
        return self.color_blue + s + self.color_close

    def bold(self, s):
        return self.color_bold + s + self.color_close

    @property
    def passed(self):
        return self.actual == self.expected

    @property
    def failed(self):
        return not self.passed

    def __repr__(self):
        if config.VERBOSE_LEVEL == 0:
            return self.green('.') if self.passed else self.red('!')
        elif config.VERBOSE_LEVEL == 1:
            printed = self.cmd[:]
            if len(printed) > 70:
                printed = printed[:67] + "..."
            fmt = self.green("{:74} [PASS]") if self.passed else self.red("{:74} [FAIL]")
            return fmt.format(printed)
        elif config.VERBOSE_LEVEL == 2:
            return self.full_diff()
        else:
            raise RuntimeError

    def put(self):
        if config.VERBOSE_LEVEL == 2 and self.passed:
            return
        print(self, end="")
        if config.VERBOSE_LEVEL == 0:
            sys.stdout.flush()
        else:
            print()

    def header(self, title: str) -> str:
        return self.bold("|---------------------------------------{:-<40}".format(title))

    @property
    def expected_header(self) -> str:
        return self.green(self.header("EXPECTED"))

    @property
    def actual_header(self) -> str:
        return self.red(self.header("ACTUAL"))

    def indicator(self, title: str, prefix: str) -> str:
        return self.bold(self.blue(prefix + " " + title))

    def file_diff(self, file_name: str, expected: str, actual: str) -> str:
        if expected == actual:
            return ""
        return (
            self.indicator("FILE {}".format(file_name), "|#") + '\n'
            + self.expected_header + '\n'
            + ("FROM TEST: File not created\n" if expected is None else self.cat_e(expected))
            + self.actual_header + '\n'
            + ("FROM TEST: File not created\n" if actual is None else self.cat_e(actual))
        )

    def files_diff(self):
        return '\n'.join([self.file_diff(n, e, a) for n, e, a in
                          zip(self.file_names,
                              self.expected.files_content,
                              self.actual.files_content)
                          if e != a])

    def output_diff(self) -> str:
        out = ""
        if self.actual.is_timeout:
            return "TIMEOUT\n"
        if self.expected.status != self.actual.status:
            out += self.indicator("STATUS: expected {} actual {}"
                    .format(self.expected.status, self.actual.status), "| ") + '\n'
        if self.expected.output != self.actual.output:
            out += (self.expected_header + '\n'
                    + self.cat_e(self.expected.output)
                    + self.actual_header + '\n'
                    + self.cat_e(self.actual.output))
        return out

    def full_diff(self) -> str:
        return (self.indicator("WITH {}".format(self.cmd), "|>") + '\n'
                + self.output_diff()
                + self.files_diff()
                + "=" * 80 + '\n')

    def cat_e(self, s: str) -> str:
        s = s.replace("\n", "$\n")
        if len(s) < 2:
            return s
        if s[-1] != '\n':
            s += '\n'
        return s


class Test:
    def __init__(self, cmd: str, setup: str = "", files: [str] = [], exports: {str: str} = {}):
        self.cmd = cmd
        self.setup = setup
        self.files = files
        self.exports = exports
        self.result = None

    def run(self):
        expected = self._run_sandboxed(config.REFERENCE_PATH, "-c")
        actual   = self._run_sandboxed(config.MINISHELL_PATH, "-c")
        self.result = Result(self.cmd, self.files, expected, actual)
        self.result.put()

    def _run_sandboxed(self, shell_path: str, shell_option: str) -> Captured:
        """ run the command in a sandbox environment

            capture the output (stdout and stderr)
            capture the content of the watched files after the command is run
        """

        try:
            os.mkdir(config.SANDBOX_PATH)
        except OSError:
            pass
        if self.setup != "":
            try:
                setup_status = subprocess.run(
                        self.setup, shell=True, cwd=config.SANDBOX_PATH, check=True)
            except subprocess.CalledProcessError as e:
                print("Error: `{}` setup command failed for `{}`\n\twith '{}'"
                      .format(setup, cmd, e.stderr.decode().strip()))
                sys.exit(1)

        try:
            process_status = subprocess.run(
                [shell_path, shell_option, self.cmd],
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                cwd=config.SANDBOX_PATH,
                env={
                    'PATH': config.PATH_VARIABLE,
                    'TERM': 'xterm-256color',
                    **self.exports
                },
                timeout=0.5
            )
        except subprocess.TimeoutExpired:
            return Captured.timeout()

        output = process_status.stdout.decode()

        # capture watched files content
        files_content = []
        for file_name in self.files:
            try:
                with open(os.path.join(config.SANDBOX_PATH, file_name), "rb") as f:
                    files_content.append(f.read().decode())
            except FileNotFoundError as e:
                files_content.append(None)
        shutil.rmtree(config.SANDBOX_PATH)
        return Captured(output, process_status.returncode, files_content)
