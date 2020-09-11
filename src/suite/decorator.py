# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    decorator.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:28:00 by charles           #+#    #+#              #
#    Updated: 2020/09/11 12:28:14 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from suite import Suite
from test import Test

def suite(origin):
    """ decorator for a suite function (fmt: suite_[name]) """

    name = origin.__name__[len("suite_"):]
    s = Suite(name)
    def test_generator():
        def test(*args, **kwargs):
            s.add(Test(*args, **kwargs))
        origin(test)
    s.add_generator(test_generator)
    Suite.available.append(s)
    return test_generator
