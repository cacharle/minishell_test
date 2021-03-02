# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    helpers.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/02 14:37:38 by cacharle          #+#    #+#              #
#    Updated: 2021/03/02 17:45:28 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import contextlib

from minishell_test.config import Config


@contextlib.contextmanager
def config_context(**kwargs):
    prevs = {attr: getattr(Config, attr) for attr in kwargs.keys()}
    for attr, value in kwargs.items():
        setattr(Config, attr, value)
    try:
        yield
    finally:
        for attr, value in prevs.items():
            setattr(Config, attr, value)
