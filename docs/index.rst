.. program:: minishell_test

minishell_test documentation
============================

.. toctree::
   :maxdepth: 1

   config
   options
   developers

.. include:: gettingstarted.rst

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

.. Add individual test
.. -------------------
..
.. In your suite function you can use the `test` function. With the following arguments:
..
.. 1. Command to be tested (output and status will be compared to bash)
.. 2. A command to setup the sandbox directory where the tested command will be run
.. 3. List of files to watch (the content of each file will be compared)
..
.. ```python
.. test("echo bonjour je suis")                                  # simple command
.. test("cat < somefile", setup="echo file content > somefile")  # setup
.. test("ls > somefile", setup="", files=["somefile"])           # watch a file
.. test("echo $A", exports={"A": "a"})                           # export variables
..                                                               # in the environment
.. test("echo bonjour", hook=lambda s: s.replace("o", "a"))      # pass the shell output
..                                                               # through a hook function
..
.. test("cat < somefile > otherfile",
..      setup="echo file content > somefile",
..      files=["otherfile"])
.. ```
..
.. ### Add Suite
..
.. A test suite is a group of related tests.
..
.. ```python
.. @suite()  # @suite(bonus=True) if it's a bonus suite
.. def suite_yoursuitename(test):
..     """ a description of the suite """
..     test(...)
..     test(...)
..     test(...)
.. ```
..
