def parse_args():
    parser = argparse.ArgumentParser(description="Minishell test", epilog="Make sure read README.md")
    parser.add_argument("-v", "--verbose", action="store_true", help="print test result to stdout")
    parser.add_argument("-g", "--generate", type=int, help="number of new random test to generate")
    parser.add_argument("-l", "--list", action="store_true", help="print available test suites")
    parser.add_argument("suites", nargs='*', metavar="suite",
                        help="test suites to run (available suites: {})".format(available_suites_str))
    return parser.parse_args()

def handle_args():
    # utils.verbose = args.verbose

    # check if selected suite is valid
    for s in args.suites:
        if s not in utils.available_suites:
            print("{}: error: the `{}` suite doesn't exist, try {} --list"
                    .format(sys.argv[0], s, sys.argv[0]))
            sys.exit(1)

    # update ignored runned_suites according to the selected ones (if no suite is selected, all are run)
    if len(args.suites) != 0:
        for available in State.available_suites:
            if available not in args.suites:
                utils.ignored_suites.append(available)
