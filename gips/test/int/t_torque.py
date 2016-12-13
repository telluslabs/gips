import os
import datetime
import time

import pytest
import envoy

from django.core.management import call_command

import gippy
from gips.inventory import dbinv, orm
from gips.test.sys import util
from gips.datahandler.torque import submit


@pytest.fixture
def disable_db_blocker(django_db_blocker):
    with django_db_blocker.unblock():
        orm.setup()
        call_command('migrate', interactive=False)
        for s in 'requested', 'in-progress', 'complete', 'failed':
            dbinv.models.Status.objects.update_or_create(status=s)
        yield


def t_submit_single(disable_db_blocker):
    """Simple test for torque.submit('fetch'...).  Warning:  Destructive."""

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
    if os.path.exists(expected): # remove the asset if it's present
        os.remove(expected)
    dbinv.update_or_add_asset(**api_kwargs) # set the asset to 'requested' status

    # test
    submission_outcome = submit('fetch', [fetch_args])
    #(job_exit_status, job_stdout, job_stderr) = job_outcomes[0]
    print "qsub called; exit status, stdout, stderr: {}, {}, {}".format(*submission_outcome[0])
    # wait on outcome - once per second check status
    queried_asset = dbinv.models.Asset.objects.get(**key_kwargs)
    for i in range(1, 46):
        queried_asset.refresh_from_db()
        if queried_asset.status.status in ('complete', 'failed'):
            break
        time.sleep(1)
        if i % 5 == 0:
            print "Wait time: {}s".format(i)

    assert (True # TODO check outcome of job in torque via pbs_python call
            and (expected, 'complete') == (queried_asset.name, queried_asset.status.status)
            and os.path.isfile(expected))
