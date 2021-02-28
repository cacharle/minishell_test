# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:32 by charles           #+#    #+#              #
#    Updated: 2021/02/28 09:06:53 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import argparse
import textwrap


def parse_args(argv):
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(
        description="Test for the minishell project of school 42.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Made by cacharle - https://cacharle.xyz"
    )
    parser.add_argument(
        "-p", "--path",
        default=".",
        help="Path to minishell directory"
    )
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="Print available test suites"
    )
    parser.add_argument(
        "-t", "--try",
        metavar="COMMAND",
        dest='try_cmd',
        help=textwrap.dedent("""\
            Run a custom command like this test would
            (the only environment variable passed to your executable are TERM and PATH)
        """)
    )
    parser.add_argument(
        "-k", "--check-leaks",
        action="store_true",
        help="Run valgrind on tests (disable usual comparison with bash)"
    )
    parser.add_argument(
        "-r", "--range",
        nargs=2,
        type=int,
        metavar=("BEGIN", "END"),
        help="Range of test index to run (imply --show-index)"
    )
    parser.add_argument(
        "--show-range",
        action="store_true",
        help="Show test index (useful with --range)"
    )
    parser.add_argument(
        "-x", "--exit-first",
        action="store_true",
        help="Exit on first fail"
    )
    parser.add_argument(
        "-m", "--make",
        action="store_true",
        help="Make minishell and exit"
    )
    parser.add_argument(
        "-g", "--pager",
        action="store_true",
        help="After running the test, display the result in a pager of your choice"
    )
    parser.add_argument(
        "suites",
        nargs='*',
        metavar="SUITE",
        help=textwrap.dedent("""\
            Test suites/group to run.
            It tries to be smart and autocomplete the suite name
            (e.g ./run int -> ./run preprocess/interpolation)
        """)
    )
    return parser.parse_args(argv)
