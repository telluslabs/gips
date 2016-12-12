
import os
import datetime

import pytest
import envoy

from gips.inventory import dbinv, orm
from gips.test.sys import util

@pytest.fixture
def status_table(db, request):
    for s in 'requested', 'in-progress', 'complete', 'failed':
        dbinv.models.Status(status=s).save()


@pytest.mark.django_db()
def t_fetch(status_table):
    """Simple test for worker.fetch.  Warning:  Operates destructively."""
    from gips.datahandler.worker import fetch
    import gippy

    # config
    gippy.Options.SetVerbose(4) # substantial verbosity for testing purposes

    os.environ['GIPS_ORM'] = 'true'
    key_kwargs = dict(driver='modis', 
                      asset ='MCD43A2', 
                      tile  ='h12v04',
                      date  =datetime.date(2012, 12, 1))
    fetch_args = tuple(key_kwargs[k] for k in ('driver', 'asset', 'tile', 'date'))
    api_kwargs = dict(sensor='dontcare', 
                      name  ='unspecified',
                      status='requested',
                      **key_kwargs)
    expected = os.path.join(
            util.DATA_REPO_ROOT,
            # taken from the modis fetch test; hash isn't used but is:  531008224
            'modis/tiles/h12v04/2012336/MCD43A2.A2012336.h12v04.006.2016112010833.hdf')

    # setup
    orm.setup()
    if os.path.exists(expected): # remove the asset if it's present
        os.remove(expected)
    dbinv.update_or_add_asset(**api_kwargs) # set the asset to 'requested' status

    # test
    returned_asset = fetch(*fetch_args)
    queried_asset = dbinv.models.Asset.objects.get(**key_kwargs)
    assert (expected == returned_asset.name == queried_asset.name
            and 'complete' == returned_asset.status.status == queried_asset.status.status
            and os.path.isfile(expected))
