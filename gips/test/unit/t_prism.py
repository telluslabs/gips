import datetime

import pytest

from gips.data.prism import prism

a_type = '_tmin'
tile = 'CONUS'
date = datetime.date(1982, 12, 2)
asset_fn = 'PRISM_tmin_stable_4kmD1_19821202_bil.zip'

@pytest.fixture
def m_ftp_connect(mpo):
    return mpo(prism.prismAsset, 'ftp_connect')

def t_prismAsset_query_provider_success_case(mpo):
    m_ftp_connect = mpo(prism.prismAsset, 'ftp_connect')
    date_str = date.strftime('%Y%m%d')
    m_ftp_connect().nlst.return_value = ['foo.txt', 'bar.txt', asset_fn]

    actual_asset_fn, _ = prism.prismAsset.query_provider(a_type, tile, date)

    assert asset_fn == actual_asset_fn

def t_prismAsset_fetch_success_case(mocker, mock_context_manager, mpo):
    m_query_service = mpo(prism.prismAsset, 'query_service')
    m_query_service.return_value = {'basename': asset_fn, 'url': None}
    m_ftp_connect = mpo(prism.prismAsset, 'ftp_connect')
    mpo(prism.prismRepository, 'path').return_value = 'fake-stage-dir'
    mock_context_manager(prism.utils, 'make_temp_dir', 'fake-temp-dir')
    m_open = mpo(prism, 'open')
    m_rename = mpo(prism.os, 'rename')

    actual = prism.prismAsset.fetch(a_type, tile, date)

    expected_rename = mocker.call(
        'fake-temp-dir/PRISM_tmin_stable_4kmD1_19821202_bil.zip',
        'fake-stage-dir/PRISM_tmin_stable_4kmD1_19821202_bil.zip')
    assert (['fake-stage-dir/' + asset_fn] == actual
            and expected_rename == m_rename.call_args)
