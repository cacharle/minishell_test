# minishell test [![Build Status](https://api.travis-ci.com/cacharle/minishell_test.svg?branch=master)](https://travis-ci.com/cacharle/minishell_test)

Test for the minishell project of school 42.

![preview](preview.gif)

## Usage

The default path to your project is `../minishell` but you can change it the the [configuration](src/config.py).

```
$ ./run  # run all tests

$ ./run --help
usage: run [-h] [-k] [-x] [-r BEGIN END] [--show-range] [-v] [-b] [-n] [-l]
           [-m] [-p]
           [suite [suite ...]]

___  ____       _     _          _ _   _            _
|  \/  (_)     (_)   | |        | | | | |          | |
| .  . |_ _ __  _ ___| |__   ___| | | | |_ ___  ___| |_
| |\/| | | '_ \| / __| '_ \ / _ \ | | | __/ _ \/ __| __|
| |  | | | | | | \__ \ | | |  __/ | | | ||  __/\__ \ |_
\_|  |_/_|_| |_|_|___/_| |_|\___|_|_|  \__\___||___/\__|

positional arguments:
  suite                 Test suites/group to run.
                        It tries to be smart and autocomplete the suite name
                        (e.g ./run int -> ./run preprocess/interpolation)

optional arguments:
  -h, --help            show this help message and exit
  -k, --check-leaks     Run valgrind on tests (disable usual comparison with bash)
  -x, --exit-first      Exit on first fail
  -r BEGIN END, --range BEGIN END
                        Range of test index to run (imply --show-index)
  --show-range          Show test index (useful with --range)
  -v, --verbose         Increase verbosity level (e.g -vv == 2)
  -b, --bonus           Enable bonus tests
  -n, --no-bonus        Disable bonus tests
  -l, --list            Print available test suites
  -m, --make            Make minishell and exit
  -p, --pager           After running the test, display the result in a pager of your choice

Signal handling is not tested
There is a commented glob suite in src/suites/preprocess.py.
Good luck handling `*'.*'`.
```

## Test compatibility

Your executable **must** support the `-c` option which allow to pass command as string.

```command
$ bash -c 'echo bonjour je suis'
bonjour je suis
$ ./minishell -c 'echo bonjour je suis'
bonjour je suis

$ bash -c 'ls'
README.md test.sh
$ ./minishell -c 'ls'
README.md test.sh
```

With this setup `argv[2]` is what you would usually get in `line` from `get_next_line`.  
This allows you to set the prompt to whatever you want.

**This test works with Python3.6 or higher.**

### Environement variables

My test only gives the `PATH=minishell_test/bin` and `TERM=xterm-256color` environment variables to your minishell.  
**Please check that your project still work with those settings before messaging me on Slack or creating an issue**.  
You can test this quickly with the [try](try) script (e.g `./try 'echo bonjour | cat -e'`).

## Bonus

Their is 3 different method to enable the bonus tests:

* Force the bonus tests with `./run -b`
* Change the `BONUS` variable in [config.py](src/config.py) to True
* Set the environment variable `MINISHELL_TEST_BONUS` to `yes`  
  (e.g `echo 'export MINISHELL_TEST_BONUS=yes' >> ~/.zshrc`)

## Memory leaks

`./run -k`, checkout the `--show-range`, `--range` and `-x` options to help
to select the tests to run since valgrind is really slow.

## Don't check error messages

If you don't want to copy bash syntax error message,
you can set the environment variable `MINISHELL_TEST_DONT_CHECK_ERROR_MESSAGE` to `yes`.  
It will still test your exit status code but will discard any output on error tests.

## Linux

The tester will try to convert to output/status code of bash on Linux to the one on Mac.

---

## Add new tests

You can find the suites in the [src/suites](src/suites) directory.

### Add individual test

In your suite function you can use the `test` function. With the following arguments:

1. Command to be tested (output and status will be compared to bash)
2. A command to setup the sandbox directory where the tested command will be run
3. List of files to watch (the content of each file will be compared)

```python
test("echo bonjour je suis")                                  # simple command
test("cat < somefile", setup="echo file content > somefile")  # setup
test("ls > somefile", setup="", files=["somefile"])           # watch a file
test("echo $A", exports={"A": "a"})                           # export variables
                                                              # in the environment
test("echo bonjour", hook=lambda s: s.replace("o", "a"))      # pass the shell output
                                                              # through a hook function

test("cat < somefile > otherfile",
     setup="echo file content > somefile",
     files=["otherfile"])
```

### Add Suite

A test suite is a group of related tests.

```python
@suite()  # @suite(bonus=True) if it's a bonus suite
def suite_yoursuitename(test):
    """ a description of the suite """
    test(...)
    test(...)
    test(...)
```

---

## Wildcard (or glob)

There is a commented glob suite in [src/suites/preprocess.py](src/suites/preprocess.py).
Good luck handling `*'.*'`.
