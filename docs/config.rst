.. bt in -*- rst -*- mode!

Configuration
=============

File
----

The configuration file is named ``minishell_test.cfg`` and should be located at the root of your project.

Here is what the default configuration looks like:

.. include:: ../minishell_test/data/default.cfg
   :code: ini


The format of this file is described in more details
`here <https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`_.

Global
------

Global settings are defined under the ``[minishell_test]`` section.

.. _config-bonus:
.. conf:: bonus

   :type: true|false

   Enable the bonus tests, see :ref:`bonus`.

.. _config-make:
.. conf:: make

   :type: true|false

   Run the ``make`` command in your project directory before the test.

.. _config-make-args:
.. conf:: make_args

   :type: space separated list

   | Argument given to the ``make`` command.
   | The default value (``MINISHELL_TEST_FLAGS=-DMINISHELL_TEST``) allows you to do conditional compilation
     to support both the ``-c`` option and the subject
     (which doesn't say anything about options, so we assume the minishell executable didn't take any).

   | In your ``Makefile`` add ``$(MINISHELL_TEST_FLAGS)`` in your object compilation command.
     (e.g ``$(CC) $(CCFLAGS) -c -o $@ $<``)

   | You can then have something resembling the following in your ``main``:

   .. code:: c

        #ifndef MINISHELL_TEST
        int main(int argc, char **argv)
        {
            if (argc != 1) error;
            ...
        }
        #else
        int main(int argc, char **argv)
        {
            if (argc != 3 && strcmp(argv[1], "-c") == 0) do the thing;
            ...
        }
        #endif

.. _config-check-error-messages:

.. conf:: check_error_messages

   :type: true|false

   | If is ``true``, will ignore the content of the error messages outputted by the reference shell,
   | Useful if you have implemented your own error messages and don't want to copy bash's ones.

.. _config-pager:
.. conf:: pager

   :type: command name

   | Pager to use when viewing your results after the tests finished running.
   | Will be called like: ``{pager} {log_filename}``.

.. conf:: end_command_with_linefeed

   :type: true|false

   Weather the test should add a linefeed (``\n``) at the end of the command passed via ``-c``.

Shell
-----

Shell settings are defined under the ``[shell]`` section.

.. conf:: available_commands

   :type: multi-line list

   Commands available in a test.

   .. warning::
      Some of the default tests won't serve their purpose
      if the default available commands are not present.

.. _config-path-variable:
.. conf:: path_variable

   :type: string (``:`` separated directories)

   ``$PATH`` environment variable passed to the shell.

   .. note::
      ``{shell_available_commands_dir}`` will be replaced by the directory
      where the available commands are stored.

.. _config-reference-shell:

Reference Shell
+++++++++++++++

Reference shell settings are defined under the ``[shell:reference]`` section.

.. conf:: path

   :type: path

   Path to reference shell, to which your ``minishell`` will be compared.

   .. note::
      has to support the ``-c`` option, ``sh``, ``bash`` and ``zsh`` support it.

.. conf:: args

   :type: space separated list

   | Supplementary arguments to the reference shell.
   | e.g ``--posix`` can be used with bash for a more posix compliant behavior.

Timeout
-------

Timeout settings are defined under the ``[timeout]`` section.

.. _config-timeout-test:

.. conf:: test

   :type: float (seconds)

   Time before a timeout occurs on a regular test.

.. _config-timeout-leaks:

.. conf:: leaks

   :type: float (seconds)

   Time before a timeout occurs on a leak test (with ``valgrind``).
