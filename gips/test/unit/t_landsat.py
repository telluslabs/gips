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

@pytest.mark.parametrize(
        'avail_rv, a_type, get_setting_rv, query_service_rv',
        [(False, 'dontcare', 'dontcare', None),
         (True,  'DN',       'dontcare', None),
         (True,  'C1',       'invalid-data-source', ValueError)])
def t_landsatAsset_query_service_early_exits(
            mocker, avail_rv, a_type, get_setting_rv, query_service_rv):
    """Confirms the query_service method gives up early when it should."""
    mocker.patch.object(landsat.landsatAsset, 'available',
                        return_value=avail_rv)
    mocker.patch.object(landsat.landsatAsset.Repository, 'get_setting',
                        return_value=get_setting_rv)
    dc = 'dontcare'
    if query_service_rv is ValueError:
        with pytest.raises(ValueError):
            landsat.landsatAsset.query_service(a_type, dc, dc)
    else:
        assert None == landsat.landsatAsset.query_service(a_type, dc, dc)

@pytest.fixture
def m_load_ee_search_keys(mocker):
    return mocker.patch.object(landsat.landsatAsset, 'load_ee_search_keys')

@pytest.fixture
def m_get_setting(mocker):
    return mocker.patch.object(landsat.landsatAsset.Repository, 'get_setting')

@pytest.fixture
def m_ee_login(mocker):
    return mocker.patch.object(landsat.landsatAsset, 'ee_login')

@pytest.yield_fixture
def m_usgs_lib(mocker):
    """landsat does 'import usgs' in local scope; work around that"""
    # TODO try mocker.patch.dict
    saved_usgs = sys.modules.get('usgs', None)
    m_usgs = sys.modules['usgs'] = mocker.MagicMock()
    yield m_usgs
    if saved_usgs is not None:
        sys.modules['usgs'] = saved_usgs

def t_landsatAsset_query_service_c1_success_case(
        mocker, m_ee_login, m_get_setting, m_load_ee_search_keys, m_usgs_lib):
    """Confirms method works for the normal case."""
    ### big pile o' mocks
    m_get_setting.return_value = 'usgs'
    m_dataset = mocker.MagicMock()
    mocker.patch.object(landsat.landsatAsset, '_ee_datasets'
                        ).keys.return_value = [m_dataset]
    result = {'metadataUrl': 'dontcare', 'displayId': 'basename',
              'entityId': 'scene-id'}
    # response object
    m_usgs_lib.api.search.return_value = {'data': {'results': [result]}}
    mocker.patch.object(landsat.requests, 'get')
    # why do people use XML?  Trick question:  XML uses you, and not gently.
    m_xml = mocker.patch.object(landsat.ElementTree, 'fromstring').return_value
    m_xml.find.return_value.__getitem__.return_value.text = '0.6'

    ### now do the call & assertion
    expected = {'basename': 'basename.tar.gz',
                'scene_id': 'scene-id',
                'dataset': m_dataset,
                'a_type': 'C1',
                #'sceneCloudCover': 0.6, # presently unused
                #'landCloudCover': 0.6,
                }

    actual = landsat.landsatAsset.query_service('C1', '012030',
                                                datetime.date(2016, 1, 1))

    assert expected == actual

sample_c1s3_keys = {
    'a_type': 'C1S3', # not a part of the asset but it's returned by query_s3
    '_15m_tif':
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B8.TIF',
    '_30m_tifs': [
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B1.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B2.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B3.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B4.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B5.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B6.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B7.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B9.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B10.TIF',
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_B11.TIF',
    ],
    'qa_tif':
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_BQA.TIF',
    'mtl_txt':
        'c1/L8/027/033/LC08_L1TP_027033_20170506_20170515_01_T1/LC08_L1TP_027033_20170506_20170515_01_T1_MTL.txt',
}

@pytest.fixture
def m_query_s3(mocker):
    mocker.patch.object(landsat.landsatAsset.Repository, 'get_setting',
                        return_value='s3')
    mocker.patch.dict(landsat.os.environ, {
        'AWS_SECRET_ACCESS_KEY': 'fake-secret-key',
        'AWS_ACCESS_KEY_ID': 'fake-key-id'})
    # have to mock around a local import
    m_boto3 = sys.modules['boto3'] = mocker.MagicMock()
    m_s3 = m_boto3.resource.return_value
    flattened_keys = sample_c1s3_keys['_30m_tifs'] + [
        sample_c1s3_keys[k] for k in ('qa_tif', '_15m_tif', 'mtl_txt')]
    filter_output = []
    for key in flattened_keys:
        mm = mocker.MagicMock()
        mm.key = key
        filter_output.append(mm)
    m_s3.Bucket.return_value.objects.filter.return_value = filter_output

    return mocker.patch.object(landsat.requests, 'get')

def cloud_cover_snippet(percentage):
    """Returns a string that should match landsat's cloud cover detection.

    Taken from LC08_L1TP_027033_20170506_20170515_01_T1_MTL.txt.
    """
    return """
        RLUT_FILE_NAME = "LC08RLUT_20150303_20431231_01_12.h5"
      END_GROUP = PRODUCT_METADATA
      GROUP = IMAGE_ATTRIBUTES
        CLOUD_COVER = {}
        CLOUD_COVER_LAND = 0.03
        IMAGE_QUALITY_OLI = 9
    """.format(float(percentage))

s3_qs_expected = sample_c1s3_keys.copy()
s3_qs_expected['basename'] = \
    'LC08_L1TP_027033_20170506_20170515_01_T1_S3.json'

@pytest.mark.parametrize("pclouds, expected", [
    (100.0, s3_qs_expected), # note cloud cover is fixed at 50%
    (50.0, s3_qs_expected),
    (49.99, None),
    (25.0, None),
])
def t_landsatAsset_query_service_s3(
        pclouds, expected, mocker, m_query_s3):
    """Confirms method works for the normal case."""
    m_get = m_query_s3
    m_get().text = cloud_cover_snippet(50.0)

    actual = landsat.landsatAsset.query_service(
            'C1S3', '027033', datetime.date(2017, 5, 6), pclouds)
    assert expected == actual


def t_landsatData_products2assets(m_query_s3):
    """Unfetchable and undesired sources should be filtered out."""
    assert {'C1S3'} == landsat.landsatData.products2assets(['rad', 'landmask'])
