.. _developers:

Developers
==========

Install requirements
--------------------

.. include:: ../requirements-dev.txt
   :literal:

.. code-block::

    $ pip3 instal -r requirements-dev.txt

Install in *editable* mode
--------------------------

.. code-block::

    $ git clone https://github.com/cacharle/minishell_test
    $ cd minishell_test
    $ pip3 install -e .

This make it possible to modify the source and see the changes live.

Linting
-------

.. code-block::

    $ flake8 minishell_test

Type checking
-------------

.. code-block::

    $ mypy minishell_test

Unit Test
---------

.. code-block::

    $ pytest

Cross environment testing
-------------------------

.. code-block::

    $ tox
