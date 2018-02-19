import datetime
import sys

import pytest

from ...data.landsat import landsat

def actual(la):
    # TODO: la.visbands, la.lwbands, and possibly la.meta
    return (la.filename, la.asset, la.version, la.sensor,
            la.date.year, la.date.timetuple().tm_yday)

dn_fn = '/data-root/landsat/tiles/012030/2015352/LC80120302015352LGN00.tar.gz'
sr_fn = '/data-root/landsat/tiles/026035/2015162/LC80260352015162-SC20160317174932.tar.gz'
c1_lc8_fn = '/data-root/landsat/tiles/013030/2016202/LC08_L1TP_013030_20160720_20170222_01_T1.tar.gz'
c1_le7_fn = '/data-root/landsat/tiles/012030/2010010/LE07_L1TP_013030_20100110_20160916_01_T1.tar.gz'
c1_lt5_fn = '/data-root/landsat/tiles/012030/2010018/LT05_L1GS_013030_20100118_20160903_01_T2.tar.gz'

@pytest.mark.parametrize("fn, expected", [
    (dn_fn, (dn_fn, 'DN', 0, 'LC8',   2015, 352)),
    # uncomment when this merges, it may fix it:
    # https://github.com/Applied-GeoSolutions/gips/pull/337/
    #(sr_fn, (sr_fn, 'SR', 1, 'LC8SR', 2015, 162)),
    (c1_lc8_fn, (c1_lc8_fn, 'C1', 1000052.9, 'LC8', 2016, 202)),
    (c1_le7_fn, (c1_le7_fn, 'C1', 999893.9, 'LE7', 2010, 10)),
    (c1_lt5_fn, (c1_lt5_fn, 'C1', 999880.5, 'LT5', 2010, 18)),
])
def t_landsatAsset_constructor(fn, expected, mocker):
    m_cloud_cover = mocker.patch.object(landsat.landsatAsset, 'cloud_cover')
    la = landsat.landsatAsset(fn)
    assert expected == actual(la)

def t_landsatAsset_query_service_not_available_case(mocker):
    """Confirms the query_service method gives up if dates are invalid."""
    mocker.patch.object(landsat.landsatAsset, 'available').return_value = False
    dc = 'dontcare'
    # if it doesn't exit in time, this fake date will raise an exception when
    # query_service tries to call strftime on it -------vv
    assert None == landsat.landsatAsset.query_service(dc, dc, dc)

def t_landsatAsset_query_service_success_case(mocker):
    """Confirms method works for the normal case."""

    ### big pile o' mocks
    mocker.patch.object(landsat.landsatAsset, 'load_ee_search_keys')
    mocker.patch.object(landsat.landsatAsset, 'ee_login')

    # have to mock around a local import
    m_usgs, m_api = mocker.MagicMock(), mocker.MagicMock()
    sys.modules['usgs'] = m_usgs
    m_usgs.api = m_api

    m_dataset = mocker.MagicMock()
    mocker.patch.object(landsat.landsatAsset, '_ee_datasets'
                        ).keys.return_value = [m_dataset]
    result = {'metadataUrl': 'dontcare', 'displayId': 'basename',
              'entityId': 'scene-id'}
    # response object
    m_api.search.return_value = {'data': {'results': [result]}}
    mocker.patch.object(landsat.requests, 'get')
    # why do people use XML?  Trick question:  XML uses you, and not gently.
    m_xml = mocker.patch.object(landsat.ElementTree, 'fromstring').return_value
    m_xml.find.return_value.__getitem__.return_value.text = '0.6'

    ### now do the call & assertion
    expected = {'basename': 'basename.tar.gz',
                'sceneID': 'scene-id',
                'dataset': m_dataset,
                'sceneCloudCover': 0.6,
                'landCloudCover': 0.6}

    actual = landsat.landsatAsset.query_service('C1', '012030',
                                                datetime.date(2016, 1, 1))

    assert expected == actual
