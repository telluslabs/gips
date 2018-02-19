import datetime

from gips.data.aod import aod

def t_aodAsset_query_service_success_case(mocker):
    """Confirm aodAsset.query_service successfully reports a found asset."""
    m_ftp_obj = mocker.patch.object(aod.aodAsset, 'ftp_connect').return_value
    m_ftp_obj.nlst.return_value = ['MOD08_D3-oh-hai.hdf', 'MOD99-no-match.pdf']
    actual = aod.aodAsset.query_service('MOD08', 'dontcare',
                                       datetime.date(2015, 01, 01))
    assert {'basename': 'MOD08_D3-oh-hai.hdf'} == actual
