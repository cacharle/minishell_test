.. bt in -*- rst -*- mode!

Configuration
=============

Configuration file
------------------

It looks for a ``minishell_test.cfg`` file in your project directory.

Here is what the default configuration looks like:

.. include:: ../minishell_test/data/default.cfg
   :code: cfg


The format of this file is described in more details `here <https://docs.python.org/3/library/configparser.html#supported-ini-file-structure>`_

Global
------

Global settings are defined under the ``minishell_test`` section:

.. code-block:: cfg

   [minishell_test]
   bonus = true

.. conf:: bonus

   :type: true|false
   :default: false

   Run the bonus tests

.. conf:: exec_name

   :type: PATH
   :default: minishell

   Minishell executable name

.. conf:: make

   :type: true|false
   :default: true

   Run ``make`` in your project directory before the test

.. conf:: pager

   :type: NAME
   :default: less

   Pager to use when viewing your results

.. conf:: log_path

   :type: PATH
   :default: minishell_test.log

   File where to put the test results

.. conf:: cache_path

   :type: PATH
   :default: $XDG_CACHE_HOME/minishell_test ^ ~/.cache/minishell_test


Shell
-----

Shell settings are defined under the ``shell`` section:

.. code-block:: cfg

   [shell]
   available_commands = ls,cat

.. conf:: available_commands

   :type: LIST
   :default: rmdir env cat touch ls grep sh head

   Commands available in test

.. conf:: path_variable

   :type: LIST
   :default: {cache:executables_path}

   ``$PATH`` environment variable passed to the shell

Reference
+++++++++

Reference shell settings are defined under the ``shell:reference`` section:

.. code-block:: cfg

   [shell:reference]
   path = /bin/sh

.. conf:: path

   :type: PATH
   :default: /bin/bash

   Path to reference shell (shell which will be compared minishell)
   has to support the ``-c`` option (``sh``, ``bash`` and ``zsh`` support it)

.. conf:: args

   :type: ARGV

   | Supplementary arguments to the reference shell
   | e.g ``--posix`` can be used with bash for a more posix complient behavior

Timeout
-------

Timeout settings are defined under the ``timeout`` section:

.. code-block:: cfg

   [timeout]
   leaks = 60

.. conf:: test

   :type: FLOAT
   :default: 0.5

   Time before a timeout occurs on a regular test (in seconds)

.. conf:: leaks

   :type: FLOAT
   :default: 10

   Time before a timeout occurs on a leak test (with valgrind) (in seconds)
