# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_result.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/01 16:26:34 by cacharle          #+#    #+#              #
#    Updated: 2021/03/02 14:21:14 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import pytest

from minishell_test.config import Config
from minishell_test import colors

colors.disable()
Config.init([])

from minishell_test.test.result import BaseResult, Result, LeakResult
from minishell_test.test.captured import CapturedCommand


class TestBaseResult:
    @pytest.fixture
    def base_result(self):
        return BaseResult("echo bonjour")

    def test_passed(self, base_result):
        with pytest.raises(NotImplementedError):
            base_result.passed

    def test_failed(self, base_result):
        with pytest.raises(NotImplementedError):
            base_result.failed

    def test_repr(self, base_result):
        with pytest.raises(NotImplementedError):
            base_result.__repr__()

    def test_cmd(self, base_result):
        assert "echo bonjour" == base_result._cmd
        assert "foo\\nbar" == BaseResult("foo\nbar")._cmd
        assert "foo\\tbar" == BaseResult("foo\tbar")._cmd
        assert "foo\\vbar" == BaseResult("foo\vbar")._cmd
        assert "foo\\rbar" == BaseResult("foo\rbar")._cmd
        assert "foo\\fbar" == BaseResult("foo\fbar")._cmd

    def test_summarize(self, base_result):
        pass




class TestResult:
    @pytest.fixture
    def result_pass(self):
        return Result(
            "echo bonjour",
            [],
            CapturedCommand("bonjour", 0, []),
            CapturedCommand("bonjour", 0, []),
        )

    @pytest.fixture
    def result_fail(self):
        return Result(
            "echo bonjour",
            [],
            CapturedCommand("bonjour", 0, []),
            CapturedCommand("aurevoir", 0, []),
        )

    def test_passed(self, result_pass, result_fail):
        assert result_pass.passed
        assert not result_fail.passed

    def test_failed(self, result_pass, result_fail):
        assert not result_pass.failed
        assert result_fail.failed

