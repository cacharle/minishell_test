# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    hooks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 16:10:20 by charles           #+#    #+#              #
#    Updated: 2021/02/28 12:06:14 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re

from minishell_test.config import Config


DISCARDED_TEXT = "DISCARDED BY TEST"


def sort_lines(output):
    """Sort lines of output"""
    return '\n'.join(sorted(output.split('\n')))


def error_line0(output):
    """Replace "/bin/bash: -c: line n:" by "minishell:" and delete the second line"""
    if not Config.check_error_messages:
        return DISCARDED_TEXT

    lines = output.split('\n')
    if len(lines) != 3:
        return output
    prefix = Config.shell_reference_prefix + "-c: "
    if not lines[0].startswith(prefix):
        return output
    return lines[0].replace(prefix, Config.minishell_prefix, 1) + "\n"


def discard(output):
    """Discard the output"""
    return DISCARDED_TEXT


def export_singleton(output):
    """Remove variable that are not set to anything in a call to export without arguments"""
    prefix = "export " if ("--posix" in Config.shell_reference_args) else "declare -x "
    return sort_lines(
        '\n'.join([line for line in output.split('\n')
                   if re.match("^{}[a-zA-Z_][a-zA-Z0-9_]*$".format(prefix), line) is None])
    )


def replace_double(s):
    """Replace double occurence of a string by one"""
    def hook(output):
        return output.replace(s + s, s)
    return hook


def error_eof_to_expected_token(output):
    return output.replace(
        "-c: line 1: syntax error: unexpected end of file",
        "syntax error expected token"
    )


def should_not_be(not_expected):
    def hook(output):
        if output == not_expected:
            return "OUTPUT SHOULD NOT BE " + output
        return DISCARDED_TEXT
    return hook


def platform_status(darwin_status, linux_status):
    def hook(status):
        if Config.platform == "darwin":
            return status
        elif Config.platform == "linux":
            return (darwin_status if status == linux_status else status)
        return status
    return hook


def linux_replace(f, t):
    def hook(output):
        if not Config.platform == "linux":
            return output
        return output.replace(f, t)
    return hook


is_directory = linux_replace("Is a directory", "is a directory")
shlvl_0_to_1 = linux_replace("SHLVL=0", "SHLVL=1")
delete_escape = linux_replace("\\", "")


def linux_discard(output):
    if not Config.platform == "linux":
        return output
    return DISCARDED_TEXT
