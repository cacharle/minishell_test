# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_test.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/02 18:48:57 by cacharle          #+#    #+#              #
#    Updated: 2021/03/06 10:07:07 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #


import pytest
from pathlib import Path

from minishell_test.config import Config
from minishell_test import colors

from minishell_test.test.result import LeakResult
from minishell_test.test.captured import CapturedCommand, CapturedTimeout
from minishell_test.test.test import Test, TestSetupException


colors.disable()
Config.init([])


class TestTest:
    @pytest.fixture(autouse=True)
    def reset_config(self):
        Config.init([])

    def test_init_timeout(self, monkeypatch):
        assert Config.timeout_test == Test("")._timeout
        assert Config.timeout_test == Test("", timeout=0)._timeout
        assert 2                   == Test("", timeout=2)._timeout
        assert 100                 == Test("", timeout=100)._timeout
        monkeypatch.setattr(Config, 'check_leaks', True)
        assert Config.timeout_leaks == Test("", timeout=-10)._timeout
        assert Config.timeout_leaks == Test("", timeout=0)._timeout
        assert Config.timeout_leaks == Test("", timeout=1)._timeout
        assert Config.timeout_leaks == Test("", timeout=100)._timeout

    def test_coerce_into_list(self):
        assert [1] == Test._coerce_into_list(1)
        assert [1] == Test._coerce_into_list([1])
        assert ["bonjour"] == Test._coerce_into_list("bonjour")
        assert ["bonjour"] == Test._coerce_into_list(["bonjour"])
        assert ["bonjour", "foo", "bar"] == Test._coerce_into_list(["bonjour", "foo", "bar"])

    def test_apply_hook(self, monkeypatch):
        bonjour_to_foo  = lambda x: x.replace("bonjour", "foo")   # noqa
        foo_to_aurevoir = lambda x: x.replace("foo", "aurevoir")  # noqa
        assert "foo"      == Test._apply_hooks("bonjour", [bonjour_to_foo])
        assert "aurevoir" == Test._apply_hooks("foo", [foo_to_aurevoir])
        assert "aurevoir" == Test._apply_hooks("bonjour", [bonjour_to_foo, foo_to_aurevoir])
        plus_one  = lambda x: x + 1  # noqa
        minus_one = lambda x: x - 1  # noqa
        assert 1  == Test._apply_hooks(0, [plus_one])
        assert 5  == Test._apply_hooks(0, [plus_one, plus_one, plus_one, plus_one, plus_one])
        assert -1 == Test._apply_hooks(0, [minus_one])
        assert -5 == Test._apply_hooks(0, [minus_one, minus_one, minus_one, minus_one, minus_one])
        assert 0  == Test._apply_hooks(0, [plus_one, minus_one, plus_one, minus_one, plus_one, minus_one])
        monkeypatch.setattr(Config, 'check_leaks', True)
        assert "foo"     == Test._apply_hooks("foo", [foo_to_aurevoir])
        assert "bonjour" == Test._apply_hooks("bonjour", [bonjour_to_foo, foo_to_aurevoir])
        assert 0         == Test._apply_hooks(0, [plus_one, plus_one, plus_one, plus_one, plus_one])
        assert 0         == Test._apply_hooks(0, [minus_one, minus_one, minus_one, minus_one, minus_one])

    def test_extended_cmd(self):
        assert "" == Test("")._extended_cmd
        assert "echo bonjour" == Test("echo bonjour")._extended_cmd
        assert "[SETUP echo foo > bar] echo bonjour" == Test("echo bonjour", setup="echo foo > bar")._extended_cmd
        assert "[EXPORTS A='a' B='b' C='c'] echo bonjour" == Test("echo bonjour", exports={"A": "a", "B": "b", "C": "c"})._extended_cmd
        assert "[SETUP echo foo > bar] [EXPORTS A='a' B='b' C='c'] echo bonjour" == Test("echo bonjour", setup="echo foo > bar", exports={"A": "a", "B": "b", "C": "c"})._extended_cmd

    BIN_DIR = Path(__file__).parent / "bin"

    def test_run_echo(self, monkeypatch):
        monkeypatch.setattr(Config, 'minishell_exec_path', self.BIN_DIR / "minishell-echo")
        r = Test("bonjour").run()
        assert r.actual == CapturedCommand("bonjour\n", 0, [])
        assert r.expected.status != 0

    @pytest.mark.parametrize(
        "cmd",
        [
            "echo bonjour",
            "ls -la /",
            "ls -la / | cat -e",
            "cat somefile",
            "ls somedir",
            "echo $FOO",
        ],
    )
    @pytest.mark.parametrize(
        "setup",
        [
            "echo bonjour > somefile",
            "mkdir somedir; echo bonjour > somedir/somefile",
        ],
    )
    @pytest.mark.parametrize(
        "exports",
        [
            {},
            {"FOO": "foo"}
        ],
    )
    def test_run_minishell_is_bash(self, monkeypatch, cmd, setup, exports):
        monkeypatch.setattr(Config, 'minishell_exec_path', Path("/bin/bash"))
        r = Test(cmd).run()
        assert r.passed

    @pytest.mark.parametrize(
        "setup",
        [
            ("exit 1", "no output"),
            ("echo '   ' ; exit 1", "no output"),
            ("echo bonjour ; exit 1", "bonjour"),
            ("echo aurevoir 2>&1 ; exit 1", "aurevoir"),
            ("echo bonjour; echo aurevoir 2>&1 ; exit 1", "bonjour\naurevoir"),
        ],
    )
    def test_run_bad_setup(self, setup):
        with pytest.raises(TestSetupException) as e:
            Test("yes", setup=setup[0]).run()
        assert setup[0] == e.value._setup
        assert "yes" == e.value._cmd
        assert f"Error: `{setup[0]}` setup command failed for `yes`\n\twith '{setup[1]}'" == e.value.__str__()

    def test_run_check_leaks(self, monkeypatch):
        monkeypatch.setattr(Config, 'check_leaks', True)
        monkeypatch.setattr(Config, 'valgrind_cmd', ["/bin/bash"])
        r = Test("echo bonjour").run()
        assert isinstance(r, LeakResult)
        assert "bonjour\n" == r._captured.output
        assert "echo bonjour" == r._cmd

    @pytest.mark.parametrize("timeout", [0.05, 0.1, 0.15, 0.2, 0.3])
    def test_run_timeout(self, monkeypatch, timeout):
        monkeypatch.setattr(Config, 'minishell_exec_path', self.BIN_DIR / "minishell-timeout")
        r = Test("echo bonjour", timeout=timeout).run()
        assert "bonjour\n" == r.expected.output
        assert 0 == r.expected.status
        assert isinstance(r.actual, CapturedTimeout)

    @pytest.mark.parametrize("file", ["/dev/random", "/dev/urandom"])
    def test_run_decode_error(self, monkeypatch, file):
        monkeypatch.setattr(Config, 'minishell_exec_path', Path("/bin/bash"))
        r = Test(f"/usr/bin/head -c 100 {file}").run()
        assert r.expected.output.startswith("UNICODE DECODE ERROR: ")
        assert r.actual.output.startswith("UNICODE DECODE ERROR: ")
        assert 0 == r.expected.status
        assert 0 == r.actual.status

    def test_run_files(self, monkeypatch):
        monkeypatch.setattr(Config, 'minishell_exec_path', self.BIN_DIR / "minishell-file")
        r = Test("echo bonjour > bonjour", files=["bonjour", "aurevoir"]).run()
        assert CapturedCommand("", 0, ["bonjour\n", None]) == r.expected
        assert CapturedCommand("", 0, ["bonjour\n", "aurevoir\n"]) == r.actual
