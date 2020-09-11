#!/usr/bin/python3

# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 15:11:52 by charles           #+#    #+#              #
#    Updated: 2020/07/15 15:11:52 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import shutil
import distutils.spawn
import subprocess

import config
import sandbox
from args import parse_args
from suite import Suite
from suites import *

def main():
    args = parse_args()
    if args.list:
        print("The available suites are:")
        print('\n'.join([" - " + s.name for s in Suite.available]))
        print("Groups:")
        print('\n'.join([" - " + ', '.join(s.groups) for s in Suite.available]))
        sys.exit(0)

    if config.MINISHELL_MAKE or args.make:
        try:
            subprocess.run(["make", "-C", config.MINISHELL_DIR], check=True)
        except subprocess.CalledProcessError:
            sys.exit(1)
        if args.make:
            sys.exit(0)
    if os.path.exists(config.EXECUTABLES_PATH):
        shutil.rmtree(config.EXECUTABLES_PATH)
    os.mkdir(config.EXECUTABLES_PATH)
    for cmd in config.AVAILABLE_COMMANDS:
        shutil.copy(distutils.spawn.find_executable(cmd),  # FIXME search whole PATH
                    os.path.join(config.EXECUTABLES_PATH, cmd))


    config.VERBOSE_LEVEL = args.verbose
    if args.bonus:
        config.BONUS = True
    if args.no_bonus:
        config.BONUS = False
    Suite.setup(args.suites)
    try:
        Suite.run_all()
    except KeyboardInterrupt:
        sandbox.remove()

    Suite.summarize()
    Suite.save_log()
    print("See", config.LOG_PATH, "for more information")


if __name__ == "__main__":
    main()
