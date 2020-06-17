import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Minishell test", epilog="Make sure read README.md")
    parser.add_argument(
        "-v", "--verbose", action="count",
        help="increase verbosity level (e.g -vv == 2)"
    )
    parser.add_argument(
        "-g", "--generate", metavar="NUMBER", type=int,
        help="number of new random test to generate"
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
        tmp.verbose = 0
    return tmp
