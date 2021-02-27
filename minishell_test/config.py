# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/26 09:40:36 by cacharle          #+#    #+#              #
#    Updated: 2021/02/27 12:18:55 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import sys
import configparser
import inspect
import shutil
import distutils
from pathlib import Path

import minishell_test.data
from minishell_test.args import parse_args


DATA_DIR        = Path(inspect.getfile(minishell_test.data)).parent
CONFIG_FILENAME = Path('minishell_test.cfg')

config = configparser.ConfigParser()
config.read(DATA_DIR / 'default.cfg')

# TODO check user_config for unkown stuff
user_config = configparser.ConfigParser()
user_config.read(Path(".") / CONFIG_FILENAME)
config.read_dict({**config, **user_config})

args = parse_args()

BONUS                    = config.getboolean('minishell_test', 'bonus')
EXEC_NAME                = Path(config.get('minishell_test', 'exec_name'))
MAKE                     = config.getboolean('minishell_test', 'make')
PAGER                    = config.getboolean('minishell_test', 'pager')
PAGER_PROG               = config.get('minishell_test', 'pager_prog')
LOG_PATH                 = Path(config.get('minishell_test', 'log_path'))

SHELL_AVAILABLE_COMMANDS = config.get('shell', 'available_commands').strip().split('\n')
SHELL_PATH_VARIABLE      = config.get('shell', 'path_variable')

SHELL_REFERENCE_PATH     = Path(config.get('shell:reference', 'path'))

reference_args = config.get('shell:reference', 'args')
SHELL_REFERENCE_ARGS = reference_args.strip().split(' ') if len(reference_args) != 0 else []

TIMEOUT_TEST             = config.getfloat('timeout', 'test')
TIMEOUT_LEAKS            = config.getfloat('timeout', 'leaks')


xdg_cache_home = os.environ.get('XDG_CACHE_HOME')
home = os.environ.get('HOME')
if xdg_cache_home is not None:
    CACHE_DIR = Path(xdg_cache_home) / 'minishell_test'
elif home is not None:
    CACHE_DIR = Path(home) / '.cache' / 'minishell_test'
else:
    CACHE_DIR = Path('.cache', 'minishell_test')

SANDBOX_DIR            = CACHE_DIR / 'sandbox'
SHELL_AVAILABLE_COMMANDS_DIR = CACHE_DIR / 'bin'

SHELL_PATH_VARIABLE = SHELL_PATH_VARIABLE.format(shell_available_commands_dir=SHELL_AVAILABLE_COMMANDS_DIR)

with open(DATA_DIR / 'lorem') as f:
    LOREM = ' '.join(f.read().split('\n'))

MINISHELL_DIR       = Path(args.path)
MINISHELL_EXEC_PATH = MINISHELL_DIR / EXEC_NAME

EXIT_FIRST = args.exit_first
RANGE = args.range
CHECK_LEAKS = args.check_leaks

if RANGE is not None or CHECK_LEAKS:
    SHOW_RANGE = True
else:
    SHOW_RANGE = args.show_range

if CHECK_LEAKS:
    valgrind_path = distutils.spawn.find_executable("valgrind")
    if valgrind_path is None:
        raise RuntimeError("Could not find valgrind command on your system")
    VALGRIND_CMD = [
        str(valgrind_path),
        "--trace-children=no",
        "--leak-check=yes",
        "--child-silent-after-fork=yes",
        "--show-leak-kinds=definite",
        str(MINISHELL_EXEC_PATH),
    ]

TERM_COLS = shutil.get_terminal_size().columns
if TERM_COLS < 40:
    raise RuntimeError("You're terminal isn't wide enough 40 cols minimum required")

PLATFORM = sys.platform
supported = ['linux', 'darwin']
if PLATFORM not in supported:
    raise RuntimeError("Your platform ({PLATFORM}) is not supported, supported platforms are: {', '.join(supported)}")
