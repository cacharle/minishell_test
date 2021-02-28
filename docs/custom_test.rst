Add Custom Tests
================

Test
----

In your suite function you can use the ``test`` function. With the
following arguments:

1. Command to be tested (output and status will be compared to bash)
2. A command to setup the sandbox directory where the tested command
   will be run
3. List of files to watch (the content of each file will be compared)

.. code:: python

   test("echo bonjour je suis")                                  # simple command
   test("cat < somefile", setup="echo file content > somefile")  # setup
   test("ls > somefile", setup="", files=["somefile"])           # watch a file
   test("echo $A", exports={"A": "a"})                           # export variables
                                                                 # in the environment
   test("echo bonjour", hook=lambda s: s.replace("o", "a"))      # pass the shell output
                                                                 # through a hook function

   test("cat < somefile > otherfile",
        setup="echo file content > somefile",
        files=["otherfile"])

Suite
-----

A test suite is a group of related tests.

.. code:: python

   @suite()  # @suite(bonus=True) if it's a bonus suite
   def suite_yoursuitename(test):
       """ a description of the suite """
       test(...)
       test(...)
       test(...)
