# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    hooks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 16:10:20 by charles           #+#    #+#              #
#    Updated: 2021/02/27 20:54:14 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re

from minishell_test.config import Config


def sort_lines(output):
    """Sort lines of output"""
    return '\n'.join(sorted(output.split('\n')))


def error_line0(output):
    """Replace "/bin/bash: -c: line n:" by "minishell:" and delete the second line"""
    if not Config.check_error_messages:
        return "DISCARDED BY TEST"

    lines = output.split('\n')
    if len(lines) != 3:
        return output
    prefix = Config.shell_reference_prefix + "-c: "
    if not lines[0].startswith(prefix):
        return output
    return lines[0].replace(prefix, Config.minishell_prefix, 1) + "\n"


def discard(output):
    """Discard the output"""
    return "DISCARDED BY TEST"


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


def platform_status(darwin_status, linux_status, windows_status=None):
    def hook(status):
        if Config.platform == "darwin":
            return status
        elif Config.platform == "linux":
            return (darwin_status if status == linux_status else status)
        return status
    return hook


def linux_only(func):
    """ Decorator for hooks that only need to be executed on linux """
    def hook(output):
        if not Config.platform == "linux":
            return output
        return func(output)
    return hook


@linux_only
def is_directory(output):
    return output.replace("Is a directory", "is a directory")


@linux_only
def shlvl_0_to_1(output):
    return output.replace("SHLVL=0", "SHLVL=1")


@linux_only
def delete_escape(output):
    return output.replace("\\", "")


@linux_only
def linux_discard(output):
    return "DISCARDED BY MINISHELL TEST"


def error_eof_to_expected_token(output):
    return output.replace(
        "-c: line 1: syntax error: unexpected end of file",
        "syntax error expected token"
    )


def should_not_be(not_expected):
    def hook(output):
        if output == not_expected:
            return "OUTPUT SHOULD NOT BE " + output
        return "DISCARDED BY TEST"
    return hook
