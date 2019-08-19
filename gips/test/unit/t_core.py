"""Unit tests for core functions found in gips.core and gips.data.core."""

import sys
import os
import pkgutil
import imp
import datetime
from datetime import datetime as dt

import pytest

import gips
from gips import core
from gips.data import core as data_core
from gips.inventory import dbinv

# the tests use certain drivers to help out with testing core functions
from gips.data.landsat.landsat import landsatRepository, landsatData
from gips.data.sar import sar
from gips.data.landsat import landsat
# re-use mocks from modis fetch tests
from . import t_modis_fetch
from .t_modis_fetch import fetch_mocks # have to do direct import; pytest magic
from gips.data.modis import modis

def t_repository_find_tiles_normal_case(mocker, orm):
    """Test Repository.find_tiles using landsatRepository as a guinea pig."""
    m_list_tiles = mocker.patch('gips.data.core.dbinv.list_tiles')
    expected = [u'tile1', u'tile2', u'tile3'] # list_tiles returns unicode
    m_list_tiles.return_value = expected
    actual = landsatRepository.find_tiles()
    assert expected == actual


def t_repository_find_tiles_error_case(mocker, orm):
    """Confirm Repository.find_tiles quits on error."""
    m_list_tiles = mocker.patch('gips.data.core.dbinv.list_tiles')
    m_list_tiles.side_effect = RuntimeError('AAAAAAAAAAH!') # intentionally break list_tiles

    with pytest.raises(RuntimeError):
        landsatRepository.find_tiles()


def t_repository_find_dates_normal_case(mocker, orm):
    """Test Repository.find_dates using landsatRepository as a guinea pig."""
    m_list_dates = mocker.patch('gips.data.core.dbinv.list_dates')
    expected = [datetime.datetime(*a) for a in
                ((1900, 1, 1), (1950, 10, 10), (2000, 12, 12))]
    m_list_dates.return_value = expected
    actual = landsatRepository.find_dates('some-tile')
    assert expected == actual


@pytest.mark.skip(reason="Letting exception bubble up for now; if that changes un-skip this test.")
def t_repository_find_dates_error_case(mocker):
    """Confirm Repository.find_dates quits on error."""
    m_list_dates = mocker.patch('gips.data.core.dbinv.list_dates')
    m_list_dates.side_effect = Exception('AAAAAAAAAAH!') # intentionally break list_dates

    # confirm call was still a success via the righ code path
    with pytest.raises(SystemExit):
        landsatRepository.find_dates('some-tile')


@pytest.mark.parametrize('add_to_db', (False, True))
def t_data_add_file(orm, mocker, add_to_db):
    """Basic test for Data.AddFile; calls it once then tests its state."""
    m_uoap = mocker.patch('gips.data.core.dbinv.update_or_add_product')
    t_sensor    = 'test-sensor'
    t_product   = 'test-product'
    t_filename  = 'test-filename.tif'
    lsd = landsatData(
            'test-tile', datetime.datetime(1955, 11, 5), search=False)

    lsd.AddFile(t_sensor, t_product, t_filename, add_to_db)

    # alas, cleanest to make multiple assertions for this test
    if add_to_db:
        m_uoap.assert_called_once_with(driver='landsat', product=t_product, sensor=t_sensor,
                                       tile=lsd.id, date=lsd.date, name=t_filename)
    else:
        m_uoap.assert_not_called()
    assert (lsd.filenames == {(t_sensor, t_product): t_filename}
            and lsd.sensors == {t_product: t_sensor})


def t_data_add_file_repeat(orm, mocker):
    """Confirm that calling Data.AddFile twice results in overwrite.

    Thus, confirm it's possible to replace file entries with new versions.
    """
    t_tile      = 'test-tile'
    t_date      = datetime.datetime(1955, 11, 5)
    t_sensor    = 'test-sensor'
    t_product   = 'test-product'
    t_filename  = 'test-filename.tif'
    t_new_filename = 'test-new-filename.tif'
    lsd = landsatData(search=False) # heh
    lsd.id = t_tile
    lsd.date = t_date
    lsd.AddFile(t_sensor, t_product, t_filename)
    lsd.AddFile(t_sensor, t_product, t_new_filename) # should overwrite the old one
    # confirm overwrite happens both in the Data object and in the database
    assert (t_new_filename == lsd.filenames[(t_sensor, t_product)] and
            t_new_filename == dbinv.models.Product.objects.get(tile=t_tile, date=t_date).name)


