#!/usr/bin/python3

import os
import sys
import subprocess
import shutil

import config


def green(s):
    return "\033[32m{}\033[0m".format(s)


def red(s):
    return "\033[31m{}\033[0m".format(s)


def run_sandboxed(program: str, cmd: str) -> str:
    try:
        os.mkdir(config.SANDBOX_PATH)
    except OSError:
        pass
    # os.system(self.setup_cmd)
    current_dir = os.getcwd()
    os.chdir(config.SANDBOX_PATH)
    output = ""
    try:
        output = subprocess.check_output([program, "-c", cmd], stderr=subprocess.STDOUT)
    except:
        pass

    os.chdir(current_dir)
    shutil.rmtree(config.SANDBOX_PATH)
    return output


ignored_suites = []
suites = {}
current_suite = "default"

def test(cmd, setup = None, *files):
    if current_suite in ignored_suites:
        return
    expected = run_sandboxed(config.REFERENCE_SHELL_PATH, cmd)
    actual = run_sandboxed(os.path.join(config.MINISHELL_DIR, config.MINISHELL_EXEC), cmd)

    if actual != expected:
        sys.stdout.write(red(config.FAIL_MARKER))
    else:
        sys.stdout.write(green(config.PASS_MARKER))
    sys.stdout.flush()

    if suites.get(current_suite) is None:
        suites[current_suite] = []
    suites[current_suite].append((expected, actual))


def test_echo():
    test("echo bonjour")
    test("echo je suis charles")
    test("echo je   suis    charles")

    test("'echo' 'bonjour'")
    test("'echo' 'je' 'suis' 'charles'")
    test("'echo' 'je'   'suis'    'charles'")

    test('"echo" "bonjour"')
    test('"echo" "je" "suis" "charles"')
    test('"echo" "je"   "suis"    "charles"')



def main():
    test_echo()

if __name__ == "__main__":
    main()
