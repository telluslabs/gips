import datetime

import pytest

from ...data.daymet import daymet

# approach here is cribbed from unit/t_landsat.py

_2015002 = datetime.date(2015, 1, 2)
_afps = { # asset full paths
    'tmin': '/repo/daymet/tiles/11935/2015002/11935_2015002_daymet_tmin.tif',
    'tmax': '/repo/daymet/tiles/11935/2015002/11935_2015002_daymet_tmax.tif',
    'prcp': '/repo/daymet/tiles/11935/2015002/11935_2015002_daymet_prcp.tif',
    'srad': '/repo/daymet/tiles/11935/2015002/11935_2015002_daymet_srad.tif',
    'vp':   '/repo/daymet/tiles/11935/2015002/11935_2015002_daymet_vp.tif',
}

# inputs and outputs for the base case - one for each asset/product type
asset_constructor_base_case_params = [
    (asset_fp, (asset_fp, ap_type, '11935', _2015002, 'daymet', {ap_type: asset_fp}))
    for ap_type, asset_fp in _afps.items()
]

@pytest.mark.parametrize("fn, expected", asset_constructor_base_case_params)
def t_daymetAsset_constructor_base_case(fn, expected):
    """Confirm well-behaved files go in correctly."""
    a = daymet.daymetAsset(fn)
    assert expected == (a.filename, a.asset, a.tile, a.date, a.sensor, a.products)

def t_daymetAsset_fetch_query_service_call(mocker, mpo):
    """Test just enough of daymet's fetch to prove that:

    query_service's output is used correctly."""
    a_type, tile, date = 'fake-asset', 'fake-tile', 'fake-date'
    url = 'http://himom.com/'
    m_query_service = mpo(daymet.daymetAsset, 'query_service')
    m_query_service.return_value = {'basename': 'fake-basename', 'url': url}
    m_open_url = mpo(daymet, 'open_url')
    # intentionally short-circuit daymet's fetch, to avoid mocking the world
    m_open_url.side_effect = RuntimeError('aaaaaah!')

    try:
        daymet.daymetAsset.fetch(a_type, tile, date)
    except RuntimeError:
        pass

    assert (mocker.call(a_type, tile, date) == m_query_service.call_args
            and mocker.call(url) == m_open_url.call_args)
