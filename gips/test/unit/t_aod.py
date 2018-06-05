import datetime

from gips.data.aod import aod

# taken from https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD08_D3/2017/145.json
test_basename = 'MOD08_D3.A2017145.006.2017151134051.hdf'
test_url = ('https://ladsweb.modaps.eosdis.nasa.gov/'
            'archive/allData/61/MOD08_D3/2015/001/'
            'MOD08_D3.A2017145.006.2017151134051.hdf')

def t_aodAsset_query_provider_success_case(mocker, mpo):
    """Confirm aodAsset.query_service successfully reports a found asset."""
    mpo(aod, 'requests').get.return_value.json.return_value = [{
        u'name': u'MOD08_D3.A2017145.006.2017151134051.hdf'}]
    actual_bn, actual_url = aod.aodAsset.query_provider(
        'MOD08', 'dontcare', datetime.date(2015, 1, 1))
    assert (test_basename, test_url) == (actual_bn, actual_url)

def t_aodAsset_fetch_success_case(mocker, mpo, mock_context_manager):
    """Mock I/O & confirm correct behavior by inspecting calls & output."""
    # technically make_temp_dir should be mocked, but it's harmless
    mpo(aod.aodAsset, 'query_service').return_value = {
        'basename': test_basename, 'url': test_url}
    # should usually work regardless of gips config:
    mpo(aod.aodRepository, 'get_setting').return_value = 'fake-stage'
    m_get = mpo(aod, 'requests').get
    mpo(aod.os, 'rename')
    mpo(aod, 'open')
    mock_context_manager(aod.utils, 'make_temp_dir', 'fake-temp-dir')

    actual = aod.aodAsset.fetch('MOD08', 'h01v01', datetime.date(2015, 1, 1))

    assert (mocker.call(test_url, stream=True) == m_get.call_args
            and ['fake-stage/stage/' + test_basename] == actual)
