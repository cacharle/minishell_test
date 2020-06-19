#!/usr/bin/python3

import os
import sys
import shutil

import config
from args import parse_args
from suite import Suite
import suites.builtin
import suites.suites
import suites.operation
import suites.parenthesis

def main():
    if not os.path.exists(config.EXECUTABLES_PATH):
        os.mkdir(config.EXECUTABLES_PATH)
    for cmd in config.AVAILABLE_COMMANDS:
        shutil.copy(os.path.join("/usr/bin", cmd),  # search whole PATH
                    os.path.join(config.EXECUTABLES_PATH, cmd))

    args = parse_args()
    if args.list:
        print("The available suites are:")
        print('\n'.join([" - " + s.name for s in Suite.available]))
        sys.exit(0)

    config.VERBOSE_LEVEL = args.verbose
    Suite.setup(args.suites)
    try:
        Suite.run_all()
    except KeyboardInterrupt:
        shutil.rmtree(config.SANDBOX_PATH)

    Suite.summarize()
    Suite.save_log()
    print("See", config.LOG_PATH, "for more information")


if __name__ == "__main__":
    main()
