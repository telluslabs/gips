import datetime

from gips.data.aod import aod

# TODO revise
def t_aodAsset_query_service_success_case(mocker):
    """Confirm aodAsset.query_service successfully reports a found asset."""
    m_ftp_obj = mocker.patch.object(aod.aodAsset, 'ftp_connect').return_value
    m_ftp_obj.nlst.return_value = ['MOD08_D3-oh-hai.hdf', 'MOD99-no-match.pdf']
    actual = aod.aodAsset.query_service('MOD08', 'dontcare',
                                       datetime.date(2015, 1, 1))
    assert {'basename': 'MOD08_D3-oh-hai.hdf'} == actual

# TODO revise
def t_aodAsset_fetch_success_case(mocker, mpo):
    """Mock I/O & confirm correct behavior by inspecting calls & output."""
    test_bn = 'test-base-name'
    mpo(aod.aodAsset, 'query_service').return_value = {'basename': test_bn}
    mpo(aod.aodRepository, 'get_setting').return_value = 'fake-stage'
    m_ftp_connect = mpo(aod.aodAsset, 'ftp_connect')
    m_open = mpo(aod, 'open')

    actual = aod.aodAsset.fetch('MOD08', 'h01v01', datetime.date(2015, 1, 1))

    assert (mocker.call('MOD08', datetime.date(2015, 1, 1))
                == m_ftp_connect.call_args
            and ['fake-stage/stage/test-base-name'] == actual)
