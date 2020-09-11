# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    suite.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:29 by charles           #+#    #+#              #
#    Updated: 2020/09/11 20:35:13 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import config


class Suite:
    available = []

    @classmethod
    def run_all(cls):
        """Run all available suites"""
        for s in cls.available:
            s.run()

    @classmethod
    def setup(cls, asked_names: [str]):
        """Remove not asked suite from available suites"""
        if len(asked_names) == 0:
            asked_names = [s.name for s in cls.available]
        if not config.BONUS:
            cls.available = [s for s in cls.available if not s.bonus]
        cls.available = list(set(
            [s for s in cls.available if s.name in asked_names]
            + [s for s in cls.available if any([g for g in s.groups if g in asked_names])]
        ))
        for s in cls.available:
            s.generator_func()

    @classmethod
    def available_names(cls) -> [str]:
        """List of available suites names"""
        return [s.name for s in cls.available]

    def __init__(self, name: str, groups: [str], bonus: bool = False):
        """Suite class
           name:   suite id
           groups: list of suite groups
           bonus:  is this suite bonus
        """
        self.name = name
        self.groups = groups
        self.bonus = bonus
        self.generator_func = None
        self.tests = []

    def add(self, test):
        """Append a test to the suite"""
        self.tests.append(test)

    def run(self):
        """Run all test in the suite"""
        if config.VERBOSE_LEVEL == 0:
            print(self.name + ": ", end="")
        else:
            print("{} {:#<41}".format("#" * 39, self.name + " "))
        for t in self.tests:
            t.run()
        if config.VERBOSE_LEVEL == 0:
            print()

    def total(self) -> (int, int):
        """Returns the total of passed and failed tests"""
        passed_total = 0
        for t in self.tests:
            if t.result is None:
                return (-1, -1)
            if t.result.passed:
                passed_total += 1
        return (passed_total, len(self.tests) - passed_total)

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
            print("{:<30} \033[32m{:3} [PASS]\033[0m  \033[31m{:3} [FAIL]\033[0m"
                  .format(s.name, pass_total, fail_total))
        print("{:<30} \033[32m{:3} [PASS]\033[0m  \033[31m{:3} [FAIL]\033[0m"
              .format("TOTAL", pass_sum, fail_sum))

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
