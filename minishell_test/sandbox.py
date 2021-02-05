# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    sandbox.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 13:48:07 by charles           #+#    #+#              #
#    Updated: 2021/02/05 14:54:37 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import glob
import shutil
import subprocess
from contextlib import contextmanager

import minishell_test.config as config


def create():
    """Create a new sandbox directory"""
    try:
        os.mkdir(config.SANDBOX_PATH)
    except OSError:
        pass


def remove():
    """Remove the sandbox directory
       Brute force rm -rf if clean removal doesn't work due to permissions.
    """
    try:
        shutil.rmtree(config.SANDBOX_PATH)
    except PermissionError:
        subprocess.run(["chmod", "777", *glob.glob(config.SANDBOX_PATH + "/*")], check=True)
        subprocess.run(["rm", "-rf", config.SANDBOX_PATH], check=True)
    except FileNotFoundError:
        pass


@contextmanager
def context():
    """Sandbox context manager"""
    create()
    yield
    remove()
