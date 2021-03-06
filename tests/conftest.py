import pytest

from minishell_test.config import Config
from minishell_test import colors


@pytest.fixture(autouse=True)
def config_init():
    colors.disable()
    Config.init([])
