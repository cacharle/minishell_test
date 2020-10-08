# minishell test

Test for the minishell project of school 42.

![preview](preview.gif)

## Usage

The default path to your project is `..` but you can change it the the [configuration](src/config.py).

```sh
$ ./run  # run all tests

$ ./run --help
usage: run [-h] [-k] [-x] [-r BEGIN END] [--show-range] [-v] [-b] [-n] [-l]
           [-m] [-p]
           [suite [suite ...]]

Minishell test

positional arguments:
  suite                 Test suites/group to run. It tries to be smart and
                        autocomplete the suite name (e.g ./run int -> ./run
                        preprocess/interpolation)

optional arguments:
  -h, --help            show this help message and exit
  -k, --check-leaks     Run valgrind on tests (disable usual comparison with
                        bash)
  -x, --exit-first      Exit on first fail
  -r BEGIN END, --range BEGIN END
                        Range of test index to run (imply --show-index)
  --show-range          Show test index (useful with --range)
  -v, --verbose         Increase verbosity level (e.g -vv == 2)
  -b, --bonus           Enable bonus tests
  -n, --no-bonus        Disable bonus tests
  -l, --list            Print available test suites
  -m, --make            Make minishell and exit
  -p, --pager           After running the test, display the result in a pager
                        of your choice
```

## Test compatibility

Your executable **must** support the `-c` option which allow to pass command as string.

```sh
$ bash -c 'echo bonjour je suis'
bonjour je suis
$ ./minishell -c 'echo bonjour je suis'
bonjour je suis

$ bash -c 'ls'
README.md test.sh
$ ./minishell -c 'ls'
README.md test.sh
```

This allows you to set the prompt to whatever you want.

This test works with python >= 3.5.

## Bonus

Their is 3 different method to enable the bonus tests:

* Force the bonus tests with `./run -b`
* Change the `BONUS` variable in [config.py](src/config.py) to True
* Set the environment variable `MINISHELL_TEST_BONUS` to `yes`  
  (e.g `echo 'export MINISHELL_TEST_BONUS=yes' >> ~/.zshrc`)

## Memory leaks

`./run -k`, checkout the `--show-range`, `--range` and `-x` options to help
to select the tests to run since valgrind is really slow.

## Custom syntax error message

If you don't want to copy bash syntax error message,
you can set the environment variable `MINISHELL_TEST_DONT_CHECK_ERROR_MESSAGE` to `yes`.  
It will still test your exit status code but will discard any output on error tests.

## Linux

The tester will try to convert to output/status code of bash on Linux to the one on Mac.

---

## Add new tests

### Add individual test

In your suite function you can use the `test` function. With the following arguments:

1. Command to be tested (output and status will be compared to bash)
2. A command to setup the sandbox directory where the tested command will be run
3. List of files to watch (the content of each file will be compared)

```python
test("echo bonjour je suis")                                  # simple command
test("cat < somefile", setup="echo file content > somefile")  # setup
test("ls > somefile", setup="", files=["somefile"])           # watch a file
test("echo $A", exports={"A": "a"})                           # export variables in the environment

test("cat < somefile > otherfile",
     setup="echo file content > somefile",
     files=["otherfile"])
```

### Add Suite

A test suite is a group of related tests.

```python
@suite()  # @suite(bonus=True) if it's a bonus suite
def suite_yoursuitename(test):
    test(...)
    test(...)
    test(...)
```
