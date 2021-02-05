# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    suite.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:29 by charles           #+#    #+#              #
#    Updated: 2021/02/04 16:13:08 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import sys
from typing import List, Tuple, Optional, Callable

import config
from test import Test


class Suite:
    available: List['Suite'] = []

    @classmethod
    def run_all(cls):
        """Run all available suites"""
        for s in cls.available:
            if not s.run() and config.EXIT_FIRST:
                break

    @classmethod
    def setup(cls, asked_names: List[str]) -> None:
        """ Remove not asked suite from available suites
            Tries to autocomplete the asked names
        """
        if not config.BONUS:
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
                       if n.find("/") != -1
                       and n[n.find("/") + 1:].startswith(name)
                       or n.startswith(name)]
            if len(matches) == 1:
                names.append(matches[0])
            elif len(matches) != 0 and all(n.startswith(name) for n in matches):
                names.extend(matches)
            elif len(matches) > 2:
                print(("Ambiguous name `{}` match the following suites\n\t{}\n"
                       "Try to run with -l to see the available suites")
                      .format(name, ', '.join(matches)))
                sys.exit(1)
            elif len(matches) == 0:
                print(("Name `{}` doesn't match any suite/group name\n\t"
                       "Try to run with -l to see the available suites")
                      .format(name))
                sys.exit(1)

        cls.available = list(set(
            [s for s in cls.available if s.name in names]
            + [s for s in cls.available if any(g for g in s.groups if g in names)]
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

    def add(self, test):
        """Append a test to the suite"""
        self.tests.append(test)

    BLUE_CHARS  = "\033[34m"
    CLOSE_CHARS = "\033[0m"

    def run(self) -> bool:
        """Run all test in the suite"""
        if config.VERBOSE_LEVEL == 0:
            print(self.name + ": ", end="")
        else:
            print("{}{:#^{width}}{}".format(
                self.BLUE_CHARS,
                " " + self.name + " ",
                self.CLOSE_CHARS,
                width=config.TERM_COLS
            ))
            for i, t in enumerate(self.tests):
                if config.RANGE is not None:
                    if not (config.RANGE[0] <= i <= config.RANGE[1]):
                        continue
                t.run(i)
                if config.EXIT_FIRST and t.result is not None and t.result.failed:
                    return False
        if config.VERBOSE_LEVEL == 0:
            print()
        return True

    def total(self) -> Tuple[int, int]:
        """Returns the total of passed and failed tests"""
        passed_total = 0
        for t in self.tests:
            if t.result is None:
                return (-1, -1)
            if t.result.passed:
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
                  .format(s.name + " ", pass_total, fail_total, width=config.TERM_COLS - 24))
        print("{:.<{width}} \033[32m{:4} [PASS]\033[0m \033[31m{:4} [FAIL]\033[0m"
              .format("TOTAL ", pass_sum, fail_sum, width=config.TERM_COLS - 24))

    @classmethod
    def save_log(cls):
        """Save the result of all suites to a file"""
        with open(config.LOG_PATH, "w") as log_file:
            for s in cls.available:
                for t in s.tests:
                    if t.result is not None and t.result.failed:
                        t.result.colored = False
                        t.result.set_colors()
                        log_file.write(t.result.full_diff() + '\n')
