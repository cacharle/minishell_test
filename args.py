# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:32 by charles           #+#    #+#              #
#    Updated: 2020/09/10 13:52:37 by charles          ###   ########.fr        #
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
        "-b", "--build", action="store_true",
        help="build minishell and exit"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="print available test suites"
    )
    parser.add_argument(
        "suites", nargs='*', metavar="suite",
        help="test suites to run (-h for more information)"
    )
    tmp = parser.parse_args()
    if tmp.verbose is None:
        tmp.verbose = 1
    return tmp
