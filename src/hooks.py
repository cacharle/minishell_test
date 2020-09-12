# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    hooks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 16:10:20 by charles           #+#    #+#              #
#    Updated: 2020/09/12 10:37:16 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import regex

import config


def sort_lines(output):
    """Sort lines of output"""
    return '\n'.join(sorted(output.split('\n')))


def error_line0(output):
    """Replace "/bin/bash: -c: line 0:" by "minishell:" and delete the second line"""
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
                   if regex.match("^{}.+=\".*\"$".format(prefix), line) is not None])
    )
