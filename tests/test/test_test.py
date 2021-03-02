# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_test.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/02 18:48:57 by cacharle          #+#    #+#              #
#    Updated: 2021/03/02 18:50:07 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #


import pytest

from minishell_test.config import Config
from minishell_test import colors

from minishell_test.test.result import BaseResult, Result, LeakResult, LeakResultException
from minishell_test.test.captured import CapturedCommand, CapturedTimeout

from tests.helpers import config_context


colors.disable()
Config.init([])

class TestTest:
    def test_run(self):
        pass
