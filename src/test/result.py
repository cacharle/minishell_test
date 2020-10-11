# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    result.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:17:34 by charles           #+#    #+#              #
#    Updated: 2020/10/11 14:09:24 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import sys
import re

import config
from test.captured import Captured


class Result:
    RED_CHARS   = "\033[31m"
    GREEN_CHARS = "\033[32m"
    BLUE_CHARS  = "\033[34m"
    BOLD_CHARS  = "\033[1m"
    CLOSE_CHARS = "\033[0m"

    def __init__(
        self,
        cmd: str,
        file_names: [str],
        expected: Captured,
        actual: Captured,
        leak_output: str = None
    ):
        """Result class
           cmd:         runned command
           file_names:  names of watched files
           expected:    expected capture
           actual:      actual capture
           leak_output: output of valgrind in check leak mode
        """
        self.cmd = cmd
        self.file_names = file_names
        self.expected = expected
        self.actual = actual
        self.colored = True
        self.leak_output = leak_output
        self.set_colors()

    @staticmethod
    def leak(cmd: str, leak_output: str = None):
        return Result(cmd, None, None, None, leak_output)

    def _search_leak_kind(self, kind: str) -> int:
        match = re.search(
            r"==\d+==\s+" + kind + r" lost: (?P<bytes>[0-9,]+) bytes in [0-9,]+ blocks",
            self.leak_output
        )
        if match is None:
            raise RuntimeError(
                "valgrind output parsing failed for `{}`:\n{}"
                .format(self.cmd, self.leak_output)
            )
        return match

    @property
    def lost_bytes(self):
        definite_match = self._search_leak_kind("definitely")
        indirect_match = self._search_leak_kind("indirectly")
        definite_bytes = int(definite_match.group("bytes").replace(",", ""))
        indirect_bytes = int(indirect_match.group("bytes").replace(",", ""))
        return definite_bytes + indirect_bytes

    @property
    def passed(self):
        """Check if the result passed"""
        if self.leak_output is not None:
            return self.lost_bytes == 0
        return self.actual == self.expected

    @property
    def failed(self):
        """Check if the result failed"""
        return not self.passed

    def __repr__(self):
        """Returns a representation of the result based on the verbosity"""
        if config.VERBOSE_LEVEL == 0:
            return self.green('.') if self.passed else self.red('!')
        elif config.VERBOSE_LEVEL == 1:
            printed = self.escaped_cmd[:]
            if config.SHOW_RANGE:
                printed = "{:2}: ".format(self.index) + printed
            if len(printed) > config.TERM_COLS - 7:
                printed = printed[:config.TERM_COLS - 10] + "..."
            fmt = self.green("{:{width}} [PASS]") if self.passed else self.red("{:{width}} [FAIL]")
            return fmt.format(printed, width=config.TERM_COLS - 7)
        elif config.VERBOSE_LEVEL == 2:
            return self.full_diff()
        else:
            raise RuntimeError("Invalid verbose level")

    def put(self, index: int):
        """Print a summary of the result"""
        if config.VERBOSE_LEVEL == 2 and self.passed:
            return
        self.index = index
        print(self, end="")
        if config.VERBOSE_LEVEL == 0:
            sys.stdout.flush()
        else:
            print()

    def header(self, title: str) -> str:
        """Create a one line header with a title"""
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
        """Difference between 2 files"""
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
        """Difference between watched files"""
        return '\n'.join([self.file_diff(n, e, a) for n, e, a in
                          zip(self.file_names,
                              self.expected.files_content,
                              self.actual.files_content)
                          if e != a])

    def output_diff(self) -> str:
        """Difference in command output"""
        out = ""
        if self.actual.is_timeout:
            return "TIMEOUT\n"
        if self.expected.status != self.actual.status:
            out += self.indicator(
                "STATUS: expected {} actual {}"
                .format(self.expected.status, self.actual.status), "| "
            ) + '\n'
        if self.expected.output != self.actual.output:
            out += (self.expected_header + '\n'
                    + self.cat_e(self.expected.output)
                    + self.actual_header + '\n'
                    + self.cat_e(self.actual.output))
        return out

    def full_diff(self) -> str:
        """Concat all difference reports"""
        rest = ""
        if self.leak_output is not None:
            rest = self.leak_output
        else:
            rest = (self.output_diff() + self.files_diff() + "=" * 80 + '\n')
        return (self.indicator("WITH {}".format(self.escaped_cmd), "|>") + '\n' + rest)

    def cat_e(self, s: str) -> str:
        """Pass a string through a cat -e like output"""
        s = s.replace("\n", "$\n")
        if len(s) < 2:
            return s
        if s[-1] != '\n':
            s += '\n'
        return s

    @property
    def escaped_cmd(self):
        """Escape common control characters"""
        return (self.cmd
                .replace("\t", "\\t")
                .replace("\n", "\\n")
                .replace("\v", "\\v")
                .replace("\r", "\\r")
                .replace("\f", "\\f"))

    def set_colors(self):
        """Set colors strings on or off based on self.colored"""
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
