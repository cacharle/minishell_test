# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    suite.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:29 by charles           #+#    #+#              #
#    Updated: 2021/03/02 13:17:31 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from typing import List, Tuple, Optional, Callable

from minishell_test.config import Config
from minishell_test.test import Test


class SuiteException(Exception):
    """ Base exception for suite """
    pass


class AmbiguousNameException(SuiteException):
    def __init__(self, name: str, matches: List[str]):
        self.name = name
        self.matches = matches

    def __str__(self) -> str:
        return (("Ambiguous name `{}` match the following suites\n\t{}\n"
                 "Try to run with -l to see the available suites")
                .format(self.name, ', '.join(self.matches)))


class NoMatchException(SuiteException):
    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return (("Name `{}` doesn't match any suite/group name\n\t"
                 "Try to run with -l to see the available suites")
                .format(self.name))


class Suite:
    available: List['Suite'] = []

    @classmethod
    def run_all(cls):
        """Run all available suites"""
        for s in cls.available:
            if not s.run() and Config.exit_first:
                break

    @classmethod
    def setup(cls, asked_names: List[str]) -> None:
        """ Remove not asked suite from available suites
            Tries to autocomplete the asked names
        """
        if not Config.bonus:
            cls.available = [s for s in cls.available if not s.bonus]
        if len(asked_names) == 0:
            asked_names = [s.name for s in cls.available]

        suite_names = [s.name for s in cls.available]
        names = []
        for i, name in enumerate(asked_names):
            if name in suite_names:
                names.append(name)
                continue
            matches = [n for n in suite_names
                       if n.find("/") != -1 and
                       n[n.find("/") + 1:].startswith(name) or
                       n.startswith(name)]
            if len(matches) == 1:
                names.append(matches[0])
            elif len(matches) != 0 and all(n.startswith(name) for n in matches):
                names.extend(matches)
            elif len(matches) > 2:
                raise AmbiguousNameException(name, matches)
            elif len(matches) == 0:
                raise NoMatchException(name)

        cls.available = list(set(
            [s for s in cls.available if s.name in names] +
            [s for s in cls.available if any(g for g in s.groups if g in names)]
        ))
        cls.available.sort(key=lambda s: s.name)
        for s in cls.available:
            if s.generator_func is not None:
                s.generator_func()

    @classmethod
    def available_names(cls) -> List[str]:
        """List of available suites names"""
        return [s.name for s in cls.available]

    @classmethod
    def list(cls):
        print("Groups:")
        print("\n".join({" - " + ', '.join(s.groups) for s in Suite.available}))
        print("The available suites are:")
        max_name_width = max(len(s.name) for s in Suite.available) + 5
        lines = [
            " - {:.<{max_name_width}} {}".format(
                s.name + " ",
                s.description,
                max_name_width=max_name_width
            )
            for s in Suite.available
        ]
        print("\n".join(lines))

    def __init__(
        self,
        name: str,
        groups: List[str],
        bonus: bool = False,
        description: str = "no description",
    ):
        """Suite class
           name:   suite id
           groups: list of suite groups
           bonus:  is this suite bonus
        """
        self.name = name
        self.groups = groups
        self.description = description
        self.bonus = bonus
        self.generator_func: Optional[Callable] = None
        self.tests: List[Test] = []
        self.results: List[Result] = []

    def add(self, test):
        """Append a test to the suite"""
        self.tests.append(test)

    BLUE_CHARS  = "\033[34m"
    CLOSE_CHARS = "\033[0m"

    def run(self) -> bool:
        """Run all test in the suite"""
        print("{}{:#^{width}}{}".format(
            self.BLUE_CHARS,
            " " + self.name + " ",
            self.CLOSE_CHARS,
            width=Config.term_cols
        ))
        if Config.range is not None:
            self.tests = self.test[Config.range[0] : Config.range[1] + 1]
        for i, test in enumerate(self.tests):
            result = test.run()
            self.results.append(result)
            print(result.to_string(i))
            if Config.exit_first and result is not None and result.failed:
                return False
        return True

    def total(self) -> Tuple[int, int]:
        """Returns the total of passed and failed tests"""
        passed_total = 0
        for result in self.results:
            if result is None:
                return (-1, -1)
            if result.passed:
                passed_total += 1
        return passed_total, len(self.tests) - passed_total

    @classmethod
    def summarize(cls):
        """Print a summary of all runned suites"""
        pass_sum = 0
        fail_sum = 0
        print("\nSummary:")
        for s in cls.available:
            (pass_total, fail_total) = s.total()
            if pass_total == -1:
                continue
            pass_sum += pass_total
            fail_sum += fail_total
            print("{:.<{width}} \033[32m{:4} [PASS]\033[0m \033[31m{:4} [FAIL]\033[0m"
                  .format(s.name + " ", pass_total, fail_total, width=Config.term_cols - 24))
        print("{:.<{width}} \033[32m{:4} [PASS]\033[0m \033[31m{:4} [FAIL]\033[0m"
              .format("TOTAL ", pass_sum, fail_sum, width=Config.term_cols - 24))

    @classmethod
    def save_log(cls):
        """Save the result of all suites to a file"""
        colors.disable()
        with open(Config.log_path, "w") as log_file:
            for result in self.results:
                if result is not None and result.failed:
                    log_file.write(result.full_diff() + '\n')
