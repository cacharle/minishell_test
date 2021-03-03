# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_result.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/01 16:26:34 by cacharle          #+#    #+#              #
#    Updated: 2021/03/03 07:53:09 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import pytest

from minishell_test.config import Config
from minishell_test import colors

from minishell_test.test.result import BaseResult, Result, LeakResult, LeakResultException
from minishell_test.test.captured import CapturedCommand, CapturedTimeout

from tests.helpers import config_context


colors.disable()
Config.init([])


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

    def test_summarize(self, base_result):
        with pytest.raises(NotImplementedError):
            base_result.summarize(0)

    def test_cmd(self, base_result):
        assert "echo bonjour" == base_result._cmd
        assert "foo\\nbar" == BaseResult("foo\nbar")._cmd
        assert "foo\\tbar" == BaseResult("foo\tbar")._cmd
        assert "foo\\vbar" == BaseResult("foo\vbar")._cmd
        assert "foo\\rbar" == BaseResult("foo\rbar")._cmd
        assert "foo\\fbar" == BaseResult("foo\fbar")._cmd


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

    @pytest.fixture
    def result_fail_status(self):
        return Result(
            "echo bonjour",
            [],
            CapturedCommand("bonjour", 0, []),
            CapturedCommand("bonjour", 1, []),
        )

    @pytest.fixture
    def result_fail_file(self):
        return Result(
            "echo bonjour > foo",
            ["foo"],
            CapturedCommand("bonjour", 0, ["bonjour"]),
            CapturedCommand("bonjour", 0, ["aurevoir"]),
        )

    @pytest.fixture
    def result_fail_file_not_exist(self):
        return Result(
            "echo bonjour > foo",
            ["foo"],
            CapturedCommand("bonjour", 0, ["bonjour"]),
            CapturedCommand("bonjour", 0, [None]),
        )

    @pytest.fixture
    def result_fail_file_not_exist_expected(self):
        return Result(
            "echo bonjour",
            ["foo"],
            CapturedCommand("bonjour", 0, [None]),
            CapturedCommand("bonjour", 0, ["bonjour"]),
        )

    @pytest.fixture
    def result_fail_file_multiple(self):
        return Result(
            "echo bonjour > foo > bar",
            ["foo", "bar"],
            CapturedCommand("bonjour", 0, ["", "bonjour"]),
            CapturedCommand("bonjour", 0, ["bonjour", None]),
        )

    @pytest.fixture
    def result_fail_timeout(self):
        return Result("echo bonjour", [], CapturedCommand("bonjour", 0, []), CapturedTimeout())

    @pytest.fixture
    def result_pass_long_cmd(self):
        return Result("e" * 300, [], CapturedCommand("", 0, []), CapturedCommand("", 0, []))

    def test_passed(self, result_pass, result_fail, result_fail_status, result_fail_file, result_fail_file_not_exist,
                    result_fail_file_multiple, result_fail_timeout, result_fail_file_not_exist_expected, result_pass_long_cmd):
        assert result_pass.passed
        assert result_pass_long_cmd.passed
        assert not result_fail.passed
        assert not result_fail_status.passed
        assert not result_fail_file.passed
        assert not result_fail_file_not_exist.passed
        assert not result_fail_file_multiple.passed
        assert not result_fail_timeout.passed
        assert not result_fail_file_not_exist_expected.passed

    def test_failed(self, result_pass, result_fail, result_fail_status, result_fail_file, result_fail_file_not_exist,
                    result_fail_file_multiple, result_fail_timeout, result_fail_file_not_exist_expected, result_pass_long_cmd):
        assert not result_pass.failed
        assert not result_pass_long_cmd.failed
        assert result_fail.failed
        assert result_fail_status.failed
        assert result_fail_file.failed
        assert result_fail_file_not_exist.failed
        assert result_fail_file_multiple.failed
        assert result_fail_timeout.failed
        assert result_fail_file_not_exist_expected.failed

    @pytest.mark.parametrize("term_cols", range(40, 300, 40))
    def test_summarize(self, result_pass, result_fail, result_fail_status, result_fail_file, result_fail_file_not_exist,
                       result_fail_timeout, result_fail_file_not_exist_expected, result_pass_long_cmd, term_cols):
        with config_context(show_range=False, term_cols=term_cols):
            assert f"{'echo bonjour':{term_cols - 7}} [PASS]" == result_pass.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_fail.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_fail_status.summarize(-1)
            assert f"{'echo bonjour > foo':{term_cols - 7}} [FAIL]" == result_fail_file.summarize(-1)
            assert f"{'echo bonjour > foo':{term_cols - 7}} [FAIL]" == result_fail_file_not_exist.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_fail_timeout.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_fail_file_not_exist_expected.summarize(-1)
            assert f"{('e' * 300)[:term_cols - 10]}... [PASS]" == result_pass_long_cmd.summarize(-1)
        with config_context(show_range=True, term_cols=term_cols):
            assert f" 1: {'echo bonjour':{term_cols - 11}} [PASS]" == result_pass.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail_status.summarize(1)
            assert f" 1: {'echo bonjour > foo':{term_cols - 11}} [FAIL]" == result_fail_file.summarize(1)
            assert f" 1: {'echo bonjour > foo':{term_cols - 11}} [FAIL]" == result_fail_file_not_exist.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail_timeout.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail_file_not_exist_expected.summarize(1)
            assert f" 1: {('e' * 300)[:term_cols - 14]}... [PASS]" == result_pass_long_cmd.summarize(1)
            assert f"99: {'echo bonjour':{term_cols - 11}} [PASS]" == result_pass.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail_status.summarize(99)
            assert f"99: {'echo bonjour > foo':{term_cols - 11}} [FAIL]" == result_fail_file.summarize(99)
            assert f"99: {'echo bonjour > foo':{term_cols - 11}} [FAIL]" == result_fail_file_not_exist.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail_timeout.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_fail_file_not_exist_expected.summarize(99)
            assert f"99: {('e' * 300)[:term_cols - 14]}... [PASS]" == result_pass_long_cmd.summarize(99)
            assert f"100: {'echo bonjour':{term_cols - 12}} [PASS]" == result_pass.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_fail.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_fail_status.summarize(100)
            assert f"100: {'echo bonjour > foo':{term_cols - 12}} [FAIL]" == result_fail_file.summarize(100)
            assert f"100: {'echo bonjour > foo':{term_cols - 12}} [FAIL]" == result_fail_file_not_exist.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_fail_timeout.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_fail_file_not_exist_expected.summarize(100)
            assert f"100: {('e' * 300)[:term_cols - 15]}... [PASS]" == result_pass_long_cmd.summarize(100)

    def test_repr(self, result_fail, result_fail_status, result_fail_file, result_fail_file_not_exist, result_fail_file_multiple,
                  result_fail_timeout, result_fail_file_not_exist_expected):
        assert """\
|> WITH echo bonjour
|----------------------------------------EXPECTED-------------------------------
bonjour
|----------------------------------------ACTUAL---------------------------------
aurevoir
""" == result_fail.__repr__()
        assert """\
|> WITH echo bonjour
| STATUS: expected 0 actual 1
""" == result_fail_status.__repr__()
        assert """\
|> WITH echo bonjour > foo
|# FILE foo
|----------------------------------------EXPECTED-------------------------------
bonjour
|----------------------------------------ACTUAL---------------------------------
aurevoir
""" == result_fail_file.__repr__()
        assert """\
|> WITH echo bonjour > foo
|# FILE foo
|----------------------------------------EXPECTED-------------------------------
bonjour
|----------------------------------------ACTUAL---------------------------------
FROM TEST: File not created
""" == result_fail_file_not_exist.__repr__()
        assert """\
|> WITH echo bonjour > foo > bar
|# FILE foo
|----------------------------------------EXPECTED-------------------------------
|----------------------------------------ACTUAL---------------------------------
bonjour
|# FILE bar
|----------------------------------------EXPECTED-------------------------------
bonjour
|----------------------------------------ACTUAL---------------------------------
FROM TEST: File not created
""" == result_fail_file_multiple.__repr__()
        assert """\
|> WITH echo bonjour
TIMEOUT
""" == result_fail_timeout.__repr__()
        assert """\
|> WITH echo bonjour
|# FILE foo
|----------------------------------------EXPECTED-------------------------------
FROM TEST: File not created
|----------------------------------------ACTUAL---------------------------------
bonjour
""" == result_fail_file_not_exist_expected.__repr__()

    def test_expected_is_timeout(self):
        with pytest.raises(RuntimeError):
            Result("echo bonjour", [], CapturedTimeout(), CapturedCommand("bonjour", 0, []))


