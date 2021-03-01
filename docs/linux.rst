Linux
-----

| The output and status codes will be converted to the one of ``bash`` OSX.
| Although it mainly depends on your ``bash`` version (``3.2.57`` on the school's computers).

Generally those differences are pretty minor, here is an example (``line n`` changes).

Linux:

.. code-block::

   bash: -c: line 1: syntax error near unexpected token `newline'
   bash: -c: line 1: `>'

OSX:

.. code-block::

   bash: -c: line 0: syntax error near unexpected token `newline'
   bash: -c: line 0: `>'

.. note::
   I've tried with ``bash5.1.4`` at home and most of the test are converted but don't be surprised if it's not the case for some of them.
