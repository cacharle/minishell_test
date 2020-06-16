import os
import sys
import subprocess
import shutil

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
            setup_status = subprocess.run(setup, shell=True, cwd=config.SANDBOX_PATH, check=True)
        except subprocess.CalledProcessError as e:
            print("Error: `{}` setup command failed for `{}`\n\twith '{}'"
                  .format(setup, cmd, e.stderr.decode().strip()))
            sys.exit(1)

    # TODO: add timeout
    # https://docs.python.org/3/library/subprocess.html#using-the-subprocess-module
    process_status = subprocess.run([program, "-c", cmd],
                                    stderr=subprocess.STDOUT,
                                    stdout=subprocess.PIPE,
                                    cwd=config.SANDBOX_PATH)
    output = process_status.stdout.decode()

    output_files = []
    for file_name in files:
        try:
            with open(os.path.join(config.SANDBOX_PATH, file_name), "rb") as f:
                output_files.append(f.read().decode())
        except FileNotFoundError as e:
            output_files.append(None)

    shutil.rmtree(config.SANDBOX_PATH)
    return (output, output_files)

status = 0
ignored_suites = []
runned_suites = {}
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

    if runned_suites.get(current_suite) is None:
        runned_suites[current_suite] = []
    runned_suites[current_suite].append((cmd, expected, actual, files, expected_files, actual_files))

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