@pytest.mark.parametrize('search', (False, True))
def t_data_init_search(mocker, orm, search):
    """Confirm Data.__init__ searches the FS only when told to.

    Do this by instantiating landsatData."""
    # set up mocks:  prevent it from doing I/O and use for assertions below
    mocker.patch.object(landsatData.Asset, 'discover')
    mocker.patch.object(landsatData, 'ParseAndAddFiles')

    lsd = landsatData(tile='t', date=datetime.datetime(9999, 1, 1),
                      search=search)

    # assert normal activity & entry of search block
    assert (lsd.id == 't'
            and lsd.date == datetime.datetime(9999, 1, 1)
            and '' not in (lsd.path, lsd.basename)
            and lsd.assets == lsd.filenames == lsd.sensors == {}
            and lsd.ParseAndAddFiles.called == lsd.Asset.discover.called == search)

@pytest.fixture
def m_discover_asset(mocker):
    return mocker.patch.object(landsatData.Asset, 'discover_asset',
                               return_value=None)

@pytest.fixture
def m_query_service(mocker):
    asset_bn = 'LC08_L1TP_012030_20170801_20170811_01_T1.tar.gz'
    query_rv = {'basename': asset_bn, 'url': 'himom.com'}
    return mocker.patch.object(landsatData.Asset, 'query_service',
                               return_value=query_rv)

@pytest.fixture
def m_fetch(mocker):
    return mocker.patch.object(landsatData.Asset, 'fetch')

# useful constant for the following tests
df_args = (['rad', 'ndvi', 'bqashadow'], ['012030'],
           core.TemporalExtent('2017-08-01'))

def t_data_fetch_error_case(mocker, m_discover_asset, m_query_service, m_fetch):
    """Test error case of data.core.Data.fetch.

    It should return [], and shouldn't raise an exception."""
    m_fetch.side_effect = RuntimeError('aaah!')
    assert landsatData.fetch(*df_args) == []


def t_Asset_dates():
    """Test Asset's start and end dates, using SAR."""
    dates_in = datetime.date(2006, 1, 20), datetime.date(2006, 1, 27)
    # tile isn't used --------------vvv     dayrange --vvvvvv
    actual = sar.sarAsset.dates('alos1', 'dontcare', dates_in, (1, 366))
    expected = [datetime.datetime(*a) for a in
                ((2006, 1, 24), (2006, 1, 25), (2006, 1, 26), (2006, 1, 27))]
    assert expected == actual

@pytest.fixture
def asset_and_replacement():
    """For tests of the update=True case of the archive call chain."""
    # note later date processing date -------------vvvvvvvv
    LA = landsat.landsatAsset
    return (LA('LC08_L1TP_012030_20170801_20170811_01_T1.tar.gz'),
            LA('LC08_L1TP_012030_20170801_20171231_01_T1.tar.gz'))

def t_Asset_archive_update_case(mocker, asset_and_replacement):
    """Tests Asset.archive with a single file and update=True"""
    # TODO more cases --^
    old_asset_obj, new_asset_obj = asset_and_replacement
    # interpret path as a single file
    mocker.patch.object(data_core.os.path, 'isdir').return_value = False
    # needs to return (asset object, link count, overwritten asset object)
    mocker.patch.object(landsat.landsatAsset, '_archivefile').return_value = (
            old_asset_obj, 1, new_asset_obj)
    # prevent exception for file-not-found
    mocker.patch.object(data_core, 'RemoveFiles')

    # setup complete; perform the call
    (actual_assets, actual_replaced_assets) = landsat.landsatAsset.archive(
            old_asset_obj.filename, update=True)

    assert (actual_assets == [old_asset_obj] and
            actual_replaced_assets == [new_asset_obj])

