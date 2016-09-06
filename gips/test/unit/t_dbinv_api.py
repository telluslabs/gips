import os, fnmatch, datetime

import pytest
import django.db
from django.forms.models import model_to_dict

from gips.inventory.dbinv import models
from gips.inventory.dbinv import rectify, list_tiles, add_asset
from gips.data.modis import modisAsset


### rectify() test setup
stale_file_names = [ # these should be removed during rectify()
    'h12v04/2012338/MCD43A4.A2012338.h12v04.006.2016112020013.hdf',
    'h12v04/2012337/MCD43A4.A2012337.h12v04.006.2016112013509.hdf',
    'h12v04/2012336/MOD10A1.A2012336.h12v04.005.2012339213007.hdf',
]

rubbish_filenames = [
    # landsat is wrong obviously; shouldn't show up in results
    '012030/2015352/012030_2015352_LC8_rad-toa.tif',
    '012030/2015352/012030_2015352_LC8_bqashadow.tif',
    '012030/2015352/012030_2015352_LC8_acca.tif',
    '012030/2015352/LC80120302015352LGN00_MTL.txt',
    # erroneous assets
    'h12v04/2012338/A2003266.h12v09.005.hdf',  # missing generation stamp per issue #79
    'h12v04/2012338/bork.hdf',                 # not enough period-delimited substrings
    'h12v04/2012338/_2004001._02_06.051.2014287173613.hdf', # try to trip it up with wrong characters
]

proper_filenames = [
    'h12v04/2012338/MYD11A1.A2012338.h12v04.005.2012341075802.hdf',
    'h12v04/2012337/MOD10A1.A2012337.h12v04.005.2012340033542.hdf',
    'h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf',
]

path_prefix = modisAsset.Repository.data_path()
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


@pytest.mark.django_db
def t_rectify(mocker):
    from gips.inventory.dbinv import models
    # construct plausible file listing & mock it into glob outcome
    path = modisAsset.Repository.data_path()
    rubbish_full_fns = [os.path.join(path, fn) for fn in rubbish_filenames]
    proper_full_fns  = [os.path.join(path, fn) for fn in proper_filenames]
    full_fns = rubbish_full_fns + proper_full_fns
    mock_iglob = mocker.patch('gips.inventory.dbinv.glob.iglob')
    mock_iglob.side_effect = lambda pat: [fn for fn in full_fns if fnmatch.fnmatchcase(fn, pat)]

    # preload stale data to confirm stale things get deleted
    for fn in stale_file_names:
        full_fn = os.path.join(path, fn)
        ma = modisAsset(full_fn)
        asset = models.Asset(
            asset =ma.asset,
            sensor=ma.sensor,
            tile  =ma.tile,
            date  =ma.date,
            name  =full_fn,
            driver='modis',
        )
        asset.save()

    # run the function under test
    rectify(modisAsset)

    # load data for inspection
    rows = [model_to_dict(ao) for ao in models.Asset.objects.all()]
    [a.pop('id') for a in rows] # don't care what the keys are
    actual = {r['asset']: r for r in rows} # enforce an order so whims of hashing doesn't ruin test

    assert expected == actual


# This data isn't entirely valid but is correct enough for the test.  Also unicode isn't super
# relevant here; it's an artifact of cutpasting
list_tiles_fixture = [
    { # basic row in table
        'name':   path_prefix + '/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf',
        'asset':  u'MCD43A2',
        'date':   datetime.date(2012, 12, 1),
        'driver': u'modis',
        'sensor': u'MCD',
        'tile':   u'h12v04'
    },
    { # duplicate tile string to confirm nonrepetition in outcome
        'name':   path_prefix + '/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf',
        'asset':  u'MCD43A2',
        'date':   datetime.date(2012, 12, 2),
        'driver': u'modis',
        'sensor': u'MCD',
        'tile':   u'h12v04'
    },
    { # second tile to confirm multiple tiles will be returned
        'name':   path_prefix + '/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf',
        'asset':  u'MCD43A2',
        'date':   datetime.date(2012, 12, 2),
        'driver': u'modis',
        'sensor': u'MCD',
        'tile':   u'h13v05'
    },
    { # different driver to confirm no cross-driver pollution of results
        'name':   path_prefix + '/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf',
        'asset':  u'MCD43A2',
        'date':   datetime.date(2012, 12, 1),
        'driver': u'landsat',
        'sensor': u'MCD',
        'tile':   u'trolololo'
    },
]

@pytest.mark.django_db
def t_list_tiles():
    """Test gips.inventory.dbinv for correctness using a database fixture."""
    [models.Asset(**f).save() for f in list_tiles_fixture]
    actual = list_tiles('modis')
    expected = [u'h13v05', u'h12v04']
    assert len(actual) == 2 and set(expected) == set(actual)


@pytest.mark.django_db
def t_add_asset():
    """Confirm that dbinv.add_asset works for saving assets."""
    values = {
        'asset':  u'some-asset',
        'sensor': u'some-sensor',
        'tile':   u'some-tile',
        'date':   datetime.date(2099, 12, 31),
        'name':   u'/some/file/name.hdf',
        'driver': u'some-driver',
    }
    expected = dict(values)
    expected['id'] = 1
    a = add_asset(**values)
    returned_actual = model_to_dict(a)
    queried_actual = model_to_dict(models.Asset.objects.get(pk=1))
    assert expected == returned_actual == queried_actual
