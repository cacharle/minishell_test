# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    hooks.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 16:10:20 by charles           #+#    #+#              #
#    Updated: 2020/09/11 17:06:03 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import config


def sort_lines(output):
    return '\n'.join(sorted(output.split('\n')))

def error_line0(output):
    lines = output.split('\n')
    if len(lines) != 3:
        return output
    prefix = "{}: -c: line 0: ".format(config.REFERENCE_PATH)
    if lines[0].find(prefix) != 0:
        return output
    return lines[0].replace(prefix, "minishell: ") + "\n"

def discard(output):
    return "DISCARDED BY TEST"
