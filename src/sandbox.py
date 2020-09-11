# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    sandbox.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 13:48:07 by charles           #+#    #+#              #
#    Updated: 2020/09/11 19:53:13 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import glob
import shutil
import subprocess

import config


def create():
    try:
        os.mkdir(config.SANDBOX_PATH)
    except OSError:
        pass


def remove():
    try:
        shutil.rmtree(config.SANDBOX_PATH)
    except PermissionError:
        subprocess.run(["chmod", "777", *glob.glob(config.SANDBOX_PATH + "/*")], check=True)
        subprocess.run(["rm", "-rf", config.SANDBOX_PATH], check=True)
