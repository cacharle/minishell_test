# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    captured.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:16:25 by charles           #+#    #+#              #
#    Updated: 2021/03/01 16:02:26 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
from typing import List, Optional

from minishell_test.config import Config


class Captured:
    def __init__(
        self,
        output: str,
        status: int,
        files_content: List[Optional[str]],
        is_timeout: bool = False
    ):
        """Captured class
           output:        captured content
           status:        command status
           files_content: content of the files altered by the command
           is_timeout:    the command has timed out
        """

        self.output = output
        self.status = status
        self.files_content = files_content
        self.is_timeout = is_timeout

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Captured):
            raise NotImplementedError
        if self.is_timeout:
            return self.is_timeout == other.is_timeout
        return (self.output == other.output and
                self.status == other.status and
                all(x == y for x, y in zip(self.files_content, other.files_content)))

    @staticmethod
    def timeout():
        """Create a new captured timeout"""
        return Captured("", 0, [], is_timeout=True)
