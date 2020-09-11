# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    captured.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:16:25 by charles           #+#    #+#              #
#    Updated: 2020/09/11 20:08:00 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import config


class Captured:
    def __init__(self, output: str, status: int, files_content: [str], is_timeout: bool = False):
        lines = output.split('\n')
        for i, l in enumerate(lines):
            if l.find(config.REFERENCE_ERROR_BEGIN) == 0:
                lines[i] = l.replace(config.REFERENCE_ERROR_BEGIN, config.MINISHELL_ERROR_BEGIN, 1)
            elif l.find(config.REFERENCE_PATH + ": ") == 0:
                lines[i] = l.replace(config.REFERENCE_PATH + ": ", config.MINISHELL_ERROR_BEGIN, 1)

        self.output = '\n'.join(lines)

        self.status = status
        self.files_content = files_content
        self.is_timeout = is_timeout

    def __eq__(self, other: 'Captured') -> bool:
        if self.is_timeout:
            return self.is_timeout == other.is_timeout
        return (self.output == other.output
                and self.status == other.status
                and all([x == y for x, y in zip(self.files_content, other.files_content)]))

    @staticmethod
    def timeout():
        return Captured("", 0, [], is_timeout=True)
