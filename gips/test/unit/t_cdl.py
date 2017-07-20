import datetime
import os

import pytest

from ...data.cdl import cdl

_2016 = datetime.date(2016, 1, 1)
_afps = {
    'cdl': '/repo/cdl/tiles/IN/2016/IN_2016_cdl_cdl.tif',
    'cdlmkii': '/repo/cdl/tiles/IN/2016/IN_2016_cdlmkii_cdl.zip',
}

def _patched_cdlData_init(self, *args, **kwargs):
    asset = cdl.cdlAsset(os.path.dirname(__file__) + '/../IN_2016_cdlmkii_cdl.zip')
    self.assets = {'cdlmkii': asset}

asset_constructor_base_case_params = [
    (asset_fp, (asset_fp, ap_type, 'IN', _2016, 'cdl', {ap_type: asset_fp}))
    for ap_type, asset_fp in _afps.items()
]

@pytest.mark.parametrize("fn, expected", asset_constructor_base_case_params)
def t_cdlAsset_constructor(fn, expected):
    a = cdl.cdlAsset(fn)
    assert expected == (a.filename, a.asset, a.tile, a.date, a.sensor, a.products)

def t_cdlData_legend(mocker):
    mocker.patch('gips.data.cdl.cdlData.__init__', _patched_cdlData_init)
    d = cdl.cdlData()
    assert d.legend() == ['class1', 'class2']
    assert d.get_code('class1') == 0
    assert d.get_cropname(0) == 'class1'
