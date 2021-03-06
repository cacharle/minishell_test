# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_suite.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/06 11:20:47 by cacharle          #+#    #+#              #
#    Updated: 2021/03/06 16:01:03 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import pytest
from pathlib import Path

from minishell_test.suite.suite import Suite, NoMatchException, SuiteExitFirstException
from minishell_test.config import Config


class TestSuite:
    @pytest.fixture
    def available_suite_names(self, monkeypatch):
        s = [
            Suite(None, 'bonjour', 'grouped', False, 'nice description'),
            Suite(None, 'aurevoir', 'notgrouped', False, 'not nice description'),
            Suite(None, 'ft', 'yes', False, 'no'),
            Suite(None, 'ft_strlen', 'yes', False, 'no'),
            Suite(None, 'charles', 'cabergs', False, 'est super'),
            Suite(None, 'guillaume', 'cabergs', False, 'est super'),
            Suite(None, 'bonus', 'yes', True, 'est super'),
        ]
        monkeypatch.setattr(Suite, '_available', s)

    def test_list(self, monkeypatch, available_suite_names):
        assert """\
grouped/bonjour ....... nice description
notgrouped/aurevoir ... not nice description
yes/ft ................ no
yes/ft_strlen ......... no
cabergs/charles ....... est super
cabergs/guillaume ..... est super
yes/bonus ............. est super
""" == Suite.list()

    def test_asked_names(self, monkeypatch, available_suite_names):
        def suite_names_set(suites):
            return {s._name for s in suites}
        monkeypatch.setattr(Config, "bonus", False)
        assert {"charles"}                  == suite_names_set(Suite._asked_suites(["charl"]))
        assert {"guillaume"}                == suite_names_set(Suite._asked_suites(["gui"]))
        assert {"charles", "guillaume"}     == suite_names_set(Suite._asked_suites(["cab"]))
        assert {"ft", "ft_strlen"}          == suite_names_set(Suite._asked_suites(["ft"]))
        assert {"ft_strlen"}                == suite_names_set(Suite._asked_suites(["ft_"]))
        assert {"ft", "ft_strlen"}          == suite_names_set(Suite._asked_suites(["yes"]))
        assert {"ft", "ft_strlen", "charles", "guillaume", "bonjour", "aurevoir"} == suite_names_set(Suite._asked_suites([]))
        monkeypatch.setattr(Config, "bonus", True)
        assert {"ft", "ft_strlen", "bonus"} == suite_names_set(Suite._asked_suites(["yes"]))
        assert {"ft", "ft_strlen", "charles", "guillaume", "bonjour", "aurevoir", "bonus"} == suite_names_set(Suite._asked_suites([]))
        with pytest.raises(NoMatchException) as e:
            Suite._asked_suites(["notanavailablename"])
        assert "notanavailablename" == e.value._name
        assert (f"Name `notanavailablename` doesn't match any suite/group name\n\t"
                 "Try to run with -l to see the available suites") == e.value.__str__()

    @pytest.fixture
    def runnable_suite(self):
        def suite_func(test):
            test("echo bonjour")
        monkeypatch.setattr(
            Suite,
            '_available',
            [Suite(suite_func, "suite_name", "suite_group", False, "suite_description")]
        )

    def test_instance_run(self, monkeypatch, capsys):
        def suite_func(test):
            test("echo bonjour")
            test("echo foo")
            test("echo bar")
        s = Suite(suite_func, "suite_name", "suite_group", False, "suite_description")
        monkeypatch.setattr(Config, 'minishell_exec_path', Path("/bin/bash"))
        s._register()
        assert len(s._tests) == 3
        assert "echo bonjour" == s._tests[0]._cmd
        assert "echo foo"     == s._tests[1]._cmd
        assert "echo bar"     == s._tests[2]._cmd
        monkeypatch.setattr(Config, 'term_cols', 20)
        s._run()
        output = capsys.readouterr()
        output_lines = output.out.splitlines()
        assert len(output_lines) == 4
        assert '#### suite_name ####' == output_lines[0]
        assert len(s._results) == 3
        assert all(r.passed for r in s._results)

        s = Suite(suite_func, "suite_name", "suite_group", False, "suite_description")
        s._register()
        monkeypatch.setattr(Config, 'range', (1, 2))
        s._run()
        output = capsys.readouterr()
        output_lines = output.out.splitlines()
        assert len(output_lines) == 3
        assert '#### suite_name ####' == output_lines[0]
        assert len(s._results) == 2
        assert all(r.passed for r in s._results)

        monkeypatch.setattr(Config, 'exit_first', True)
        monkeypatch.setattr(Config, 'minishell_exec_path', Path("/usr/bin/cat"))
        s = Suite(suite_func, "suite_name", "suite_group", False, "suite_description")
        s._register()
        with pytest.raises(SuiteExitFirstException):
            s._run()
        output = capsys.readouterr()
        output_lines = output.out.splitlines()
        assert len(output_lines) == 2
        assert '#### suite_name ####' == output_lines[0]
        assert len(s._results) == 1
        assert all(r.failed for r in s._results)

    def test_summarize(self):
        assert False
