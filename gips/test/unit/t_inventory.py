"""Unit tests for inventory/*, mainly the Inventory classes."""

import os
import datetime

import pytest
import mock
from django.forms.models import model_to_dict

from gips.inventory import DataInventory, dbinv
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

    # specify spatial & temporal
    tiles = ['h12v04', 'h13v05', 'h12v05', 'h13v04']
    se = SpatialExtent(modisData, tiles, 0.0, 0.0)
    te = TemporalExtent('2012-12-01,2012-12-03')
    # can ignore rest of **kwargs in constructor due to mocking
    di = DataInventory(modisData, se, te, fetch=True)

    # confirm DB has correct entries in it now
    rows = [model_to_dict(ao) for ao in models.Asset.objects.all()]
    [a.pop('id') for a in rows] # don't care what the keys are
    actual = {r['asset']: r for r in rows} # enforce an order so whims of hashing doesn't ruin test

    assert expected == actual


@pytest.mark.django_db
def t_data_inventory_load_assets():
    """Confirm DataInventory() loads assets from the inventory DB correctly.

    In particular check the resulting hierarchy of objects for correctness."""

    # mock: dates = self.temporal.prune_dates(spatial.available_dates) . . . ?

    # first load DB with data
    for asset_fields in expected.values():
        dbinv.add_asset(**asset_fields)

    # instantiate the class under test
    tiles = ['h12v04', 'h12v05', 'h13v04', 'h13v05']
    se = SpatialExtent(modisData, tiles, 0.0, 0.0)
    te = TemporalExtent('2012-12-01,2012-12-03')
    di = DataInventory(modisData, se, te)

    # confirm DataInventory object is correct
    assert len(di.data) == 3
    for tiles_obj in di.data.values():
        assert len(tiles_obj.tiles) == 1
        data_obj = tiles_obj.tiles['h12v04']
        assert len(data_obj.assets) == 1
        asset_obj = data_obj.assets.values()[0]
        # FINALLY compare the objects themselves
        ea = expected[asset_obj.asset]
        for field in ('asset', 'date', 'sensor', 'tile'):
            assert ea[field] == getattr(asset_obj, field)
        assert ea['name'] == asset_obj.filename