class TestLeakResult:
    @pytest.fixture
    def result_leak_pass(self):
        valgrind_output = r"""
==33584== Memcheck, a memory error detector
==33584== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==33584== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==33584== Command: ./minishell -c echo\ bonjour
==33584==
bonjour
==33584==
==33584== HEAP SUMMARY:
==33584==     in use at exit: 0 bytes in 0 blocks
==33584==   total heap usage: 88 allocs, 88 frees, 102,949 bytes allocated
==33584==
==33584==  LEAK SUMMARY:
==33584==     definitely lost: 0 bytes in 0 blocks
==33584==     indirectly lost: 0 bytes in 0 blocks
==33584==       possibly lost: 0 bytes in 0 blocks
==33584==     still reachable: 0 bytes in 0 blocks
==33584==          suppressed: 0 bytes in 0 blocks
==33584==
==33584== For lists of detected and suppressed errors, rerun with: -s
==33584== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
""".lstrip("\n")
        return LeakResult("echo bonjour", CapturedCommand(valgrind_output, 0, []))

    @pytest.fixture
    def result_leak_fail_definitive(self):
        valgrind_output = r"""
==32896== Memcheck, a memory error detector
==32896== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32896== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==32896== Command: ./minishell -c echo\ bonjour
==32896==
bonjour
==32896==
==32896== HEAP SUMMARY:
==32896==     in use at exit: 3,787 bytes in 75 blocks
==32896==   total heap usage: 88 allocs, 13 frees, 102,949 bytes allocated
==32896==
==32896== 3,787 (24 direct, 3,763 indirect) bytes in 1 blocks are definitely lost in loss record 5 of 5
==32896==    at 0x483E77F: malloc (vg_replace_malloc.c:307)
==32896==    by 0x10D317: ft_vecnew (ft_vecnew.c:26)
==32896==    by 0x109382: env_from_array (env.c:33)
==32896==    by 0x1091C1: main (main.c:111)
==32896==
==32896== LEAK SUMMARY:
==32896==    definitely lost: 24 bytes in 1 blocks
==32896==    indirectly lost: 0 bytes in 0 blocks
==32896==      possibly lost: 0 bytes in 0 blocks
==32896==    still reachable: 0 bytes in 0 blocks
==32896==         suppressed: 0 bytes in 0 blocks
==32896==
==32896== For lists of detected and suppressed errors, rerun with: -s
==32896== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
""".lstrip("\n")
        return LeakResult("echo bonjour", CapturedCommand(valgrind_output, 0, []))

    @pytest.fixture
    def result_leak_fail_indirect(self):
        valgrind_output = r"""
==32896== Memcheck, a memory error detector
==32896== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32896== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==32896== Command: ./minishell -c echo\ bonjour
==32896==
bonjour
==32896==
==32896== HEAP SUMMARY:
==32896==     in use at exit: 3,787 bytes in 75 blocks
==32896==   total heap usage: 88 allocs, 13 frees, 102,949 bytes allocated
==32896==
==32896== 3,787 (24 direct, 3,763 indirect) bytes in 1 blocks are definitely lost in loss record 5 of 5
==32896==    at 0x483E77F: malloc (vg_replace_malloc.c:307)
==32896==    by 0x10D317: ft_vecnew (ft_vecnew.c:26)
==32896==    by 0x109382: env_from_array (env.c:33)
==32896==    by 0x1091C1: main (main.c:111)
==32896==
==32896== LEAK SUMMARY:
==32896==    definitely lost: 0 bytes in 0 blocks
==32896==    indirectly lost: 3,763 bytes in 74 blocks
==32896==      possibly lost: 0 bytes in 0 blocks
==32896==    still reachable: 0 bytes in 0 blocks
==32896==         suppressed: 0 bytes in 0 blocks
==32896==
==32896== For lists of detected and suppressed errors, rerun with: -s
==32896== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
""".lstrip("\n")
        return LeakResult("echo bonjour", CapturedCommand(valgrind_output, 0, []))

    @pytest.fixture
    def result_leak_fail_both(self):
        valgrind_output = r"""
==32896== Memcheck, a memory error detector
==32896== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32896== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==32896== Command: ./minishell -c echo\ bonjour
==32896==
bonjour
==32896==
==32896== HEAP SUMMARY:
==32896==     in use at exit: 3,787 bytes in 75 blocks
==32896==   total heap usage: 88 allocs, 13 frees, 102,949 bytes allocated
==32896==
==32896== 3,787 (24 direct, 3,763 indirect) bytes in 1 blocks are definitely lost in loss record 5 of 5
==32896==    at 0x483E77F: malloc (vg_replace_malloc.c:307)
==32896==    by 0x10D317: ft_vecnew (ft_vecnew.c:26)
==32896==    by 0x109382: env_from_array (env.c:33)
==32896==    by 0x1091C1: main (main.c:111)
==32896==
==32896== LEAK SUMMARY:
==32896==    definitely lost: 24 bytes in 1 blocks
==32896==    indirectly lost: 3,763 bytes in 74 blocks
==32896==      possibly lost: 0 bytes in 0 blocks
==32896==    still reachable: 0 bytes in 0 blocks
==32896==         suppressed: 0 bytes in 0 blocks
==32896==
==32896== For lists of detected and suppressed errors, rerun with: -s
==32896== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
""".lstrip("\n")
        return LeakResult("echo bonjour", CapturedCommand(valgrind_output, 0, []))

    @pytest.fixture
    def result_leak_pass_no_count(self):
        valgrind_output = r"""
==33584== Memcheck, a memory error detector
==33584== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==33584== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==33584== Command: ./minishell -c echo\ bonjour
==33584==
bonjour
==33584==
==33584== HEAP SUMMARY:
==33584==     in use at exit: 0 bytes in 0 blocks
==33584==   total heap usage: 88 allocs, 88 frees, 102,949 bytes allocated
==33584==
==33584== All heap blocks were freed -- no leaks are possible
==33584==
==33584== For lists of detected and suppressed errors, rerun with: -s
==33584== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
""".lstrip("\n")
        return LeakResult("echo bonjour", CapturedCommand(valgrind_output, 0, []))

    @pytest.fixture
    def result_leak_fail_timeout(self):
        return LeakResult("echo bonjour", CapturedTimeout())

    def test_passed(self, result_leak_pass, result_leak_fail_indirect, result_leak_fail_definitive,
                    result_leak_fail_both, result_leak_pass_no_count, result_leak_fail_timeout):
        assert result_leak_pass.passed
        assert result_leak_pass_no_count.passed
        assert not result_leak_fail_indirect.passed
        assert not result_leak_fail_definitive.passed
        assert not result_leak_fail_both.passed
        assert not result_leak_fail_timeout.passed

    def test_failed(self, result_leak_pass, result_leak_fail_indirect, result_leak_fail_definitive,
                    result_leak_fail_both, result_leak_pass_no_count, result_leak_fail_timeout):
        assert not result_leak_pass.failed
        assert not result_leak_pass_no_count.failed
        assert result_leak_fail_indirect.failed
        assert result_leak_fail_definitive.failed
        assert result_leak_fail_both.failed
        assert result_leak_fail_timeout.failed

    @pytest.mark.parametrize("term_cols", range(40, 300, 40))
    def test_summarize(self, result_leak_pass, result_leak_fail_indirect, result_leak_fail_definitive,
                       result_leak_fail_both, result_leak_pass_no_count, result_leak_fail_timeout, term_cols):
        with config_context(show_range=False, term_cols=term_cols):
            assert f"{'echo bonjour':{term_cols - 7}} [PASS]" == result_leak_pass.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [PASS]" == result_leak_pass_no_count.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_leak_fail_definitive.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_leak_fail_indirect.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_leak_fail_both.summarize(-1)
            assert f"{'echo bonjour':{term_cols - 7}} [FAIL]" == result_leak_fail_timeout.summarize(-1)
        with config_context(show_range=True, term_cols=term_cols):
            assert f" 1: {'echo bonjour':{term_cols - 11}} [PASS]" == result_leak_pass.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [PASS]" == result_leak_pass_no_count.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_definitive.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_indirect.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_both.summarize(1)
            assert f" 1: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_timeout.summarize(1)
            assert f"99: {'echo bonjour':{term_cols - 11}} [PASS]" == result_leak_pass.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [PASS]" == result_leak_pass_no_count.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_definitive.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_indirect.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_both.summarize(99)
            assert f"99: {'echo bonjour':{term_cols - 11}} [FAIL]" == result_leak_fail_timeout.summarize(99)
            assert f"100: {'echo bonjour':{term_cols - 12}} [PASS]" == result_leak_pass.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [PASS]" == result_leak_pass_no_count.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_leak_fail_definitive.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_leak_fail_indirect.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_leak_fail_both.summarize(100)
            assert f"100: {'echo bonjour':{term_cols - 12}} [FAIL]" == result_leak_fail_timeout.summarize(100)

    def test_repr(self, result_leak_fail_indirect, result_leak_fail_definitive, result_leak_fail_both, result_leak_fail_timeout):
        assert r"""
|> WITH echo bonjour
==32896== Memcheck, a memory error detector
==32896== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32896== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==32896== Command: ./minishell -c echo\ bonjour
==32896==
bonjour
==32896==
==32896== HEAP SUMMARY:
==32896==     in use at exit: 3,787 bytes in 75 blocks
==32896==   total heap usage: 88 allocs, 13 frees, 102,949 bytes allocated
==32896==
==32896== 3,787 (24 direct, 3,763 indirect) bytes in 1 blocks are definitely lost in loss record 5 of 5
==32896==    at 0x483E77F: malloc (vg_replace_malloc.c:307)
==32896==    by 0x10D317: ft_vecnew (ft_vecnew.c:26)
==32896==    by 0x109382: env_from_array (env.c:33)
==32896==    by 0x1091C1: main (main.c:111)
==32896==
==32896== LEAK SUMMARY:
==32896==    definitely lost: 24 bytes in 1 blocks
==32896==    indirectly lost: 0 bytes in 0 blocks
==32896==      possibly lost: 0 bytes in 0 blocks
==32896==    still reachable: 0 bytes in 0 blocks
==32896==         suppressed: 0 bytes in 0 blocks
==32896==
==32896== For lists of detected and suppressed errors, rerun with: -s
==32896== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
""".lstrip("\n") == result_leak_fail_definitive.__repr__()
        assert r"""
|> WITH echo bonjour
==32896== Memcheck, a memory error detector
==32896== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32896== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==32896== Command: ./minishell -c echo\ bonjour
==32896==
bonjour
==32896==
==32896== HEAP SUMMARY:
==32896==     in use at exit: 3,787 bytes in 75 blocks
==32896==   total heap usage: 88 allocs, 13 frees, 102,949 bytes allocated
==32896==
==32896== 3,787 (24 direct, 3,763 indirect) bytes in 1 blocks are definitely lost in loss record 5 of 5
==32896==    at 0x483E77F: malloc (vg_replace_malloc.c:307)
==32896==    by 0x10D317: ft_vecnew (ft_vecnew.c:26)
==32896==    by 0x109382: env_from_array (env.c:33)
==32896==    by 0x1091C1: main (main.c:111)
==32896==
==32896== LEAK SUMMARY:
==32896==    definitely lost: 0 bytes in 0 blocks
==32896==    indirectly lost: 3,763 bytes in 74 blocks
==32896==      possibly lost: 0 bytes in 0 blocks
==32896==    still reachable: 0 bytes in 0 blocks
==32896==         suppressed: 0 bytes in 0 blocks
==32896==
==32896== For lists of detected and suppressed errors, rerun with: -s
==32896== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
""".lstrip("\n") == result_leak_fail_indirect.__repr__()
        assert r"""
|> WITH echo bonjour
==32896== Memcheck, a memory error detector
==32896== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==32896== Using Valgrind-3.16.1 and LibVEX; rerun with -h for copyright info
==32896== Command: ./minishell -c echo\ bonjour
==32896==
bonjour
==32896==
==32896== HEAP SUMMARY:
==32896==     in use at exit: 3,787 bytes in 75 blocks
==32896==   total heap usage: 88 allocs, 13 frees, 102,949 bytes allocated
==32896==
==32896== 3,787 (24 direct, 3,763 indirect) bytes in 1 blocks are definitely lost in loss record 5 of 5
==32896==    at 0x483E77F: malloc (vg_replace_malloc.c:307)
==32896==    by 0x10D317: ft_vecnew (ft_vecnew.c:26)
==32896==    by 0x109382: env_from_array (env.c:33)
==32896==    by 0x1091C1: main (main.c:111)
==32896==
==32896== LEAK SUMMARY:
==32896==    definitely lost: 24 bytes in 1 blocks
==32896==    indirectly lost: 3,763 bytes in 74 blocks
==32896==      possibly lost: 0 bytes in 0 blocks
==32896==    still reachable: 0 bytes in 0 blocks
==32896==         suppressed: 0 bytes in 0 blocks
==32896==
==32896== For lists of detected and suppressed errors, rerun with: -s
==32896== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
""".lstrip("\n") == result_leak_fail_both.__repr__()
        assert r"""
|> WITH echo bonjour
TIMEOUT
""".lstrip("\n") == result_leak_fail_timeout.__repr__()

    @pytest.mark.parametrize(
        "output",
        [
            "",
            "foo",
            "asdlfjas;dkljfaslkdjflas",
            "==32896==    definitely lost: bytes in 1 blocks"
            "==32896==    definitely lost: a bytes in 1 blocks"
            "==32896==    definitely lost: _ bytes in 1 blocks"
            "==32896==    indirectly lost: bytes in 1 blocks"
            "==32896==    indirectly lost: a bytes in 1 blocks"
            "==32896==    indirectly lost: _ bytes in 1 blocks"
            "==32896==    bonjour lost: 1 bytes in 1 blocks"
        ]
    )
    def test_parsing_error(self, output):
        with pytest.raises(LeakResultException) as e:
            LeakResult("echo bonjour", CapturedCommand(output, 0, [])).passed
        assert "echo bonjour" == e.value._cmd
        assert output == e.value._captured.output
        assert f"valgrind output parsing failed for `echo bonjour`:\n{output}" == e.value.__str__()
