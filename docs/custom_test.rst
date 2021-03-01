.. _custom-tests:

Add Custom Tests
================

You can add custom test in a file named ``minishell_test.py`` at the root of your project.

Suite
-----

A test suite is a group of related tests.

.. code:: python

   @suite()
   def suite_yoursuitename(test):
       """ a description of the suite """
       test(...)
       test(...)

.. warning::
   your suite function name **must** be prefixed by ``suite_``.

Bonus
+++++

.. code:: python

   @suite(bonus=True)
   def suite_yoursuitename(test):

Test
----

In your suite function you can use the ``test`` function (passed in the suite function argument).

The first argument of ``test`` is passed to the shell (via ``-c``, see :ref:`compatibility`).

.. code:: python

   test("echo bonjour je suis")
   test("cat -e < /etc/shells")
   test("sed 's/sh/foo/g' /etc/shells > notshells")

Setup Command
+++++++++++++

| ``setup`` is a command to run before the test.
| Contrary to the tested command there is no restriction for the ``setup`` command.
| The only requirement for the test setup to be successful is for this command to return a non zero status code.

.. code:: python

   test("cat < somefile", setup="echo file content > somefile")
   test("ls -la",         setup="touch a b c d e")


Compare Files
+++++++++++++

| The ``files`` argument is a list of files to compare against the :ref:`config-reference-shell`..
| Checks if the file exists and the file's content.

.. code:: python

   test("echo bonjour > somefile",                   files=["somefile"])
   test("echo bonjour > a > b > c",                  files=["a", "b", "c"])
   test("echo bonjour > foo ; echo aurevoir >> foo", files=["foo"])

Export Variables
++++++++++++++++

Add environment variable passed to your executable with the ``exports`` dictionary.

.. note::
   Those variables will be passed **in addition** of the default exports (i.e ``PATH`` and ``TERM``).

.. code:: python

   test("echo $FOO",     exports={"FOO": "foo"})
   test("echo $FOO$BAR", exports={"FOO": "foo", "BAR": "bar"})
   test("echo $SHLVL",   exports={"SHLVL": "100"})

Timeout
+++++++

``timeout`` overwrites the :ref:`default timeout value<config-timeout-test>` of the configuration.

.. code:: python

   test("echo /*/*/*", timeout=60)

Hook
++++

Output
^^^^^^

``hook`` is a function (or list of functions) applied on the output of test after it is done running.

.. code:: python

   def replace_foo_by_bar_hook(output):
       return output.replace("foo", "bar")

   test("echo @@foo foo foo@@", hook=replace_foo_by_bar_hook)
   # initial output:            @@foo foo foo@@
   # after passed through hook: @@bar bar bar@@

Status Code
^^^^^^^^^^^

``hook_status`` is similar to ``hook`` only it take a status code has it's first argument and return the new status.

.. code:: python

   def reverse_error(status):
       return 0 if status != 0 else 1

   test("cat doesnotexists", hook=reverse_error)
   # status code will be 0 after status hook
