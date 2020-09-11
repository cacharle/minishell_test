# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:32 by charles           #+#    #+#              #
#    Updated: 2020/09/11 14:22:47 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Minishell test",
        epilog="Make sure read README.md"
    )
    parser.add_argument(
        "-v", "--verbose", action="count",
        help="increase verbosity level (e.g -vv == 2)"
    )
    parser.add_argument(
        "-b", "--bonus", action="store_true",
        help="enable bonus tests"
    )
    parser.add_argument(
        "-n", "--no-bonus", action="store_true",
        help="disable bonus tests"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="print available test suites"
    )
    parser.add_argument(
        "-m", "--make", action="store_true",
        help="make minishell and exit"
    )
    parser.add_argument(
        "suites", nargs='*', metavar="suite",
        help="test suites/group to run"
    )
    tmp = parser.parse_args()
    if tmp.verbose is None:
        tmp.verbose = 1
    return tmp
