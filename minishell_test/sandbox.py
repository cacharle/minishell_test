# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    sandbox.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 13:48:07 by charles           #+#    #+#              #
#    Updated: 2021/02/27 12:05:35 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import shutil
import subprocess
from contextlib import contextmanager

from minishell_test import config


def create():
    """Create a new sandbox directory"""
    try:
        config.SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass


def remove():
    """Remove the sandbox directory
       Brute force rm -rf if clean removal doesn't work due to permissions.
    """
    try:
        shutil.rmtree(config.SANDBOX_DIR)
    except PermissionError:
        subprocess.run(["chmod", "777", *config.SANDBOX_DIR.glob("*")], check=True)
        shutil.rmtree(config.SANDBOX_DIR)
    except FileNotFoundError:
        pass


@contextmanager
def context():
    """Sandbox context manager"""
    create()
    yield
    remove()
