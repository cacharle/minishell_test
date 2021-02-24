#!/usr/bin/env python3

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

import minishell_test.config as config
import minishell_test.sandbox as sandbox
from minishell_test.args import parse_args
from minishell_test.suite.suite import Suite, SuiteException
from minishell_test.suites import *  # noqa: F403,F401


def main(argv=None):
    args = parse_args()
    if args.list:
        Suite.list()
        sys.exit(0)

    config.MINISHELL_DIR = args.path
    config.MINISHELL_PATH = os.path.abspath(
        os.path.join(config.MINISHELL_DIR, config.MINISHELL_EXEC)
    )
    config.VALGRIND_CMD[-1] = config.MINISHELL_PATH

    if config.MINISHELL_MAKE or args.make:
        try:
            print("{:=^{width}}".format("MAKE", width=config.TERM_COLS))
            subprocess.run(["make", "--no-print-directory", "-C", config.MINISHELL_DIR],
                           check=True,
                           env={"MINISHELL_TEST_FLAGS": "-DMINISHELL_TEST", **os.environ})
            print("=" * config.TERM_COLS)
        except subprocess.CalledProcessError:
            sys.exit(1)
        if args.make:
            sys.exit(0)

    if not os.path.exists(config.EXECUTABLES_PATH):
        os.mkdir(config.EXECUTABLES_PATH)
        for cmd in config.AVAILABLE_COMMANDS:
            cmd_path = distutils.spawn.find_executable(cmd)
            if cmd_path is None:
                raise RuntimeError
            shutil.copy(cmd_path,
                        os.path.join(config.EXECUTABLES_PATH, cmd))

    reference_args = os.environ.get("MINISHELL_TEST_ARGS")
    if reference_args is not None:
        config.REFERENCE_ARGS.extend(reference_args.split(','))

    pager = os.environ.get("MINISHELL_TEST_PAGER")
    if pager is not None:
        config.PAGER = pager

    config.VERBOSE_LEVEL = args.verbose
    if args.bonus or os.environ.get("MINISHELL_TEST_BONUS") == "yes":
        config.BONUS = True
    if args.no_bonus:
        config.BONUS = False
    config.EXIT_FIRST = args.exit_first
    config.CHECK_LEAKS = args.check_leaks
    config.RANGE = args.range
    config.SHOW_RANGE = args.show_range
    if config.RANGE is not None or config.CHECK_LEAKS:
        config.SHOW_RANGE = True

    try:
        Suite.setup(args.suites)
    except SuiteException as e:
        print(e)
        sys.exit(1)
    try:
        Suite.run_all()
    except KeyboardInterrupt:
        pass
    finally:
        sandbox.remove()

    Suite.summarize()
    Suite.save_log()
    print("See", config.LOG_PATH, "for more information")
    if config.CHECK_LEAKS:
        print("HELP: Valgrind is really slow the -x and --range options could be useful"
              " (./run -h for more details)")

    if args.pager:
        subprocess.run([config.PAGER, config.LOG_PATH])


if __name__ == "__main__":
    main()
