# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_sandbox.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/03 08:09:00 by cacharle          #+#    #+#              #
#    Updated: 2021/03/06 09:58:17 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import pytest
import shutil
from pathlib import Path

from minishell_test import sandbox
from minishell_test.config import Config

Config.init([])


@pytest.fixture
def sandbox_dirs():
    return [Path(s) for s in [
        "foo",
        "asdfasdfas;dlkfjas;dkfjas;lkdfj",
        "z/y",
        "a/b/c/d/e/f/g/h/i/j/k/l/m/n/o/p/q/r/s/t/u/v/w/x/y/z",
    ]]


def test_create(tmpdir, monkeypatch, sandbox_dirs):
    for sandbox_dir in sandbox_dirs:
        sandbox_dir = Path(tmpdir / sandbox_dir)
        monkeypatch.setattr(Config, 'sandbox_dir', sandbox_dir)
        assert not sandbox_dir.exists()
        sandbox.create()
        assert sandbox_dir.exists()


def test_remove(tmpdir, monkeypatch, sandbox_dirs):
    for sandbox_dir in sandbox_dirs:
        sandbox_dir = Path(tmpdir / sandbox_dir)
        monkeypatch.setattr(Config, 'sandbox_dir', sandbox_dir)
        sandbox.create()
        assert sandbox_dir.exists()
        sandbox.remove()
        assert not sandbox_dir.exists()
    for sandbox_dir in sandbox_dirs:
        sandbox_dir = Path(tmpdir / sandbox_dir)
        monkeypatch.setattr(Config, 'sandbox_dir', sandbox_dir)
        sandbox.create()
        assert sandbox_dir.exists()
        sandbox_dir.chmod(000)
        sandbox.remove()
        assert not sandbox_dir.exists()
    for sandbox_dir in sandbox_dirs:
        sandbox_dir = Path(tmpdir / sandbox_dir)
        monkeypatch.setattr(Config, 'sandbox_dir', sandbox_dir)
        sandbox.create()
        assert sandbox_dir.exists()
        shutil.rmtree(sandbox_dir)
        sandbox.remove()
        assert not sandbox_dir.exists()


def test_context(tmpdir, monkeypatch, sandbox_dirs):
    for sandbox_dir in sandbox_dirs:
        sandbox_dir = Path(tmpdir / sandbox_dir)
        monkeypatch.setattr(Config, 'sandbox_dir', sandbox_dir)
        assert not sandbox_dir.exists()
        with sandbox.context():
            assert sandbox_dir.exists()
        assert not sandbox_dir.exists()
    for sandbox_dir in sandbox_dirs:
        sandbox_dir = Path(tmpdir / sandbox_dir)
        monkeypatch.setattr(Config, 'sandbox_dir', sandbox_dir)
        with pytest.raises(RuntimeError):
            assert not sandbox_dir.exists()
            with sandbox.context():
                assert sandbox_dir.exists()
                raise RuntimeError
            assert not sandbox_dir.exists()
