from __future__ import print_function

from .util import *

pytestmark = sys  # skip everything unless --sys

# TODO add to CI test suite?
def t_login():
    """Test landsat.landsatAsset.load_ee_search_keys()"""
    from gips.data import landsat
    assert landsat.landsatAsset._ee_datasets is None
    assert not hasattr(landsat.landsatAsset, '_ee_key')
    landsat.landsatAsset.load_ee_search_keys()
    actual = landsat.landsatAsset._ee_datasets.keys()
    print('logged in and found are: {}'.format(
            landsat.landsatAsset._ee_datasets))
    assert landsat.landsatAsset._ee_datasets is not None
    assert hasattr(landsat.landsatAsset, '_ee_key')

# TODO add to CI test suite?
def t_query_service():
    from gips.data import landsat
    from datetime import datetime as dt
    resp = landsat.landsatAsset.query_service('C1', '012030', dt(2017, 8, 1))
    # print(str(resp))
    assert len(resp) == 1
