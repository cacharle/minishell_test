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

from minishell_test import config
from minishell_test import sandbox
from minishell_test.args import parse_args
from minishell_test.suite.suite import Suite, SuiteException
from minishell_test.suites import *  # noqa: F403,F401
from minishell_test.test import Test


def main(argv=None):
    args = parse_args()

    if args.list:
        Suite.list()
        sys.exit(0)

    # running ``make`` in minishell directory
    if config.MAKE or args.make:
        print("{:=^{width}}".format("MAKE", width=config.TERM_COLS))
        try:
            subprocess.run(
                ["make", *config.MAKE_ARGS, "--no-print-directory", "-C", config.MINISHELL_DIR],
                check=True,
                env=os.environ,
            )
        except subprocess.CalledProcessError:
            sys.exit(1)
        print("=" * config.TERM_COLS)
        if args.make:
            sys.exit(0)

    # setup available commands
    if not config.SHELL_AVAILABLE_COMMANDS_DIR.exists():
        config.SHELL_AVAILABLE_COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    for cmd in config.SHELL_AVAILABLE_COMMANDS:
        copied_path = config.SHELL_AVAILABLE_COMMANDS_DIR / cmd
        if copied_path.exists():
            continue
        cmd_path = distutils.spawn.find_executable(cmd)
        if cmd_path is None:
            raise RuntimeError(f"Command not found {cmd}")
        shutil.copy(cmd_path, copied_path)

    if args.try_cmd is not None:
        print("Output")
        print(Test.try_run(args.try_cmd))
        sys.exit(0)

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
              " ({} -h for more details)".format(sys.argv[0]))

    if config.PAGER:
        # TODO {} replaced by filename in pager config var
        subprocess.run([config.PAGER_PROG, config.LOG_PATH])


if __name__ == "__main__":
    main()
