# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <charles.cabergs@gmail.com>        +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/07/15 18:24:19 by charles           #+#    #+#              #
#    Updated: 2020/09/11 14:21:14 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #


################################################################################
# Minishell configuration file                                                 #
################################################################################

import os

# run the bonus tests
BONUS = False

# minishell dir path
MINISHELL_DIR = ".."

# minishell executable
MINISHELL_EXEC = "minishell"

# make minishell before executing the test if set to True
MINISHELL_MAKE = True

# path to reference shell (shell which will be compared minishell)
# has to support the -c option (sh, bash and zsh support it)
REFERENCE_PATH = "/bin/bash"

# log file path
LOG_PATH = "result.log"

# path to the sandbox directory
# WARNING: will be rm -rf so be careful
SANDBOX_PATH = "sandbox"

# where the availables commands are stored
EXECUTABLES_PATH = "./bin"

# commands available in test"
AVAILABLE_COMMANDS = ["rmdir", "env", "cat", "touch", "ls", "grep", "sh"]

# $PATH environment variable passed to the shell
PATH_VARIABLE = os.path.abspath(EXECUTABLES_PATH)

# default test timeout
TIMEOUT = 1

LOREM = """
Mollitia asperiores assumenda excepturi et ipsa. Nihil corporis facere aut a rem consequatur.
Quas molestiae corporis et quibusdam maiores. Molestiae sed unde aut at sed.
Deserunt quidem quidem aspernatur pariatur vel illum voluptatum. Culpa unde dolor aspernatur sit.
Mollitia tenetur sed eaque autem placeat a aut in. Ipsam ea consequuntur omnis.
Non et qui vel corrupti similique eum aut voluptatibus. Iste consequatur voluptatum et omnis debitis.
Sit quia neque nihil consequatur sint. Velit libero ut aut et et rerum.
Placeat cumque incidunt non repellat sunt perspiciatis ullam.
Repellendus repudiandae nostrum quia quis corrupti.
Rerum veniam earum cumque pariatur accusantium voluptatum omnis.
Alias ut et et adipisci. Tempore omnis numquam ullam et animi et eveniet.
Dolor itaque distinctio in. Magnam rerum quia est laboriosam repellat perspiciatis eos.
Consequuntur quae corrupti atque. Numquam enim ut ut.
Perspiciatis ut maxime et libero quo voluptas consequatur illum. Pariatur porro dolor cumque molestiae harum.
"""
LOREM = ' '.join(LOREM.split('\n'))

###############################################################################
# do not edit
###############################################################################

MINISHELL_PATH = os.path.abspath(
    os.path.join(MINISHELL_DIR, MINISHELL_EXEC)
)

# 0, 1, 2
VERBOSE_LEVEL = 1

MINISHELL_ERROR_BEGIN = os.path.basename(MINISHELL_PATH) + ": "
REFERENCE_ERROR_BEGIN = REFERENCE_PATH + ": line 0: "
