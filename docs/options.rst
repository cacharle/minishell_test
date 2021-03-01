Command line Options
====================

.. command-output:: minishell_test --help
   :ellipsis: 3

.. program:: minishell_test

.. option:: suite

   | Select the test suites/group to run.
   | It tries to be smart and autocomplete the suite name,
   | e.g ``$ minishell_test int`` -> ``$ minishell_test preprocess/interpolation``.
   | See :option:`--list` to list the available suites.

   .. code-block::

      $ minishell_test -p ../../minishell inter
      ########################### preprocess/interpolation ###########################
      [EXPORTS TEST='bonjour'] echo $TEST                                       [PASS]
      [EXPORTS TEST='bonjour'] echo $TES                                        [PASS]
      [EXPORTS TEST='bonjour'] echo $TEST_                                      [PASS]
      [EXPORTS TEST='bonjour'] echo "|$TEST|"                                   [PASS]
      [EXPORTS TEST='bonjour'] echo "|$TES|"                                    [PASS]
      [EXPORTS TEST='bonjour'] echo "|$TEST_|"                                  [PASS]
      [EXPORTS TEST='bonjour'] echo '|$TEST|'                                   [PASS]
      [EXPORTS TEST='bonjour'] echo '|$TES|'                                    [PASS]
      [EXPORTS TEST='bonjour'] echo '|$TEST_|'                                  [PASS]
      [EXPORTS A='foo' B='bar' C='baz'] echo $A$B$C                             [PASS]
      [EXPORTS A='foo' B='bar' C='baz'] echo "$A$B$C"                           [PASS]
      [EXPORTS A='foo' B='bar' C='baz'] echo '$A$B$C'                           [PASS]
      [EXPORTS A='foo' B='bar' C='baz'] echo $A,$B,$C                           [PASS]
      [EXPORTS A='foo' B='bar' C='baz'] echo "$A,$B,$C"                         [PASS]
      [EXPORTS A='foo' B='bar' C='baz'] echo '$A,$B,$C'                         [PASS]
      ...

.. option:: -h, --help

   Print usage and exit.

.. option:: -p <PATH>, --path <PATH>

   Path to the minishell directory, defaults to the current directory.

.. option:: -l, --list

   Print available test suites

   .. command-output:: minishell_test --list

.. :ellipsis: 15

.. option:: -t <COMMAND>, --try <COMMAND>

   | Run a custom command like the test would,
   | the only environment variable passed to your executable are ``TERM`` and ``PATH``.

.. option:: -g, --pager

   After running the test, display the result in a pager of your choice, see :ref:`pager configuration <config-pager>`.

Memory Leaks
------------

.. option:: -k, --check-leaks

   | Runs `valgrind <https://valgrind.org/>`_ on tests to check for memory leaks.
   | (disable the usual comparison with the :ref:`config-reference-shell`)

   .. warning::
      | Running ``valgrind`` on each tests may take a while especially if your ``minishell`` isn't correctly optimized,
      | See the :ref:`leaks timeout <config-timeout-leaks>` configuration variable to change the leak tests timeout.

.. option:: -r <BEGIN> <END>, --range <BEGIN> <END>

   | Only run the test in the selected range,
   | ``<BEGIN>`` and ``<END>`` must be test indices.

.. option:: --show-range

   | Show the tests indices.
   | Both :option:`--check-leaks` and :option:`--range` imply this option.

.. option:: -x, --exit-first

   Immediately stops when a test fails.
