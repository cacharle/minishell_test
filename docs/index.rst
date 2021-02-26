.. program:: minishell_test

minishell_test
==============

Test for 42 school's minishell project.

.. .. image:: https://i.imgur.com/98xh2xY.gif

Getting Started
---------------

Installation
++++++++++++

.. code-block::

    $ pip3 install minishell-test
    $ pip3 install --user minishell-test  # if you don't have root access

Compatibility
+++++++++++++

Your executable **must** support the ``-c`` option which allow to pass command as string.

.. code-block::

    $ bash -c 'echo bonjour je suis | cat -e'
    bonjour je suis$
    $ ./minishell -c 'echo bonjour je suis | cat -e'
    bonjour je suis$


.. note::
    With this setup ``argv[2]`` is what you would usually get in ``line`` from ``get_next_line``.

Usage
+++++

Run all the predefined tests:

.. code-block::

    $ cd <MINISHELL>
    $ minishell_test

.. warning::
    If you get ``command not found``, do either of those things:

    * ``~/.local/bin`` to your ``PATH`` environment variable.
    * run ``$ python3 -m minishell_test`` instead of ``$ minishell_test``


Documentation
-------------

.. toctree::
   :maxdepth: 2

   config
   options
   developers


.. code-block::

    $ minishell_test --help

The options are explained in more details in :ref:`options <options>`.


Environement variables
----------------------

This test only gives the ``PATH`` and ``TERM`` environment variables to your minishell by default (see :ref:`config env`).

You can test this quickly with :option:`--try`.

.. warning::
    Please check that your project still work with this environment before creating an issue or messaging me on Slack.

Bonus
-----

See :ref:`config bonus`
See :ref:`options bonus`

Memory leaks
------------

See :ref:`options leaks`

Linux
-----

It will try to convert to output/status code of ``bash`` on Linux to the one on Mac.
