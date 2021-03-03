# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_colors.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/03/03 07:56:43 by cacharle          #+#    #+#              #
#    Updated: 2021/03/03 10:00:43 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import pytest

from minishell_test import colors


@pytest.fixture
def texts():
    return [
        "",
        "foo",
        "aslkdfj;asdkflaskdjfalskdjflasdf",
        "\n\n\n\n",
        "\t\t\t\t",
    ]


def test_green(texts):
    colors.enable()
    for text in texts:
        assert colors._DEFAULTS["green"] + text + colors._DEFAULTS["close"] == colors.green(text)


def test_red(texts):
    colors.enable()
    for text in texts:
        assert colors._DEFAULTS["red"] + text + colors._DEFAULTS["close"] == colors.red(text)


def test_blue(texts):
    colors.enable()
    for text in texts:
        assert colors._DEFAULTS["blue"] + text + colors._DEFAULTS["close"] == colors.blue(text)


def test_bold(texts):
    colors.enable()
    for text in texts:
        assert colors._DEFAULTS["bold"] + text + colors._DEFAULTS["close"] == colors.bold(text)


def test_toggling(texts):
    colors.disable()
    for text in texts:
        assert text == colors.green(text)
        assert text == colors.red(text)
        assert text == colors.blue(text)
        assert text == colors.bold(text)
    colors.enable()
    for text in texts:
        assert text != colors.green(text)
        assert text != colors.red(text)
        assert text != colors.blue(text)
        assert text != colors.bold(text)
    colors.disable()
