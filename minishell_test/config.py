# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/26 09:40:36 by cacharle          #+#    #+#              #
#    Updated: 2021/02/28 11:19:13 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import configparser
import inspect
import shutil
import distutils
from pathlib import Path
from typing import cast, List, Tuple

import minishell_test.data
from minishell_test.args import parse_args


DATA_DIR = Path(inspect.getfile(minishell_test.data)).parent
CONFIG_FILENAME = Path('minishell_test.cfg')


class ConfigParser(configparser.ConfigParser):
    BOOLEAN_STATES = {'true': True, 'false': False}

    def __init__(self):
        super().__init__()

    def getpath(self, section, options):
        return Path(self.get(section, options)).resolve()

    def getargs(self, section, options):
        value = self.get(section, options)
        return value.strip().split(' ') if len(value) != 0 else []

    def getmultiline(self, section, options):
        return self.get(section, options).strip().split('\n')


class Config():
    minishell_dir                = cast(Path, None)
    bonus                        = cast(bool, None)
    exec_name                    = cast(str, None)
    make                         = cast(bool, None)
    make_args                    = cast(List[str], None)
    pager                        = cast(bool, None)
    pager_prog                   = cast(Path, None)
    log_path                     = cast(Path, None)
    check_error_messages         = cast(bool, None)
    shell_available_commands     = cast(List[str], None)
    shell_path_variable          = cast(str, None)
    shell_reference_path         = cast(Path, None)
    shell_reference_args         = cast(List[str], None)
    timeout_test                 = cast(float, None)
    timeout_leaks                = cast(float, None)
    cache_dir                    = cast(Path, None)
    sandbox_dir                  = cast(Path, None)
    shell_available_commands_dir = cast(Path, None)
    lorem                        = cast(str, None)
    minishell_exec_path          = cast(Path, None)
    minishell_prefix             = cast(str, None)
    shell_reference_prefix       = cast(str, None)
    exit_first                   = cast(bool, None)
    range                        = cast(Tuple[int, int], None)
    check_leaks                  = cast(bool, None)
    show_range                   = cast(bool, None)
    valgrind_cmd                 = cast(List[str], None)
    term_cols                    = cast(int, None)
    platform                     = cast(str, None)

    @classmethod
    def init(cls, args):
        if isinstance(args, list):
            args = parse_args(args)

        cls.minishell_dir = Path(args.path).resolve()

        cfg = cls._load_cfg()

        cls.bonus                    = cfg.getboolean('minishell_test', 'bonus')
        cls.exec_name                = cfg.get('minishell_test', 'exec_name')
        cls.make                     = cfg.getboolean('minishell_test', 'make')
        cls.make_args                = cfg.getargs('minishell_test', 'make_args')
        cls.pager                    = cfg.getboolean('minishell_test', 'pager')
        cls.pager_prog               = cfg.get('minishell_test', 'pager_prog')
        cls.log_path                 = cfg.getpath('minishell_test', 'log_path')
        cls.check_error_messages     = cfg.getboolean('minishell_test', 'check_error_messages')

        cls.shell_available_commands = cfg.getmultiline('shell', 'available_commands')
        cls.shell_path_variable      = cfg.get('shell', 'path_variable')

        cls.shell_reference_path     = cfg.getpath('shell:reference', 'path')
        cls.shell_reference_args     = cfg.getargs('shell:reference', 'args')

        cls.timeout_test             = cfg.getfloat('timeout', 'test')
        cls.timeout_leaks            = cfg.getfloat('timeout', 'leaks')

        xdg_cache_home = os.environ.get('XDG_CACHE_HOME')
        home = os.environ.get('HOME')
        if xdg_cache_home is not None:
            cls.cache_dir = Path(xdg_cache_home) / 'minishell_test'
        elif home is not None:
            cls.cache_dir = Path(home) / '.cache' / 'minishell_test'
        else:
            cls.cache_dir = Path('.cache', 'minishell_test')

        cls.sandbox_dir                  = cls.cache_dir / 'sandbox'
        cls.shell_available_commands_dir = cls.cache_dir / 'bin'

        cls.shell_path_variable = cls.shell_path_variable.format(shell_available_commands_dir=cls.shell_available_commands_dir)

        with open(DATA_DIR / 'lorem') as f:
            cls.lorem = ' '.join(f.read().split('\n'))

        cls.minishell_exec_path = cls.minishell_dir / cls.exec_name

        cls.minishell_prefix = cls.exec_name + ": "
        cls.shell_reference_prefix = str(cls.shell_reference_path) + ": "

        cls.exit_first = args.exit_first
        cls.range = args.range
        cls.check_leaks = args.check_leaks

        if cls.range is not None or cls.check_leaks:
            cls.show_range = True
        else:
            cls.show_range = args.show_range

        if cls.check_leaks:
            valgrind_path = distutils.spawn.find_executable("valgrind")
            if valgrind_path is None:
                raise RuntimeError("could not find valgrind command on your system")
            cls.valgrind_cmd = [
                str(valgrind_path),
                "--trace-children=no",
                "--leak-check=yes",
                "--child-silent-after-fork=yes",
                "--show-leak-kinds=definite",
                str(cls.minishell_exec_path),
            ]

        cls.term_cols = shutil.get_terminal_size().columns
        if cls.term_cols < 40:
            raise RuntimeError("You're terminal isn't wide enough 40 cols minimum required")

        cls.platform = sys.platform
        supported = ['linux', 'darwin']
        if cls.platform not in supported:
            raise RuntimeError("Your platform ({cls.platform}) is not supported, supported platforms are: {', '.join(supported)}")

    @classmethod
    def _load_cfg(cls):
        cfg = ConfigParser()
        cfg.read(DATA_DIR / 'default.cfg')
        user_cfg = ConfigParser()
        user_cfg.read(cls.minishell_dir / CONFIG_FILENAME)  # if file doesn't exists, returns []

        for section in user_cfg:
            if section not in cfg:
                raise RuntimeError(f"Unknown section name: {section}")
            for key in user_cfg[section]:
                if key not in cfg[section]:
                    raise RuntimeError(f"Unknown key name: {key}")

        cfg.read_dict({**cfg, **user_cfg})
        return cfg
