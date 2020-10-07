# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:32 by charles           #+#    #+#              #
#    Updated: 2020/09/27 11:08:49 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import argparse


def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description="Minishell test")
    parser.add_argument(
        "-v", "--verbose", action="count",
        help="Increase verbosity level (e.g -vv == 2)"
    )
    parser.add_argument(
        "-b", "--bonus", action="store_true",
        help="Enable bonus tests"
    )
    parser.add_argument(
        "-n", "--no-bonus", action="store_true",
        help="Disable bonus tests"
    )
    parser.add_argument(
        "-l", "--list", action="store_true",
        help="Print available test suites"
    )
    parser.add_argument(
        "-m", "--make", action="store_true",
        help="Make minishell and exit"
    )
    parser.add_argument(
        "-p", "--pager", action="store_true",
        help="After running the test, display the result in a pager of your choice"
    )
    parser.add_argument(
        "suites", nargs='*', metavar="suite",
        help="Test suites/group to run. "
             "It tries to be smart and autocomplete the suite name "
             "(e.g ./run int -> ./run preprocess/interpolation)"
    )
    tmp = parser.parse_args()
    if tmp.verbose is None:
        tmp.verbose = 1
    return tmp
