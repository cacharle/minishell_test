# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    suite.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:29 by charles           #+#    #+#              #
#    Updated: 2021/03/06 15:57:52 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from typing import List, Tuple, Optional, Callable

from minishell_test.config import Config
from minishell_test.test import Test
from minishell_test import colors


class SuiteException(Exception):
    """ Base exception for suite """
    pass


class SuiteExitFirstException(SuiteException):
    pass


# class AmbiguousNameException(SuiteException):
#     def __init__(self, name: str, matches: List[str]):
#         self._name = name
#         self._matches = matches
#
#     def __str__(self) -> str:
#         return (f"Ambiguous name `{self._name}` match the following suites"
#                 f"\n\t{', '.join(self._matches)}\n"
#                  "See the --list option to list the _available test suites")


class NoMatchException(SuiteException):
    def __init__(self, name: str):
        self._name = name

    def __str__(self) -> str:
        return (f"Name `{self._name}` doesn't match any suite/group name\n\t"
                 "Try to run with -l to see the available suites")


class Suite:
    _available: List['Suite'] = []

    @classmethod
    def run(cls, asked_names: List[str]) -> None:
        """Run all _available suites"""

        """ Remove not asked suite from _available suites
            Tries to autocomplete the asked names
        """

        asked_suites = cls._asked_suites(asked_names)
        for suite in asked_suites:
            suite._register()
        for suite in asked_suites:
            try:
                suite._run()
            except SuiteExitFirstException:
                break

    @classmethod
    def _asked_suites(cls, asked_names: [str]) -> ['Suite']:
        suites = cls._available
        if not Config.bonus:
            suites = [suite for suite in cls._available if not suite._bonus]
        if len(asked_names) == 0:
            asked_names = [suite._name for suite in suites]

        names = []
        for name in asked_names:
            matches = [suite._name for suite in suites if suite._name.startswith(name) or suite._group.startswith(name)]
            if len(matches) == 0:
                raise NoMatchException(name)
            names.extend(matches)

        suites = list(set(
            [suite for suite in suites if suite._name in names] +
            [suite for suite in suites if suite._group in names]
        ))
        return sorted(suites, key=lambda suite: suite._name)

    @classmethod
    def list(cls) -> str:
        max_name_width = max(len(suite._name + suite._group) for suite in cls._available) + 5
        out = ""
        for suite in cls._available:
            prefixed_name = f"{suite._group}/{suite._name} "
            out += f"{prefixed_name:.<{max_name_width}} {suite._description}\n"
        return out

    def __init__(
        self,
        origin,
        name:        str,
        group:       str,
        bonus:       bool = False,
        description: str  = "no description",
    ):
        """Suite class
           name:   suite id
           groups: list of suite groups
           bonus:  is this suite bonus
        """
        self._name                  = name
        self._group                 = group
        self._description           = description
        self._bonus                 = bonus
        self._origin                = origin
        self._tests: List[Test]     = []
        self._results: List[Result] = []

    def _run(self) -> None:
        """Run all test in the suite"""

        title = ' ' + self._name + ' '
        print(colors.blue(f"{title:#^{Config.term_cols}}"))
        if Config.range is not None:
            self._tests = self._tests[Config.range[0] : Config.range[1] + 1]
        for i, test in enumerate(self._tests):
            result = test.run()
            self._results.append(result)
            print(result.summarize(i))
            if Config.exit_first and result.failed:
                raise SuiteExitFirstException()

    def _register(self) -> None:
        def test(*args, **kwargs):
            self._tests.append(Test(*args, **kwargs))
        self._origin(test)

    @classmethod
    def summarize(cls):
        """Print a summary of all runned suites"""
        full_pass_count = sum(suite._pass_count for suite in suites)
        full_fail_count = sum(suite._fail_count for suite in suites)
        lines = ["Summary:"]
        for suite in cls._available:
            lines.append(Suite._stat_summary(suite._name, suite._pass_count, suite._fail_count))
        lines.append(Suite._stat_summary("TOTAL", full_pass_count, full_fail_count))
        return "\n".join(lines) + "\n"

    @property
    def _pass_count(self) -> int:
        count = 0
        for result in self._results:
            if result.passed:
                count += 1
        return count

    @property
    def _fail_count(self) -> int:
        return len(self._results) - self._pass_count

    @staticmethod
    def _stat_summary(self, name: str, pass_count: int, fail_count: int) -> str:
        prefix = f"{name + ' ':.<{Config.term_cols - 24}}"
        pass_str = colors.green("{pass_count:4} [PASS]")
        fail_str = colors.red("{fail_count:4} [FAIL]")
        return f"{prefix} {pass_str} {fail_str}"

    @classmethod
    def save(cls):
        """Save the result of all suites to a file"""
        colors.disable()
        with open(Config.log_path, "w") as file:
            for suite in suites:
                for result in suite._results:
                    if result.failed:
                        file.write(result)
