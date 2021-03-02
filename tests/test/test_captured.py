# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_captured.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/01 15:55:11 by cacharle          #+#    #+#              #
#    Updated: 2021/03/02 10:14:23 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import pytest
import copy

from minishell_test.test.captured import CapturedCommand, CapturedTimeout


@pytest.fixture
def captured():
    return CapturedCommand("foo", 0, ["file1", "file2"])


def test_init(captured):
    assert "foo"              == captured.output
    assert 0                  == captured.status
    assert ["file1", "file2"] == captured.files_content


def test_eq(captured):
    assert captured != 42
    assert captured != "bonjour"
    assert captured == captured
    c2 = copy.deepcopy(captured)
    assert captured == c2
    c2.output = "bar"
    assert captured != c2
    c2 = copy.deepcopy(captured)
    c2.status = 42
    assert captured != c2
    c2 = copy.deepcopy(captured)
    c2.files_content = ["asdfasdf"]
    assert captured != c2
    assert captured != CapturedTimeout()
    assert CapturedTimeout() == CapturedTimeout()
