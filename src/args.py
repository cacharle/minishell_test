# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:32 by charles           #+#    #+#              #
#    Updated: 2021/01/11 22:20:16 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import argparse
import textwrap


def parse_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description=textwrap.dedent(r"""
            ___  ____       _     _          _ _   _            _
            |  \/  (_)     (_)   | |        | | | | |          | |
            | .  . |_ _ __  _ ___| |__   ___| | | | |_ ___  ___| |_
            | |\/| | | '_ \| / __| '_ \ / _ \ | | | __/ _ \/ __| __|
            | |  | | | | | | \__ \ | | |  __/ | | | ||  __/\__ \ |_
            \_|  |_/_|_| |_|_|___/_| |_|\___|_|_|  \__\___||___/\__|
        """),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent("""\
            Signal handling is not tested
            There is a commented glob suite in src/suites/preprocess.py.
            Good luck handling `*'.*'`.
        """)
    )
    parser.add_argument(
        "-k", "--check-leaks", action="store_true",
        help="Run valgrind on tests (disable usual comparison with bash)"
    )
    parser.add_argument(
        "-r", "--range", nargs=2, type=int, metavar=("BEGIN", "END"),
        help="Range of test index to run (imply --show-index)"
    )
    parser.add_argument(
        "--show-range", action="store_true",
        help="Show test index (useful with --range)"
    )
    parser.add_argument(
        "-x", "--exit-first", action="store_true",
        help="Exit on first fail"
    )
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
        "-g", "--pager", action="store_true",
        help="After running the test, display the result in a pager of your choice"
    )
    parser.add_argument(
        "suites", nargs='*', metavar="suite",
        help=textwrap.dedent("""\
            Test suites/group to run.
            It tries to be smart and autocomplete the suite name
            (e.g ./run int -> ./run preprocess/interpolation)
        """)
    )
    tmp = parser.parse_args()
    if tmp.verbose is None:
        tmp.verbose = 1
    return tmp
