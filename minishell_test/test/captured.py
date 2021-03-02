# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    captured.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/11 12:16:25 by charles           #+#    #+#              #
#    Updated: 2021/03/02 10:32:19 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from typing import List, Optional, Union


class CapturedCommand:
    def __init__(
        self,
        output: str,
        status: int,
        files_content: List[Optional[str]],
    ):
        """Captured command

        :param output:
            Command output
        :param status:
            Command return status code
        :param files_content:
            Content of the files altered by the command
        """

        self.output = output
        self.status = status
        self.files_content = files_content

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CapturedCommand):
            return False
        return (
            self.output == other.output and
            self.status == other.status and
            all(x == y for x, y in zip(self.files_content, other.files_content))
        )


class CapturedTimeout():
    """Captured timeout"""

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CapturedTimeout)


CapturedType = Union[CapturedCommand, CapturedTimeout]
