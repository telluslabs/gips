"""Unit tests for inventory/*, mainly the Inventory classes."""

import os
import datetime

import pytest
import mock
from django.forms.models import model_to_dict

from gips.inventory import DataInventory
from gips.data.modis.modis import modisData, modisAsset
from gips.core import SpatialExtent, TemporalExtent


# TODO blatant cutpastes from t_dbinv_api.py; refactor into common code?
path_prefix = modisAsset.Repository.data_path()

asset_filenames = [
    os.path.join(path_prefix, 'h12v04/2012338/MYD11A1.A2012338.h12v04.005.2012341075802.hdf'),
    os.path.join(path_prefix, 'h12v04/2012337/MOD10A1.A2012337.h12v04.005.2012340033542.hdf'),
    os.path.join(path_prefix, 'h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf'),
]

expected = {
    'MYD11A1': {
        'name':   path_prefix + '/h12v04/2012338/MYD11A1.A2012338.h12v04.005.2012341075802.hdf',
        'asset':  u'MYD11A1',
        'date':   datetime.date(2012, 12, 3),
        'driver': u'modis',
        'sensor': u'MYD',
        'tile':   u'h12v04'
    },
    'MOD10A1': {
        'name':   path_prefix + '/h12v04/2012337/MOD10A1.A2012337.h12v04.005.2012340033542.hdf',
        'asset':  u'MOD10A1',
        'date':   datetime.date(2012, 12, 2),
        'driver': u'modis',
        'sensor': u'MOD',
        'tile':   u'h12v04'
    },
    'MCD43A2': {
        'name':   path_prefix + '/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf',
        'asset':  u'MCD43A2',
        'date':   datetime.date(2012, 12, 1),
        'driver': u'modis',
        'sensor': u'MCD',
        'tile':   u'h12v04'
    },
}


@pytest.fixture
def di_init_mocks(mocker):
    """Appropriate mocks for DataInventory.__init__."""
    modisData.fetch = mocker.Mock() # behavior not super important
    modisData.Asset.archive = mocker.Mock() # has to return list of modisAssets
    return (modisData.fetch,
            modisData.Asset.archive,
            mock.patch('gips.inventory.dbinv.add_asset'))


@pytest.mark.django_db
def t_data_inventory_db_save(di_init_mocks):
    """Confirm DataInventory() saves to the inventory DB on fetch."""
    from gips.inventory.dbinv import models
    (m_fetch, m_archive, m_add_asset) = di_init_mocks
    # need some filenames . . .
    assets = [modisAsset(fn) for fn in asset_filenames]
    # normally _archivefile would set this attrib:
    [setattr(asset, 'archived_filename', asset.filename) for asset in assets]
    m_archive.return_value = assets

    # specify spatial & temporal?
    tiles = ['h12v04', 'h13v05', 'h12v05', 'h13v04']
    se = SpatialExtent(modisData, tiles=tiles)
    te = TemporalExtent('2012-12-01,2012-12-03')
    # can ignore rest of **kwargs in constructor due to mocking
    di = DataInventory(modisData, se, te, fetch=True)

    # confirm DB has correct entries in it now
    rows = [model_to_dict(ao) for ao in models.Asset.objects.all()]
    [a.pop('id') for a in rows] # don't care what the keys are
    actual = {r['asset']: r for r in rows} # enforce an order so whims of hashing doesn't ruin test

    assert expected == actual
