# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    sandbox.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 13:48:07 by charles           #+#    #+#              #
#    Updated: 2020/09/11 20:25:38 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import glob
import shutil
import subprocess

import config


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
