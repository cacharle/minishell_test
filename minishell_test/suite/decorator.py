# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    decorator.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:28:00 by charles           #+#    #+#              #
#    Updated: 2021/03/06 11:31:33 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import inspect
from typing import List

from minishell_test.suite import Suite
from minishell_test.test import Test


class SuiteRegistrationException(Exception):
    def __init__(self, function_name: str, message: str):
        self._function_name = function_name
        self._message = message

    def __str__(self) -> str:
        return "Error during the registration of {self._function_name} as a suite: {self._message}"


_SUITE_FUNCTION_PREFIX = "suite_"


def suite(bonus: bool = False):  # type: ignore
    """Decorator generator for suites arguments"""

    def suite_wrapper(origin):
        """Decorator for a suite function (fmt: suite_[name]) """

        # get the function name
        function_name = origin.__name__
        if not function_name.startswith(_SUITE_FUNCTION_PREFIX):
            raise SuiteRegistrationException(function_name, f"Function need to start with {_SUITE_FUNCTION_PREFIX}")
        function_name = function_name[len(_SUITE_FUNCTION_PREFIX):]
        # get the module name
        module = inspect.getmodule(origin)
        if module is None:
            raise SuiteRegistrationException(function_name, "Could not get function module")
        module_name = module.__name__[len("minishell_test.suites."):]
        # get the first line of the function docstring as the suite description
        description = origin.__doc__
        if description is None:
            warnings.warn(f"You should had a doc string to the {name} suite")
            description = "no description"
        description = description.splitlines()[0].strip()

        suite = Suite(origin, function_name, module_name, bonus, description)
        Suite._available.append(suite)

        # def test_generator():
        #     def test(*args, **kwargs):
        #         suite.append_test(Test(*args, **kwargs))
        #     origin(test)
        # suite.generator_func = test_generator
        return origin

    return suite_wrapper
