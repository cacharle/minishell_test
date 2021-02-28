# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_hooks.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/27 20:03:52 by cacharle          #+#    #+#              #
#    Updated: 2021/02/28 12:05:58 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import contextlib

from minishell_test.config import Config

from minishell_test.hooks import (
    sort_lines,
    error_line0,
    discard,
    export_singleton,
    replace_double,
    platform_status,
    linux_replace,
    error_eof_to_expected_token,
    linux_discard,
    should_not_be,
    DISCARDED_TEXT,
)

Config.init([])


@contextlib.contextmanager
def config_context(attr, value):
    prev = getattr(Config, attr)
    setattr(Config, attr, value)
    try:
        yield
    finally:
        setattr(Config, attr, prev)


def test_sort_lines():
    assert "a\nb\nc" == sort_lines("a\nb\nc")
    assert "a\nb\nc" == sort_lines("c\nb\na")
    assert "a\nb\nc" == sort_lines("b\na\nc")
    assert """\
EDITOR=vim
GNUPGHOME=/home/cacharle/.local/share/gnupg
JUPYTER_CONFIG_DIR=/home/cacharle/.config/jupyter
LESSHISTFILE=-
LESS_TERMCAP_se=[0m
LESS_TERMCAP_so=[01;33m
SHELL=/usr/bin/zsh
XDG_CONFIG_HOME=/home/cacharle/.config
XDG_DATA_HOME=/home/cacharle/.local/share
XMONAD_CONFIG_HOME=/home/cacharle/.config/xmonad
XMONAD_DATA_HOME=/home/cacharle/.local/share/xmonad
_=/usr/bin/env\
""" == sort_lines("""\
SHELL=/usr/bin/zsh
LESSHISTFILE=-
JUPYTER_CONFIG_DIR=/home/cacharle/.config/jupyter
XMONAD_CONFIG_HOME=/home/cacharle/.config/xmonad
XMONAD_DATA_HOME=/home/cacharle/.local/share/xmonad
LESS_TERMCAP_se=[0m
LESS_TERMCAP_so=[01;33m
XDG_DATA_HOME=/home/cacharle/.local/share
XDG_CONFIG_HOME=/home/cacharle/.config
GNUPGHOME=/home/cacharle/.local/share/gnupg
EDITOR=vim
_=/usr/bin/env\
""")


def test_error_line0():
    assert ""                                               == error_line0("")
    assert "foo"                                            == error_line0("foo")
    assert "a\nb"                                           == error_line0("a\nb")
    assert "a\nb\nc"                                        == error_line0("a\nb\nc")
    assert "minishell: bonjour\n"                           == error_line0(Config.shell_reference_prefix + "-c: bonjour\nfoo\n")
    assert "minishell: \n"                                  == error_line0(Config.shell_reference_prefix + "-c: \nfoo\n")
    assert Config.shell_reference_prefix + "-c:asdf\nfoo\n" == error_line0(Config.shell_reference_prefix + "-c:asdf\nfoo\n")


def test_discard():
    assert DISCARDED_TEXT == discard("")
    assert DISCARDED_TEXT == discard("foo")


