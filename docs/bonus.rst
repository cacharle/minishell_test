.. _bonus:

Bonus
=====

.. program:: minishell_test


See :ref:`how to enable the bonus tests in the configuration <config-bonus>`
and the :option:`suite` option.

Supported bonus:

.. table::
   :align: left
   :widths: auto

   ======  ====================
   Name            Suite name
   ======  ====================
   ``&&``  ``flow/and``
   ``||``  ``flow/or``
   ``()``  ``flow/parenthesis``
   ``*``   ``preprocess/glob``
   ======  ====================

.. note::
   | If your bonus isn't supported, feel free to add them yourself and make a pull request.
   | Take a look at :ref:`custom-tests` and :ref:`developers`.
