#!/usr/bin/python3

import sys
import argparse
import shutil

import utils
import config
import suites

def main():
    try:
        suites.suite_quote()
        suites.suite_echo()
        suites.suite_redirection()
    except KeyboardInterrupt:
        shutil.rmtree(config.SANDBOX_PATH)


if __name__ == "__main__":
    available_suites_str = ", ".join(utils.available_suites)

    parser = argparse.ArgumentParser(description="Minishell test", epilog="Make sure read README.md")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print test result to stdout")
    parser.add_argument("suites", nargs='*', metavar="suite",
                        help="test suites to run (available suites: {})".format(available_suites_str))
    args = parser.parse_args()
    utils.verbose = args.verbose

    # check if selected suite is valid
    for s in args.suites:
        if s not in utils.available_suites:
            print("{}: error: `{}` isn't a valid suite, the available runned_suites are {}"
                    .format(sys.argv[0], s, available_suites_str))
            sys.exit(1)

    # update ignored runned_suites according to the selected ones (if no suite is selected, all are run)
    if len(args.suites) != 0:
        for available in utils.available_suites:
            if available not in args.suites:
                utils.ignored_suites.append(available)

    main()
    log_file = open(config.LOG_PATH, "w")
    print("Summary:")
    for suite_name, results in utils.runned_suites.items():
        print("{:15} ".format(suite_name), end="")
        pass_total = 0
        for (cmd, expected, actual, files, expected_files, actual_files) in results:
            if utils.check(expected, actual, expected_files, actual_files):
                pass_total += 1
            else:
                log_file.write(utils.diff(cmd, expected, actual, files, expected_files, actual_files))
                log_file.write("=" * 80 + "\n\n")
        print(utils.green("{:2} [PASS]".format(pass_total)), end="    ")
        print(utils.red("{:2} [FAIL]".format(len(results) - pass_total)))
    sys.exit(utils.status)