def test_export_singleton():
    assert "" == export_singleton("declare -x IGOTNUMBERS42")
    assert "" == export_singleton("declare -x IGOTUNDERSCORE__")
    assert "" == export_singleton("declare -x I")
    assert "" == export_singleton("declare -x _")
    assert """\
declare -x XDG_SESSION_TYPE="tty"
declare -x XDG_VTNR="1"
declare -x XINITRC="/home/cacharle/.config/x11/xinitrc"
declare -x XMONAD_CACHE_HOME="/home/cacharle/.cache/xmonad"
declare -x XMONAD_DATA_HOME="/home/cacharle/.local/share/xmonad"
declare -x YSU_MESSAGE_POSITION="after"
declare -x YSU_VERSION="1.7.3"
declare -x ZDOTDIR="/home/cacharle/.config/zsh"\
""" == export_singleton("""\
declare -x XDG_SESSION_ID
declare -x XDG_SESSION_TYPE="tty"
declare -x XDG_VTNR="1"
declare -x XINITRC="/home/cacharle/.config/x11/xinitrc"
declare -x XMONAD_CACHE_HOME="/home/cacharle/.cache/xmonad"
declare -x XMONAD_CONFIG_HOME
declare -x XMONAD_DATA_HOME="/home/cacharle/.local/share/xmonad"
declare -x YSU_MESSAGE_POSITION="after"
declare -x YSU_VERSION="1.7.3"
declare -x ZDOTDIR="/home/cacharle/.config/zsh"\
""")

    with config_context("shell_reference_args", ["--posix"]):
        assert "" == export_singleton("export IGOTNUMBERS42")
        assert "" == export_singleton("export IGOTUNDERSCORE__")
        assert "" == export_singleton("export I")
        assert "" == export_singleton("export _")
        assert """\
export XDG_SESSION_TYPE="tty"
export XDG_VTNR="1"
export XINITRC="/home/cacharle/.config/x11/xinitrc"
export XMONAD_CACHE_HOME="/home/cacharle/.cache/xmonad"
export XMONAD_DATA_HOME="/home/cacharle/.local/share/xmonad"
export YSU_MESSAGE_POSITION="after"
export YSU_VERSION="1.7.3"
export ZDOTDIR="/home/cacharle/.config/zsh"\
""" == export_singleton("""\
export XDG_SESSION_ID
export XDG_SESSION_TYPE="tty"
export XDG_VTNR="1"
export XINITRC="/home/cacharle/.config/x11/xinitrc"
export XMONAD_CACHE_HOME="/home/cacharle/.cache/xmonad"
export XMONAD_CONFIG_HOME
export XMONAD_DATA_HOME="/home/cacharle/.local/share/xmonad"
export YSU_MESSAGE_POSITION="after"
export YSU_VERSION="1.7.3"
export ZDOTDIR="/home/cacharle/.config/zsh"\
""")


def test_replace_double():
    assert "/"    == replace_double("/")("//")
    assert "//"   == replace_double("/")("////")
    assert "////" == replace_double("/")("////////")
    assert ";"    == replace_double(";")(";;")
    assert ";;"   == replace_double(";")(";;;;")
    assert ";;;;" == replace_double(";")(";;;;;;;;")


def test_error_eof_to_expected_token():
    assert "syntax error expected token" == error_eof_to_expected_token("-c: line 1: syntax error: unexpected end of file")


def test_should_not_be():
    assert "OUTPUT SHOULD NOT BE "        == should_not_be("")("")
    assert "OUTPUT SHOULD NOT BE bonjour" == should_not_be("bonjour")("bonjour")
    assert DISCARDED_TEXT                 == should_not_be("foo")("")
    assert DISCARDED_TEXT                 == should_not_be("bar")("bonjour")


def test_platform_status():
    with config_context('platform', 'darwin'):
        assert 0 == platform_status(0, 1)(0)
        assert 1 == platform_status(42, 42)(1)
    with config_context('platform', 'linux'):
        assert 0 == platform_status(0, 1)(1)
        assert 42 == platform_status(0, 1)(42)
    with config_context('platform', 'foo'):
        assert 0 == platform_status(42, 42)(0)


def test_linux_replace():
    with config_context('platform', 'darwin'):
        assert "Is a directory" == linux_replace("Is a directory", "is a directory")("Is a directory")
        assert "SHLVL=0"        == linux_replace("SHLVL=0", "SHLVL=1")("SHLVL=0")
        assert "\\"             == linux_replace("\\", "")("\\")
    with config_context('platform', 'linux'):
        assert "is a directory" == linux_replace("Is a directory", "is a directory")("Is a directory")
        assert "SHLVL=1"        == linux_replace("SHLVL=0", "SHLVL=1")("SHLVL=0")
        assert ""               == linux_replace("\\", "")("\\")


def test_linux_discard():
    with config_context('platform', 'darwin'):
        assert ""    == linux_discard("")
        assert "foo" == linux_discard("foo")
    with config_context('platform', 'linux'):
        assert DISCARDED_TEXT == linux_discard("")
        assert DISCARDED_TEXT == linux_discard("foo")
