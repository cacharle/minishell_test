# -*- coding: utf-8 -*-
"""Packaging logic for Flake8."""
import os
import sys

import setuptools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'minishell_test'))  # noqa

setuptools.setup()
