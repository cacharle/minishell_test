# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    hooks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 16:10:20 by charles           #+#    #+#              #
#    Updated: 2021/02/05 15:13:30 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
import sys
import os

import minishell_test.config as config


def sort_lines(output):
    """Sort lines of output"""
    return '\n'.join(sorted(output.split('\n')))


def error_line0(output):
    """Replace "/bin/bash: -c: line 0:" by "minishell:" and delete the second line"""
    error_message = os.environ.get("MINISHELL_TEST_DONT_CHECK_ERROR_MESSAGE")
    if error_message is not None and error_message == "yes":
        return "DISCARDED BY TEST"

    lines = output.split('\n')
    if len(lines) != 3:
        return output
    prefix = "{}: -c: line 0: ".format(config.REFERENCE_PATH)
    if lines[0].find(prefix) != 0:
        return output
    return lines[0].replace(prefix, "minishell: ") + "\n"


def discard(output):
    """Discard the output"""
    return "DISCARDED BY TEST"


def export_singleton(output):
    """Remove variable that are not set to anything in a call to export without arguments"""
    prefix = "export " if ("--posix" in config.REFERENCE_ARGS) else "declare -x "
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
        if config.PLATFORM == "Darwin":
            return status
        elif config.PLATFORM == "Linux":
            return (darwin_status if status == linux_status else status)
        else:
            raise RuntimeError("This platform exit codes are not supported yet,"
                               "feel free to contact me to add it.")
            sys.exit(2)
        return status
    return hook


def is_directory(output):
    if config.PLATFORM == "Linux":
        return output.replace("Is a directory", "is a directory")
    else:
        return output


# def no_cd_too_many_arguments(output):
#     for i, line in output.split("\n"):
#         if line.find("too many arguments")


def shlvl_0_to_1(output):
    if config.PLATFORM == "Linux":
        return output.replace("SHLVL=0", "SHLVL=1")
    else:
        return output


def delete_escape(output):
    if config.PLATFORM == "Linux":
        return output.replace("\\", "")
    else:
        return output


def error_eof_to_expected_token(output):
    return output.replace(
        "-c: line 1: syntax error: unexpected end of file",
        "syntax error expected token"
    )


def linux_discard(output):
    if config.PLATFORM == "Linux":
        return "DISCARDED BY MINISHELL TEST"
    else:
        return output


def should_not_be(not_expected):
    def hook(output):
        if output == not_expected:
            return "OUTPUT SHOULD NOT BE " + output
        return "DISCARDED BY TEST"
    return hook
