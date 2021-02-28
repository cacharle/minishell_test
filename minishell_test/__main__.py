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

from minishell_test.config import Config
from minishell_test import sandbox
from minishell_test.args import parse_args
from minishell_test.suite.suite import Suite, SuiteException
from minishell_test.suites import *  # noqa: F403,F401
from minishell_test.test import Test


def main(argv=None):
    args = parse_args(sys.argv[1:])
    Config.init(args)

    if args.list:
        Suite.list()
        sys.exit(0)

    # running ``make`` in minishell directory
    if Config.make or args.make:
        print("{:=^{width}}".format("MAKE", width=Config.term_cols))
        try:
            subprocess.run(
                ["make", *Config.make_args, "--no-print-directory", "-C", Config.minishell_dir],
                check=True,
                env=os.environ,
            )
        except subprocess.CalledProcessError:
            sys.exit(1)
        print("=" * Config.term_cols)
        if args.make:
            sys.exit(0)

    # setup available commands
    if not Config.shell_available_commands_dir.exists():
        Config.shell_available_commands_dir.mkdir(parents=True, exist_ok=True)
    for cmd in Config.shell_available_commands:
        copied_path = Config.shell_available_commands_dir / cmd
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
    print("See", Config.log_path, "for more information")
    if Config.check_leaks:
        print("HELP: Valgrind is really slow the -x and --range options could be useful"
              " ({} -h for more details)".format(sys.argv[0]))

    if Config.pager:
        # TODO {} replaced by filename in pager config var
        subprocess.run([Config.pager_prog, Config.log_path])


if __name__ == "__main__":
    main()
