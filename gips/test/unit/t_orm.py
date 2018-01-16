import os, fnmatch, datetime

import pytest

from gips.inventory import orm

"""Test inventory.orm.* for correctness."""

@pytest.mark.parametrize('setup_complete, use_orm, expected', (
    (False, True,  True),
    (False, False, False),
    (True,  True,  False),
    (True,  False, False),
))
def t_setup(mocker, setup_complete, use_orm, expected):
    """Test orm.setup() to confirm it only runs setup at the right times."""
    mocker.patch('gips.inventory.orm.setup_complete', setup_complete)
    m_use_orm = mocker.patch('gips.inventory.orm.use_orm')
    m_use_orm.return_value = use_orm
    m_django_setup = mocker.patch('gips.inventory.orm.django.setup')
    orm.setup()
    # confirm it ran/didn't run django.setup as expected, and confirm 
    # that the global var got set in any case
    assert expected == m_django_setup.called and orm.setup_complete
