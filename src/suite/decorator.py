# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    decorator.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:28:00 by charles           #+#    #+#              #
#    Updated: 2020/09/11 22:08:36 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from suite import Suite
from test import Test
import inspect


def suite(groups: [str] = [], bonus: bool = False):
    """Decorator generator for suites arguments"""

    def suite_wrapper(origin):
        """Decorator for a suite function (fmt: suite_[name]) """

        mod_name = inspect.getmodule(origin).__name__[len("suites."):]
        # print(mod_name)

        name = "{}/{}".format(mod_name, origin.__name__[len("suite_"):])
        s = Suite(name, groups + [mod_name], bonus)

        def test_generator():
            def test(*args, **kwargs):
                s.add(Test(*args, **kwargs))
            origin(test)

        s.generator_func = test_generator
        Suite.available.append(s)
        return test_generator

    return suite_wrapper
