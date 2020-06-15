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

def green(s):
    return COLOR_RED + s + COLOR_CLOSE

def red(s):
    return COLOR_GREEN + s + COLOR_CLOSE

def diff(cmd, expected, actual, color=False):
    ret = """
WITH: {}
STATUS: TODO
{color_expected}----------------------------------------EXPECTED--------------------------------{color_close}
{}
{color_actual}----------------------------------------ACTUAL----------------------------------{color_close}
{}
================================================================================

"""
    colors = {}
    if color:
        colors = {
            "color_expected": COLOR_GREEN,
            "color_actual": COLOR_RED,
            "color_close": COLOR_CLOSE
        }
    else:
        colors = {
            "color_expected": "",
            "color_actual": "",
            "color_close": ""
        }
    return ret.format(cmd, expected, actual, **colors)


def run_sandboxed(program: str, cmd: str) -> str:
    try:
        os.mkdir(config.SANDBOX_PATH)
    except OSError:
        pass
    # os.system(self.setup_cmd)

    # TODO: add timeout
    # https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module
    process_status = subprocess.run([program, "-c", cmd],
                                    text=True,
                                    stderr=subprocess.STDOUT,
                                    stdout=subprocess.PIPE,
                                    cwd=config.SANDBOX_PATH)

    output = process_status.stdout

    shutil.rmtree(config.SANDBOX_PATH)
    return output


def put_marker(passed):
    if passed:
        sys.stdout.write(green(config.PASS_MARKER))
    else:
        sys.stdout.write(red(config.FAIL_MARKER))
    sys.stdout.flush()


status = 0
ignored_suites = []
suites = {}
current_suite = "default"
verbose = False

def test(cmd, setup = None, *files):
    if current_suite in ignored_suites:
        return
    expected = run_sandboxed(config.REFERENCE_SHELL_PATH, cmd)
    actual = run_sandboxed(config.MINISHELL_PATH, cmd)

    global status
    if actual != expected:
        status = 1
    if not verbose:
        put_marker(actual == expected)
    elif actual != expected:
        print(diff(cmd, expected, actual, True))

    if suites.get(current_suite) is None:
        suites[current_suite] = []
    suites[current_suite].append((cmd, expected, actual))

available_suites = []

def suite(origin):
    name = origin.__name__[len("suite_"):]
    available_suites.append(name)
    def f():
        global current_suite
        current_suite = name
        print(current_suite, end=": ")
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
    test("echo " + config.LOREM)

    test("echo -n bonjour")
    test("echo -n lalalala lalalalal alalalalal alalalala")
    test("echo -n " + config.LOREM)


def main():
    suite_quote()
    suite_echo()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Minishell test", epilog="Make sure read README.md")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print test result to stdout")
    parser.add_argument("suites", nargs='*', metavar="suite",
                        help="test suites to run (available suites: {})".format(", ".join(available_suites)))
    args = parser.parse_args()
    verbose = args.verbose

    main()
    log_file = open(config.LOG_PATH, "w")
    print()
    for suite_name, results in suites.items():
        print(suite_name, end=":    ")
        pass_total = 0
        for (cmd, expected, actual) in results:
            if expected == actual:
                pass_total += 1
            else:
                log_file.write(diff(cmd, expected, actual))
        print(green(str(pass_total)), green(config.PASS_MARKER), end="    ")
        print(red(str(len(results) - pass_total)), red(config.FAIL_MARKER))
