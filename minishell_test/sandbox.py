# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    sandbox.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 13:48:07 by charles           #+#    #+#              #
#    Updated: 2021/02/27 12:32:17 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import shutil
import subprocess
from contextlib import contextmanager

from minishell_test.config import Config


def create():
    """Create a new sandbox directory"""
    try:
        Config.sandbox_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass


def remove():
    """Remove the sandbox directory
       Brute force rm -rf if clean removal doesn't work due to permissions.
    """
    try:
        shutil.rmtree(Config.sandbox_dir)
    except PermissionError:
        subprocess.run(["chmod", "777", *Config.sandbox_dir.glob("*")], check=True)
        shutil.rmtree(Config.sandbox_dir)
    except FileNotFoundError:
        pass


@contextmanager
def context():
    """Sandbox context manager"""
    create()
    try:
        yield
    finally:
        remove()