def t_Data_archive_assets_update_case(orm, mocker, asset_and_replacement):
    """Tests Data.archive_assets with a single file and update=True."""
    # TODO more cases --^
    old_asset_obj, new_asset_obj = asset_and_replacement
    mocker.patch.object(landsatData.Asset, 'archive').return_value = (
            [old_asset_obj], [new_asset_obj])
    # two of these should be deleted; the third should remain
    stale_product     = ('/archive/landsat/tiles/012030/2017213/'
                         '012030_2017213_LC8_rad.tif')
    stale_product_toa = ('/archive/landsat/tiles/012030/2017213/'
                         '012030_2017213_LC8_rad-toa.tif')
    keeper_product    = ('/archive/landsat/tiles/012030/2017213/'
                         '012030_2017213_LC8SR_landmask.tif')

    def m_lsd__init__(self, *args, **kwargs):
        self.filenames = {('fake-sensor', 'rad'): stale_product,
                          ('fake-sensor', 'rad-toa'): stale_product_toa,
                          ('fake-sensor', 'landmask'): keeper_product}

    # prevent the constructor from going out to the database/filesystem
    mocker.patch.object(landsatData, '__init__', m_lsd__init__)
    m_os_remove = mocker.patch.object(data_core.os, 'remove')
    m_delete_product = mocker.patch.object(data_core.dbinv, 'delete_product')

    # setup complete; call method being tested   vvvvvv-- mocked, don't care
    actual = landsat.landsatData.archive_assets("hi-mom", update=True)

    dt = datetime.datetime(2017, 8, 1, 0, 0)
    m_delete_product.assert_any_call(
        driver='landsat', product='rad', tile='012030', date=dt)
    m_delete_product.assert_any_call(
        driver='landsat', product='rad-toa', tile='012030', date=dt)
    assert m_delete_product.call_count == 2
    m_os_remove.assert_any_call(stale_product)
    m_os_remove.assert_any_call(stale_product_toa)
    assert m_os_remove.call_count == 2

def t_query_service_caching(mpo):
    bn, url = 'basename.hdf', 'http://www.himom.com/'
    m_available = mpo(modis.modisAsset, 'available')
    m_available.return_value = False
    modis.modisAsset.query_service.cache_clear() # in case it's not empty atm

    atd = ('MOD11A1', 'h12v04', datetime.datetime(2012, 12, 1, 0, 0))
    actual_first = modis.modisAsset.query_service(*atd)
    actual_second = modis.modisAsset.query_service(*atd)

    assert (m_available.call_count == 1 # should use the cache 2nd time
            and actual_first == actual_second == None)

class GipsDriverModules(object):
    """Introspect the GIPS codebase and load all the driver modules."""
    def __init__(self):
        self.load_driver_modules()

    def load_driver_modules(self):
        """Locate all gips drivers under gips.data and return them in a dict.

        Format is {'modis': <modis module object>, 'landsat': <object>..."""
        gips_data_dir_name = os.path.dirname(gips.data.__file__)
        driver_names = [
            name for (_, name, is_pkg)
            in pkgutil.iter_modules([gips_data_dir_name])
            if is_pkg and name is not 'core']
        driver_dirs = {dn: os.path.join(gips_data_dir_name, dn)
                       for dn in driver_names}
        fmtups = {dn: imp.find_module(dn, [dd]) for (dn, dd)
                  in driver_dirs.items()}
        modules = {dn: imp.load_module(dn, *fmtup)
                   for (dn, fmtup) in fmtups.items()}
        self.modules = modules

    def asset_classes(self):
        return {driver: module.__dict__[driver + 'Asset']
                for driver, module in self.modules.items()}

gips_driver_modules = GipsDriverModules()

@pytest.mark.parametrize('driver, asset_class',
                         gips_driver_modules.asset_classes().items())
def t_check_startdate_compliance(driver, asset_class):
    expected, actual = {}, {}
    for a_type, a_info in asset_class._assets.items():
        expected[a_type] = datetime.date
        actual[a_type] = type(a_info.get('startdate', None))

    assert expected == actual

@pytest.mark.parametrize('driver, asset_class',
                         gips_driver_modules.asset_classes().items())
def t_check_enddate_latency_compliance(driver, asset_class):
    busted_a_types = {} # asset types & reasons for failure
    for a_type, a_info in asset_class._assets.items():
        if 'enddate' in a_info:
            v, t = a_info['enddate'], datetime.date
        elif 'latency' in a_info:
            v, t = a_info['latency'], int
        else:
            busted_a_types[a_type] = "Neither 'enddate' nor 'latency' found"
            continue
        if not isinstance(v, t):
            busted_a_types[a_type] = 'Expected {} but got {}'.format(
                t, type(v))

    assert {} == busted_a_types
