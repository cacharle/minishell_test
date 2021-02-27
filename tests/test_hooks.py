# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_hooks.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/27 20:03:52 by cacharle          #+#    #+#              #
#    Updated: 2021/02/27 20:44:22 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import pytest

from minishell_test import config

from minishell_test.hooks import (
    sort_lines,
    error_line0,
    discard,
    export_singleton,
    replace_double,
    platform_status,
    is_directory,
    shlvl_0_to_1,
    delete_escape,
    error_eof_to_expected_token,
    linux_discard,
    should_not_be,
)


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


@pytest.mark.skip()
def test_error_line0():
    pass


def test_discard():
    assert "DISCARDED BY TEST" == discard("")
    assert "DISCARDED BY TEST" == discard("foo")


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

    prev = config.SHELL_REFERENCE_ARGS
    config.SHELL_REFERENCE_ARGS = ['--posix']
    try:
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
    finally:
        config.SHELL_REFERENCE_ARGS = prev


def test_replace_double():
    assert "/"    == replace_double("/")("//")
    assert "//"   == replace_double("/")("////")
    assert "////" == replace_double("/")("////////")
    assert ";"    == replace_double(";")(";;")
    assert ";;"   == replace_double(";")(";;;;")
    assert ";;;;" == replace_double(";")(";;;;;;;;")


@pytest.mark.skip()
def test_platform_status():
    pass

@pytest.mark.skip()
def test_is_directory():
    pass

@pytest.mark.skip()
def test_shlvl_0_to_1():
    pass

@pytest.mark.skip()
def test_delete_escape():
    pass

def test_error_eof_to_expected_token():
    assert "syntax error expected token" == error_eof_to_expected_token("-c: line 1: syntax error: unexpected end of file")

@pytest.mark.skip()
def test_linux_discard():
    pass

@pytest.mark.skip()
def test_should_not_be():
    pass
