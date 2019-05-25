import datetime
import os

import pytest

from ...data.cdl import cdl

_2016 = datetime.date(2016, 1, 1)
_afps = {
    'cdl': '/repo/cdl/tiles/IN/2016/IN_2016_cdl_cdl.tif',
    'cdlmkii': '/repo/cdl/tiles/IN/2016/IN_2016_cdl_cdlmkii.zip',
}

def _patched_cdlData_init(self, *args, **kwargs):
    asset = cdl.cdlAsset(os.path.dirname(__file__) + '/../IN_2016_cdl_cdlmkii.zip')
    self.assets = {'cdlmkii': asset}

def _patched_metadata(self):
    return {
        'CLASS_NAME_class1': 0,
        'CLASS_NAME_class2': 1,
    }

def _patched_gdal_open(self, *args, **kwargs):
    return type('osgeo.gdal.Dataset', (object,), {'GetMetadata': _patched_metadata})()

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
    mocker.patch('osgeo.gdal.Open', _patched_gdal_open)
    d = cdl.cdlData()

    expected_legend = [''] * 256
    expected_legend[0] = 'class1'
    expected_legend[1] = 'class2'
    assert d.legend() == expected_legend and \
        d.get_code('class1') == 0 and \
        d.get_cropname(0) == 'class1'

def t_cdlAsset_query_service_success_case(mocker):
    """Confirm aodAsset.query_service successfully reports a found asset."""
    fake_tile = 'fake-tile'
    mocker.patch.object(cdl.utils, 'open_vector').return_value = {
        'fake-tile': {'STATE_FIPS': 'hi mom!'}}
    mocker.patch.object(cdl.requests, 'get').return_value.status_code = 200
    expected_url = 'http://www.fluffy-bunnies-and-rainbows.mil/'
    m_root = mocker.patch.object(cdl.ElementTree, 'fromstring').return_value
    m_root.find.return_value.text = expected_url

    actual = cdl.cdlAsset.query_service('cdl', fake_tile,
                                        datetime.date(2015, 1, 1))
    assert {'basename': 'fake-tile_2015_cdl_cdl.tif',
            'url': expected_url} == actual

def t_cdlAsset_fetch_success_case(mocker, mpo, mock_context_manager):
    """Confirm good behavior through inspecting calls to mocked I/O APIs."""
    test_url = 'http://himom.com/'
    mpo(cdl.cdlAsset, 'query_service').return_value = {'url': test_url}
    m_requests_get = mpo(cdl, 'requests').get
    m_file_response = m_requests_get()
    mock_context_manager(cdl.utils, 'make_temp_dir', 'fake-temp-dir')
    m_open = mpo(cdl, 'open')
    m_GeoImage = mpo(cdl, 'GeoImage')
    m_shutil_copy = mpo(cdl.shutil, 'copy')
    mpo(cdl.cdlRepository, 'get_setting').return_value = 'fake-stage'

    cdl.cdlAsset.fetch('cdl', 'NH', datetime.date(2016, 1, 1))

    expected_open_call = mocker.call('fake-temp-dir/NH_2016_cdl_cdl.tif', 'w')
    expected_copy_call = mocker.call('fake-temp-dir/NH_2016_cdl_cdl.tif',
                                     'fake-stage/stage')
    assert (test_url == m_requests_get.call_args[0][0]
            and expected_open_call == m_open.call_args
            and expected_copy_call == m_shutil_copy.call_args)
