# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    result.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:17:34 by charles           #+#    #+#              #
#    Updated: 2021/03/02 14:17:01 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
from typing import Match, List, Optional, Union

from minishell_test.config import Config
from minishell_test.colors import green, red, blue, bold
from minishell_test.test.captured import CapturedCommand, CapturedTimeout, CapturedType


class BaseResult:
    def __init__(self, cmd: str):
        """
        :param cmd:
            The command executed to get to the result
        """
        self._raw_cmd = cmd

    @property
    def passed(self) -> bool:
        """Check if the result passed"""
        raise NotImplementedError

    @property
    def failed(self) -> bool:
        """Check if the result failed"""
        return not self.passed

    @property
    def __repr__(self) -> str:
        raise NotImplementedError

    def summarize(self, index: int) -> str:
        """Summary of the result

        :param index:
            The test index to print when :option:`--show-range` is enabled
        :returns:
            A summary of the result on one line,
            it's length is the width of the terminal.
        """
        printed = self._cmd[:]
        if Config.show_range:
            printed = f"{index:2}: {printed}"
        width = Config.term_cols - len(" [PASS]")
        if len(printed) > width:
            printed = printed[:width - 3] + "..."
        if self.passed:
            return green(f"{printed:{width}} [PASS]")
        else:
            return red(f"{printed:{width}} [FAIL]")

    @property
    def _cmd(self) -> str:
        """The result command with the common control characters escaped"""
        c = self._raw_cmd
        c = c.replace("\t", "\\t")
        c = c.replace("\n", "\\n")
        c = c.replace("\v", "\\v")
        c = c.replace("\r", "\\r")
        c = c.replace("\f", "\\f")
        return c

    @property
    def _cmd_header(self):
        return f"|> WITH {self._cmd}\n"



class Result(BaseResult):
    def __init__(
        self,
        cmd:        str,
        file_names: List[str],
        expected:   CapturedType,
        actual:     CapturedType,
    ):
        """Result class

        :param cmd:
            runned command
        :param file_names:
            names of watched files
        :param expected:
            expected capture
        :param actual:
            actual capture
        """
        super().__init__(cmd)
        self.file_names = file_names
        self.expected   = expected
        self.actual     = actual

    @property
    def passed(self):
        return self.actual == self.expected

    def __repr__(self) -> str:
        """Concat all difference reports"""
        return (
            self._cmd_header +
            self._cmd_diff() +
            self._files_diff() +
            "=" * 80 + '\n'
        )

    def _cmd_diff(self) -> str:
        """Difference in command output"""
        if isinstance(self.actual, CapturedTimeout):
            return "TIMEOUT\n"
        out = ""
        if self.expected.status != self.actual.status:
            out = f"| STATUS: expected {self.expected.status} actual {self.actual.status}\n"
        if self.expected.output != self.actual.output:
            out += self._content_diff(self.expected.output, self.actual.output)
        return out

    _FILE_NOT_CREATED_MESSAGE = "FROM TEST: File not created\n"

    def _files_diff(self):
        """Difference between watched files"""

        if isinstance(self.actual, CapturedTimeout):
            return ""

        def diff(name, expected, actual):
            expected = expected or self._FILE_NOT_CREATED_MESSAGE
            actual   = actual   or self._FILE_NOT_CREATED_MESSAGE
            return f"|# FILE {file_name}\n" + self._content_diff(expected, actual)

        return '\n'.join([
            diff(name, expected, actual)
            for name, expected, actual in
                zip(
                    self.file_names,
                    self.expected.files_content,
                    self.actual.files_content
                )
            if expected != actual
        ])

    def _content_diff(self, expected: str, actual: str) -> str:
        return (
            self._expected_header +
            self._show_newlines(expected) +
            self._actual_header +
            self._show_newlines(actual)
        )

    def _header(self, title: str) -> str:
        """Create a 80 characters wide header in the format ``-- title --``"""
        return f"|{'-' * 40}{title:-<40}\n"

    @property
    def _expected_header(self) -> str:
        return self._header("EXPECTED")

    @property
    def _actual_header(self) -> str:
        return self._header("ACTUAL")

    def _show_newlines(self, s: str) -> str:
        """Add a ``$`` at the end of each newline

            If the string doesn't end with a newline add one but doesn't add a
            ``$`` to represent it.
        """
        s = s.replace("\n", "$\n")
        if len(s) < 2:
            return s
        if s[-1] != '\n':
            s += '\n'
        return s


class LeakResultException(Exception):
    def __init__(self, result: 'LeakResult'):
        self._result = result

    def __str__(self) -> str:
        return f"valgrind output parsing failed for `{self._result._cmd}`:\n{self._result._captured.output}"


class LeakResult(BaseResult):
    def __init__(self, cmd: str, captured: CapturedType):
        self._captured = captured
        super().__init__(cmd)

    def __repr__(self) -> str:
        return self._cmd_header + self.captured.output

    @property
    def passed(self) -> str:
        if isinstance(self._captured, CapturedTimeout):
            return False
        return self._lost_bytes == 0

    _VALGRIND_OK_MESSAGE = "All heap blocks were freed -- no leaks are possible"

    @property
    def _lost_bytes(self):
        # Some versions of valgrind don't output `definitely` and `indirectly`
        # when no leaks are found.
        if self._captured.output.find(self._VALGRIND_OK_MESSAGE) != -1:
            return 0
        definite_match = self._search_leak_kind("definitely")
        indirect_match = self._search_leak_kind("indirectly")
        definite_bytes = int(definite_match.group("bytes").replace(",", ""))
        indirect_bytes = int(indirect_match.group("bytes").replace(",", ""))
        return definite_bytes + indirect_bytes

    def _search_leak_kind(self, kind: str) -> Match:
        match = re.search(
            r"==\d+==\s+" + kind + r" lost: (?P<bytes>[0-9,]+) bytes in [0-9,]+ blocks",
            self._captured.output
        )
        if match is None:
            raise LeakResultException(self)
        return match
