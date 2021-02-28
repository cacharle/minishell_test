# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    result.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:17:34 by charles           #+#    #+#              #
#    Updated: 2021/02/27 12:28:20 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
from typing import Match, List, Optional

from minishell_test.config import Config
from minishell_test.test.captured import Captured


class BaseResult:
    RED_CHARS   = "\033[31m"
    GREEN_CHARS = "\033[32m"
    BLUE_CHARS  = "\033[34m"
    BOLD_CHARS  = "\033[1m"
    CLOSE_CHARS = "\033[0m"

    def __init__(self, cmd: str):
        self.cmd = cmd
        self.colored = True
        self.set_colors()

    @property
    def passed(self):
        """Check if the result passed"""
        raise NotImplementedError

    @property
    def failed(self):
        """Check if the result failed"""
        return not self.passed

    def __repr__(self):
        """Returns a representation of the result based on the verbosity"""
        printed = self._escaped_cmd[:]
        if Config.show_range:
            printed = "{:2}: ".format(self.index) + printed
        if len(printed) > Config.term_cols - 7:
            printed = printed[:Config.term_cols - 10] + "..."
        fmt = self.green("{:{width}} [PASS]") if self.passed else self.red("{:{width}} [FAIL]")
        return fmt.format(printed, width=Config.term_cols - 7)

    def put(self, index: int) -> None:
        """Print a summary of the result"""
        self.index = index
        print(self)

    def indicator(self, title: str, prefix: str) -> str:
        return self.bold(self.blue(prefix + " " + title))

    def full_diff(self) -> str:
        raise NotImplementedError

    @property
    def _escaped_cmd(self):
        """Escape common control characters"""
        c = self.cmd
        c = c.replace("\t", "\\t")
        c = c.replace("\n", "\\n")
        c = c.replace("\v", "\\v")
        c = c.replace("\r", "\\r")
        c = c.replace("\f", "\\f")
        return c

    @property
    def _header_with(self):
        return self.indicator("WITH {}".format(self._escaped_cmd), "|>") + '\n'

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


class Result(BaseResult):
    def __init__(
        self,
        cmd: str,
        file_names: List[str],
        expected: Captured,
        actual: Captured,
    ):
        """Result class
           cmd:         runned command
           file_names:  names of watched files
           expected:    expected capture
           actual:      actual capture
        """
        self.file_names = file_names
        self.expected = expected
        self.actual = actual
        super().__init__(cmd)

    @property
    def passed(self):
        return self.actual == self.expected

    def header(self, title: str) -> str:
        return self.bold("|---------------------------------------{:-<40}".format(title))

    @property
    def expected_header(self) -> str:
        return self.green(self.header("EXPECTED")) + '\n'

    @property
    def actual_header(self) -> str:
        return self.red(self.header("ACTUAL")) + '\n'

    def cat_e(self, s: Optional[str]) -> str:
        """Pass a string through a cat -e like output"""
        if s is None:
            return "FROM TEST: File not created\n"
        s = s.replace("\n", "$\n")
        if len(s) < 2:
            return s
        if s[-1] != '\n':
            s += '\n'
        return s

    def file_diff(self, file_name: str, expected: Optional[str], actual: Optional[str]) -> str:
        """Difference between 2 files"""
        if expected == actual:
            return ""
        file_header = self.indicator("FILE {}".format(file_name), "|#") + '\n'
        return (
            file_header +
            self.expected_header +
            self.cat_e(expected) +
            self.actual_header +
            self.cat_e(actual)
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
            out += (self.expected_header +
                    self.cat_e(self.expected.output) +
                    self.actual_header +
                    self.cat_e(self.actual.output))
        return out

    def full_diff(self) -> str:
        """Concat all difference reports"""
        return self._header_with + self.output_diff() + self.files_diff() + "=" * 80 + '\n'


class LeakResult(BaseResult):
    def __init__(self, cmd: str, captured: Captured):
        self.captured = captured
        super().__init__(cmd)

    def _search_leak_kind(self, kind: str) -> Match:
        match = re.search(
            r"==\d+==\s+" + kind + r" lost: (?P<bytes>[0-9,]+) bytes in [0-9,]+ blocks",
            self.captured.output
        )
        if match is None:
            raise RuntimeError(
                "valgrind output parsing failed for `{}`:\n{}"
                .format(self.cmd, self.captured.output)
            )
        return match

    @property
    def _lost_bytes(self):
        if self.captured.output.find("All heap blocks were freed -- no leaks are possible") != -1:
            definite_bytes = 0
            indirect_bytes = 0
        else:
            definite_match = self._search_leak_kind("definitely")
            indirect_match = self._search_leak_kind("indirectly")
            definite_bytes = int(definite_match.group("bytes").replace(",", ""))
            indirect_bytes = int(indirect_match.group("bytes").replace(",", ""))
        return definite_bytes + indirect_bytes

    @property
    def passed(self):
        """Check if the result passed"""
        if self.captured.is_timeout:
            return False
        return self._lost_bytes == 0

    def full_diff(self) -> str:
        """Concat all difference reports"""
        return self._header_with + self.captured.output
