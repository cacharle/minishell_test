# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    hooks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 16:10:20 by charles           #+#    #+#              #
#    Updated: 2021/02/27 15:40:25 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re

from minishell_test import config


def sort_lines(output):
    """Sort lines of output"""
    return '\n'.join(sorted(output.split('\n')))


def error_line0(output):
    """Replace "/bin/bash: -c: line n:" by "minishell:" and delete the second line"""
    if not config.CHECK_ERROR_MESSAGES:
        return "DISCARDED BY TEST"

    lines = output.split('\n')
    if len(lines) != 3:
        return output
    prefix = config.SHELL_REFERENCE_PREFIX + "-c: "
    if not lines[0].startswith(prefix):
        return output
    return lines[0].replace(prefix, config.MINISHELL_PREFIX, 1) + "\n"


def discard(output):
    """Discard the output"""
    return "DISCARDED BY TEST"


def export_singleton(output):
    """Remove variable that are not set to anything in a call to export without arguments"""
    prefix = "export " if ("--posix" in config.SHELL_REFERENCE_ARGS) else "declare -x "
    return sort_lines(
        '\n'.join([line for line in output.split('\n')
                   if re.match("^{}[a-zA-Z]+$".format(prefix), line) is None])
    )


def replace_double_slash(output):
    """Replace occurence of double slash by one"""
    return output.replace("//", "/")


def replace_double_semi_colon(output):
    """Replace occurence of double semi-colon by one"""
    return output.replace(";;", ";")


def platform_status(darwin_status, linux_status, windows_status=None):
    def hook(status):
        if config.PLATFORM == "darwin":
            return status
        elif config.PLATFORM == "linux":
            return (darwin_status if status == linux_status else status)
        return status
    return hook


def is_directory(output):
    if config.PLATFORM == "linux":
        return output.replace("Is a directory", "is a directory")
    else:
        return output


# def no_cd_too_many_arguments(output):
#     for i, line in output.split("\n"):
#         if line.find("too many arguments")


def shlvl_0_to_1(output):
    if config.PLATFORM == "linux":
        return output.replace("SHLVL=0", "SHLVL=1")
    else:
        return output


def delete_escape(output):
    if config.PLATFORM == "linux":
        return output.replace("\\", "")
    else:
        return output


def error_eof_to_expected_token(output):
    return output.replace(
        "-c: line 1: syntax error: unexpected end of file",
        "syntax error expected token"
    )


def linux_discard(output):
    if config.PLATFORM == "linux":
        return "DISCARDED BY MINISHELL TEST"
    else:
        return output


def should_not_be(not_expected):
    def hook(output):
        if output == not_expected:
            return "OUTPUT SHOULD NOT BE " + output
        return "DISCARDED BY TEST"
    return hook
