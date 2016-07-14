import logging

import pytest

from .util import *


def t_info(repo_env, expected):
    """Test `gips_info modis` and confirm recorded output is given."""
    actual = repo_env.run('gips_info', 'landsat')
    assert expected == actual
