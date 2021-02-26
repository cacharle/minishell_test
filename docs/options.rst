Command line Options
====================

.. code-block:: txt

    usage: minishell_test [-h] [-p PATH] [-l] [-t COMMAND] [-k] [-r BEGIN END]
                          [--show-range] [-x] [-v] [-b] [-n] [-m] [-g]
                          [suite ...]

.. program:: minishell_test

.. option:: suite

   Test suites/group to run.
   It tries to be smart and autocomplete the suite name
   (e.g ./run int -> ./run preprocess/interpolation)


.. option:: -h, --help

   show this help message and exit

.. option:: -p <PATH>, --path <PATH>

   Path to minishell directory

.. option:: -l, --list

   Print available test suites

.. option:: -t <COMMAND>, --try <COMMAND>

   Run a custom command like this test would
   (the only environment variable passed to your executable are TERM and PATH)

.. option:: -k, --check-leaks

   Run valgrind on tests (disable usual comparison with bash)

.. option:: -r <BEGIN> <END>, --range <BEGIN> <END>

    Range of test index to run (imply --show-index)

.. option:: --show-range

   Show test index (useful with --range)

.. option:: -x, --exit-first

    Exit on first fail

.. option:: -v, --verbose

    Increase verbosity level (e.g -vv == 2)

.. option:: -b, --bonus

    Enable bonus tests

.. option:: -n, --no-bonus

    Disable bonus tests

.. option:: -m, --make

    Make minishell and exit

.. option:: -g, --pager

    After running the test, display the result in a pager of your choice

