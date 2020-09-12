# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:32 by charles           #+#    #+#              #
#    Updated: 2020/09/12 02:21:51 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import argparse


def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description="Minishell test",
        epilog="Make sure read the README.md"
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
        help="test suites/group to run, "
             "It tries to be smart and auto complete the suite name "
             "you put in (e.g ./run int -> ./run preprocess/interpolation)"
    )
    tmp = parser.parse_args()
    if tmp.verbose is None:
        tmp.verbose = 1
    return tmp
