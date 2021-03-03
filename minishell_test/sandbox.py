# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    sandbox.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 13:48:07 by charles           #+#    #+#              #
#    Updated: 2021/03/03 09:15:11 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path

from minishell_test.config import Config


def create():
    """Create a new sandbox directory"""
    Config.sandbox_dir.mkdir(parents=True, exist_ok=True)


def remove():
    """Remove the sandbox directory
       Brute force rm -rf if clean removal doesn't work due to permissions.
    """
    try:
        shutil.rmtree(Config.sandbox_dir)
    except PermissionError:
        subprocess.run(["chmod", "-R", "777", Config.sandbox_dir], check=True)
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
