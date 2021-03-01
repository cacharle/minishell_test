Getting Started
---------------

Installation
++++++++++++

.. code-block::

    $ pip3 install minishell-test
    $ pip3 install --user minishell-test  # if you don't have root access

.. _compatibility:

Compatibility
+++++++++++++

Your executable **must** support the ``-c`` option which allow to pass command as an argument.

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

    * Add ``~/.local/bin`` to your ``PATH`` environment variable.
    * Run ``$ python3 -m minishell_test`` instead of ``$ minishell_test``

.. vim:ft=rst
