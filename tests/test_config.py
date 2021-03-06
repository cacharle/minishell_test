# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_config.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/03 12:25:29 by cacharle          #+#    #+#              #
#    Updated: 2021/03/06 10:11:30 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import pytest
from pathlib import Path
import contextlib
import distutils.spawn
import shutil

from minishell_test import config
from minishell_test.config import (
    Config,
    ConfigSetupException,
    ConfigParser,
    ConfigParserException,
)


Config.init([])


class TestConfigParser:
    @pytest.fixture
    def config(self):
        c = ConfigParser()
        c.read_dict({
            "general": {
                "somepath": "bonjour/je/suis",
                "someargs": "bonjour je suis",
                "someargs_spaces": "bonjour   je   suis",
                "someargs_around": "  bonjour   je   suis  ",
                "someargs_spaces_only": "    ",
                "someargs_none": "",
                "somemultiline": "bonjour\nje\nsuis",
                "somemultiline_around": "\n\n  bonjour\nje\nsuis\n\n",
                "somemultiline_crlf": "bonjour\r\nje\r\nsuis",
                "somemultiline_sep_only": "\n\n  \n\n",
                "somemultiline_none": "",
            }
        })
        return c

    def test_getpath(self, config):
        p = config.getpath("general", "somepath")
        assert isinstance(p, Path)
        assert Path("bonjour/je/suis").resolve() == p

    def test_getargs(self, config):
        assert ["bonjour", "je", "suis"] == config.getargs("general", "someargs")
        assert ["bonjour", "je", "suis"] == config.getargs("general", "someargs_spaces")
        assert ["bonjour", "je", "suis"] == config.getargs("general", "someargs_around")
        assert [] == config.getargs("general", "someargs_spaces_only")
        assert [] == config.getargs("general", "someargs_none")

    def test_getmultiline(self, config):
        assert ["bonjour", "je", "suis"] == config.getmultiline("general", "somemultiline")
        assert ["bonjour", "je", "suis"] == config.getmultiline("general", "somemultiline_around")
        assert ["bonjour", "je", "suis"] == config.getmultiline("general", "somemultiline_crlf")
        assert [] == config.getmultiline("general", "somemultiline_sep_only")
        assert [] == config.getmultiline("general", "somemultiline_none")


class TestConfig:
    # @pytest.fixture
    # def default_config(self):
    #     c = ConfigParser()
    #     c.read(config.DATA_DIR / 'default.cfg')
    #     return c
    #
    # @pytest.mark.parametrize(
    #     "config_dict",
    #     [
    #         {"minishell_test": {"bonus": True}},
    #         {"minishell_test": {"bonus": True}},
    #     ]
    # )
    # def test_load_cfg_defaults(self, tmpdir, config_dict, default_config):
    #     c = ConfigParser()
    #     c.read_dict(config_dict)
    #     for suite in default_config:
    #         for key in default_config:



    @pytest.mark.parametrize(
        "file_content",
        [
            ("foo", "[{}]\nbonus = true"),
            ("minishell_test ", "[{}]\nbonus = true"),
            (" minishell_test", "[{}]\nbonus = true"),
            (" minishell_test ", "[{}]\nbonus = true"),
            ("minishell_tes", "[{}]\nbonus = true"),
            ("inishell_test", "[{}]\nbonus = true"),
            ("shell_", "[{}]\nbonus = true"),
            ("she ll", "[{}]\nbonus = true"),
            ("shell:reference ", "[{}]\nbonus = true"),
            ("timout", "[{}]\nbonus = true"),
        ]
    )
    def test_load_cfg_unknown_section(self, tmpdir, file_content):
        with open(tmpdir / config.CONFIG_FILENAME, "w") as file:
            file.write(file_content[1].format(file_content[0]))
        with pytest.raises(ConfigParserException) as e:
            Config.init(["--path", str(tmpdir)])
        assert file_content[0] == e.value._section
        assert e.value._key is None
        assert f"Configuration parsing error: unknown section name: {file_content[0]}" == e.value.__str__()

    @pytest.mark.parametrize(
        "file_content",
        [
            ("minishell_test", "bonu", "[{}]\n{} = true"),
            ("minishell_test", "exec name", "[{}]\n{} = hello"),
            ("minishell_test", "log_pat", "[{}]\n{} = a/b/c"),
            ("minishell_test", "ager_prog", "[{}]\n{} = a/b/c"),
            ("shell", "available_command", "[{}]\n{} = a/b/c"),
            ("shell:reference", "pa", "[{}]\n{} = /bin/sh"),
        ]
    )
    def test_load_cfg_unknown_section_key(self, tmpdir, file_content):
        with open(tmpdir / config.CONFIG_FILENAME, "w") as file:
            file.write(file_content[2].format(file_content[0], file_content[1]))
        with pytest.raises(ConfigParserException) as e:
            Config.init(["--path", str(tmpdir)])
        assert file_content[0] == e.value._section
        assert file_content[1] == e.value._key
        assert f"Configuration parsing error: unknown key name: {file_content[1]} in {file_content[0]}" == e.value.__str__()

    def test_init_cache_dir_xdg_cache_home(self, monkeypatch):
        monkeypatch.setenv("XDG_CACHE_HOME", "bonjour")
        Config.init([])
        assert Path("bonjour", "minishell_test") == Config.cache_dir

    def test_init_cache_dir_xdg_cache_home_missing(self, monkeypatch):
        monkeypatch.delenv("XDG_CACHE_HOME")
        Config.init([])
        assert Path("~", ".cache", "minishell_test").expanduser() == Config.cache_dir

    def test_init_cache_dir_home(self, monkeypatch):
        monkeypatch.delenv("XDG_CACHE_HOME")
        monkeypatch.setenv("HOME", "bonjour")
        Config.init([])
        assert Path("bonjour", ".cache", "minishell_test") == Config.cache_dir

    def test_init_cache_dir_home_missing(self, monkeypatch):
        monkeypatch.delenv("XDG_CACHE_HOME")
        monkeypatch.delenv("HOME")
        Config.init([])
        assert Path(".cache", "minishell_test") == Config.cache_dir

    def test_init_show_range(self):
        Config.init([])
        assert not Config.show_range
        Config.init(["--show-range"])
        assert Config.show_range
        Config.init(["--check-leaks"])
        assert Config.show_range
        Config.init(["--range", "1", "100"])
        assert Config.show_range

    def test_init_valgrind_not_found(self, monkeypatch):
        monkeypatch.setattr(distutils.spawn, "find_executable", lambda _: None)
        with pytest.raises(ConfigSetupException) as e:
            Config.init(["--check-leaks"])
        assert "Could not find the valgrind command on your system" == e.value.__str__()

    def test_init_term_cols_too_low(self, monkeypatch):
        def mock_get_terminal_size(fallback=None):
            # has to support fallback since pytest uses this function during the verbose test
            if fallback is not None:
                return os.terminal_size(fallback)
            return os.terminal_size((39, 80))
        monkeypatch.setattr(shutil, "get_terminal_size", mock_get_terminal_size)
        with pytest.raises(ConfigSetupException) as e:
            Config.init(["--check-leaks"])
        assert "You're terminal isn't wide enough 40 cols minimum required" == e.value.__str__()

    def test_platform_not_supported(self, monkeypatch):
        monkeypatch.setattr(sys, "platform", "windows")
        with pytest.raises(ConfigSetupException) as e:
            Config.init(["--check-leaks"])
        assert "Your platform (windows) is not supported, supported platforms are: linux, darwin" == e.value.__str__()
