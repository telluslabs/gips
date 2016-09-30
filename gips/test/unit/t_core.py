"""Unit tests for core functions, such as those found in gips.core and gips.data.core."""

import sys
from datetime import datetime

import pytest
import mock

import gips
from gips.data.landsat.landsat import landsatRepository, landsatData
from gips.inventory import dbinv

def t_version_override(mocker):
    """Test gips.__init__.detect_version() for correct override of __version__."""
    env = mocker.patch.object(gips.os, 'environ')
    # os.environ.get is called by libs as well as detect_version(); fortunately no harm seems to
    # come from giving them bad results.

    # no override requested
    env.get.side_effect = lambda key, default=None: default # key not found
    version_a = gips.detect_version()

    # override requested
    env.get.side_effect = lambda key, default=None: 'fancy-new-version'
    version_b = gips.detect_version()

    env.get.assert_has_calls([ # assert two identical calls
        mock.call('GIPS_OVERRIDE_VERSION', gips.version.__version__) for _ in range(2)
    ])
    assert (version_a, version_b) == (gips.version.__version__, 'fancy-new-version')


def t_repository_find_tiles_normal_case(mocker):
    """Test Repository.find_tiles using landsatRepository as a guinea pig."""
    m_list_tiles = mocker.patch('gips.data.core.dbinv.list_tiles')
    expected = [u'tile1', u'tile2', u'tile3'] # list_tiles returns unicode
    m_list_tiles.return_value = expected
    actual = landsatRepository.find_tiles()
    assert expected == actual


def t_repository_find_tiles_error_case(mocker):
    """Confirm Repository.find_tiles quits on error."""
    m_list_tiles = mocker.patch('gips.data.core.dbinv.list_tiles')
    m_list_tiles.side_effect = Exception('AAAAAAAAAAH!') # intentionally break list_tiles

    # confirm call was still a success via the righ code path
    with pytest.raises(SystemExit):
        landsatRepository.find_tiles()


def t_repository_find_dates_normal_case(mocker):
    """Test Repository.find_dates using landsatRepository as a guinea pig."""
    m_list_dates = mocker.patch('gips.data.core.dbinv.list_dates')
    dt = datetime
    expected = [dt(1900, 1, 1), dt(1950, 10, 10), dt(2000, 12, 12)]
    m_list_dates.return_value = expected
    actual = landsatRepository.find_dates('some-tile')
    assert expected == actual


def t_repository_find_dates_error_case(mocker):
    """Confirm Repository.find_dates quits on error."""
    m_list_dates = mocker.patch('gips.data.core.dbinv.list_dates')
    m_list_dates.side_effect = Exception('AAAAAAAAAAH!') # intentionally break list_dates

    # confirm call was still a success via the righ code path
    with pytest.raises(SystemExit):
        landsatRepository.find_dates('some-tile')


@pytest.mark.django_db
def t_Data_AddFile_repeat(mocker):
    """Confirm that adding a file twice results in overwriting the original."""
    m_use_orm = mocker.patch('gips.data.core.orm.use_orm')
    m_use_orm.return_value = True
    t_tile      = 'test-tile'
    t_date      = datetime(1955, 11, 5)
    t_sensor    = 'test-sensor'
    t_product   = 'test-product'
    t_filename  = 'test-filename.tif'
    t_new_filename = 'test-new-filename.tif'
    lsd = landsatData(search=False) # heh
    lsd.id = t_tile
    lsd.date = t_date
    lsd.AddFile(t_sensor, t_product, t_filename) # should work
    lsd.AddFile(t_sensor, t_product, t_new_filename) # should also work, overwriting the old one
    # confirm overwrite happens both in the Data object and in the database
    assert (t_new_filename == lsd.filenames[(t_sensor, t_product)] and
            t_new_filename == dbinv.models.Product.objects.get(tile=t_tile, date=t_date).name)
