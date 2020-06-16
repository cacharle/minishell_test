#!/usr/bin/python3

import os
import sys
import subprocess
import shutil
import argparse

import config

COLOR_RED = "\033[32m"
COLOR_GREEN = "\033[31m"
COLOR_CLOSE = "\033[0m"

def green(s: str) -> str:
    return COLOR_RED + s + COLOR_CLOSE

def red(s: str) -> str:
    return COLOR_GREEN + s + COLOR_CLOSE

def expected_line(color: bool) -> str:
    s = "----------------------------------------EXPECTED--------------------------------"
    return COLOR_GREEN + s + COLOR_CLOSE if color else s

def actual_line(color: bool) -> str:
    s = "----------------------------------------ACTUAL----------------------------------"
    return COLOR_RED + s + COLOR_CLOSE if color else s


def diff_file(file_name: str, expected: str, actual: str, color: bool = False) -> str:
    return """\
FILE {}
{}
{}\
{}
{}\
""".format(file_name, expected_line(color), expected, actual_line(color),
           "FROM TEST: File not created\n" if actual is None else actual)

def diff_output(cmd: str, expected: str, actual: str, color: bool = False) -> str:
    return """\
WITH: {}
STATUS: TODO
{}
{}\
{}
{}\
""".format(cmd, expected_line(color), expected, actual_line(color), actual)

def diff(cmd: str, expected: str, actual: str,
        files: [str], expected_files: [str], actual_files: [str],
        color: bool = False) -> str:
    s = ""
    if expected != actual:
        s += diff_output(cmd, expected, actual, color)

    for file_name, e, a in zip(files, expected_files, actual_files):
        if a != e:
            s += "-" * 80 + "\n" + diff_file(file_name, e, a, color)
    return s


def put_result(passed: bool, cmd: str):
    if len(cmd) > 70:
        cmd = cmd[:67] + "..."

    if passed:
        print(green("{:74} [PASS]".format(cmd)))
    else:
        print(red("{:74} [FAIL]".format(cmd)))



def run_sandboxed(program: str, cmd: str, setup: str = None, files: [str] = []) -> str:
    """ run the command in a sandbox environment, return the output (stdout and stderr) of it """

    try:
        os.mkdir(config.SANDBOX_PATH)
    except OSError:
        pass
    if setup is not None:
        try:
            setup_status = subprocess.run(setup, shell=True, cwd=config.SANDBOX_PATH, check=True, text=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print("Error: `{}` setup command failed for `{}`\n\twith '{}'".format(setup, cmd, e.stderr.strip()))
            sys.exit(1)

    # TODO: add timeout
    # https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module
    process_status = subprocess.run([program, "-c", cmd],
                                    text=True,
                                    stderr=subprocess.STDOUT,
                                    stdout=subprocess.PIPE,
                                    cwd=config.SANDBOX_PATH)
    output = process_status.stdout

    output_files = []
    for file_name in files:
        try:
            with open(os.path.join(config.SANDBOX_PATH, file_name), "r") as f:
                output_files.append(f.read())
        except FileNotFoundError as e:
            output_files.append(None)

    shutil.rmtree(config.SANDBOX_PATH)
    return (output, output_files)

status = 0
ignored_suites = []
suites = {}
current_suite = "default"
verbose = False

def check(expected: str, actual: str, expected_files: [str], actual_files: [str]) -> bool:
    return actual == expected and all([a == e for a, e in zip(actual_files, expected_files)])

def test(cmd: str, setup: str = None, files: [str] = []):
    """ get expected and actual strings, compare them and push them to the suites result """

    (expected, expected_files) = run_sandboxed(config.REFERENCE_SHELL_PATH, cmd, setup, files)
    (actual, actual_files) = run_sandboxed(config.MINISHELL_PATH, cmd, setup, files)

    passed = check(expected, actual, expected_files, actual_files)
    global status
    if not passed:
        status = 1
    if not verbose:
        put_result(actual == expected, cmd)
    elif not passed:
        print(diff(cmd, expected, actual, files, expected_files, actual_files, color=True))

    if suites.get(current_suite) is None:
        suites[current_suite] = []
    suites[current_suite].append((cmd, expected, actual, files, expected_files, actual_files))

available_suites = []

def suite(origin):
    """ decorator for a suite function (fmt: suite_[name])
        update the current_suite global and print it before the suite execution
    """

    name = origin.__name__[len("suite_"):]
    available_suites.append(name)
    def f():
        if name in ignored_suites:
            return
        global current_suite
        current_suite = name.upper()
        print("{} {:#<41}".format("#" * 39, current_suite + " "))
        origin()
        print()
    return f

@suite
def suite_quote():
    test("'echo' 'bonjour'")
    test("'echo' 'je' 'suis' 'charles'")

    test('"echo" "bonjour"')
    test('"echo" "je" "suis" "charles"')

    test('echo je\'suis\'"charles"')
    test('echo "je"suis\'charles\'')
    test('echo \'je\'"suis"charles')

    test('echo "\\""')
    test('echo "\\$"')
    test('echo "\\\\"')

@suite
def suite_echo():
    test("echo bonjour")
    test("echo lalalala lalalalal alalalalal alalalala")
    test("echo lalalala                lalalalal      alalalalal alalalala")
    test("echo " + config.LOREM)

    test("echo -n bonjour")
    test("echo -n lalalala lalalalal alalalalal alalalala")
    test("echo -n lalalala                lalalalal      alalalalal alalalala")
    test("echo -n " + config.LOREM)

@suite
def suite_redirection():
    test("echo bonjour > test", setup="", files=["test"])
    test("echo > test bonjour", setup="", files=["test"])
    test("> test echo bonjour", setup="", files=["test"])


def main():
    suite_quote()
    suite_echo()
    suite_redirection()


if __name__ == "__main__":
    available_suites_str = ", ".join(available_suites)

    parser = argparse.ArgumentParser(description="Minishell test", epilog="Make sure read README.md")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print test result to stdout")
    parser.add_argument("suites", nargs='*', metavar="suite",
                        help="test suites to run (available suites: {})".format(available_suites_str))
    args = parser.parse_args()
    verbose = args.verbose

    # check if selected suite is valid
    for s in args.suites:
        if s not in available_suites:
            print("{}: error: `{}` isn't a valid suite, the available suites are {}"
                    .format(sys.argv[0], s, available_suites_str))
            sys.exit(1)

    # update ignored suites according to the selected ones (if no suite is selected, all are run)
    if len(args.suites) != 0:
        for available in available_suites:
            if available not in args.suites:
                ignored_suites.append(available)

    main()
    log_file = open(config.LOG_PATH, "w")
    print("Summary:")
    for suite_name, results in suites.items():
        print("{:15} ".format(suite_name), end="")
        pass_total = 0
        for (cmd, expected, actual, files, expected_files, actual_files) in results:
            if check(expected, actual, expected_files, actual_files):
                pass_total += 1
            else:
                log_file.write(diff(cmd, expected, actual, files, expected_files, actual_files))
                log_file.write("=" * 80 + "\n\n")
        print(green("{:2} [PASS]".format(pass_total)), end="    ")
        print(red("{:2} [FAIL]".format(len(results) - pass_total)))
