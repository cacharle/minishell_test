# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    decorator.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:28:00 by charles           #+#    #+#              #
#    Updated: 2021/02/05 17:44:25 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import inspect
from typing import List

from minishell_test.suite import Suite
from minishell_test.test import Test


def suite(groups: List[str] = [], bonus: bool = False):  # type: ignore
    """Decorator generator for suites arguments"""

    def suite_wrapper(origin):
        """Decorator for a suite function (fmt: suite_[name]) """

        mod = inspect.getmodule(origin)
        if mod is None:
            raise NotImplementedError
        mod_name = mod.__name__[len("minishell_test.suites."):]
        name = "{}/{}".format(mod_name, origin.__name__[len("suite_"):])
        description = origin.__doc__
        if description is None:
            print("You should had a doc string to the {} suite".format(name))
            description = "no description"
        description = description.split("\n")[0].strip()
        s = Suite(name, groups + [mod_name], bonus, description)

        def test_generator():
            def test(*args, **kwargs):
                s.add(Test(*args, **kwargs))
            origin(test)

        s.generator_func = test_generator
        Suite.available.append(s)
        return test_generator

    return suite_wrapper
