"""Unit tests for data.modis.modis.modisAsset.fetch."""

import sys
import os
import datetime
import urllib2


import pytest
import mock

from gips import core
from ...data.modis import modis

dt = datetime.datetime

# probably test separately; it preumaturely returns: ('MCD12Q1', 'h12v04', dt(2012, 12, 1, 0, 0)),

# everything for NH's tile for Dec 1 2012 that fails:
http_404_params = (
    ('MOD11A2', 'h12v04', dt(2012, 12, 1, 0, 0),
        # passed to managed_request
        'https://e4ftl01.cr.usgs.gov/MOLT/MOD11A2.006/2012.12.01'),
    ('MCD43A2', 'h12v04', dt(2012, 12, 1, 0, 0),
        'https://e4ftl01.cr.usgs.gov/MOTA/MCD43A2.006/2012.12.01'),
    ('MOD09Q1', 'h12v04', dt(2012, 12, 1, 0, 0),
        'https://e4ftl01.cr.usgs.gov/MOLT/MOD09Q1.006/2012.12.01'),
    ('MCD43A4', 'h12v04', dt(2012, 12, 1, 0, 0),
        'https://e4ftl01.cr.usgs.gov/MOTA/MCD43A4.006/2012.12.01'),
)


# not presently used
model_404 = (
    '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">\n',
    '<html><head>\n',
    '<title>404 Not Found</title>\n',
    '</head><body>\n',
    '<h1>Not Found</h1>\n',
    # shouldn't matter what it says here vvv
    '<p>The requested URL /MOLT/MOD11A2.005/2012.12.01 was not found on this server.</p>\n',
    '</body></html>\n',
)

@pytest.fixture
def fetch_mocks(mpo, mocker):
    """Mock out all I/O used in modisAsset.fetch; used for unit tests below."""
    # called once to get a listing of files then again when one is chosen to download
    m_get_setting = mpo(modis.modisRepository, 'get_setting')
    m_get_setting.return_value = 'driver-dir'
    managed_request = mpo(modis.modisRepository, 'managed_request')
    content = mocker.Mock(code=200, msg='OK')
    managed_request.return_value = content
    open = mpo(modis, 'open')
    file = open.return_value.__enter__.return_value # context manager
    return (managed_request, m_get_setting, content, open, file)

@pytest.mark.parametrize('a_type, tile, date, url', http_404_params)
def t_managed_request_returns_none(fetch_mocks, a_type, tile, date, url):
    """Unit test for handling cases when managed_request returns None.

    This happens for any 4xx error, 5xx error, and similar."""
    # setup & mocks
    (managed_request, m_get_setting, content, open, file) = fetch_mocks
    managed_request.return_value = None

    # call
    actual = modis.modisAsset.fetch(a_type, tile, date, 'whatever.hdf', url)

    # assertions:
    assert ([] == actual
            and (url,) == managed_request.call_args[0]
            # It should skip the I/O code except for managed_request
            and 0 == open.call_count)

# VERY truncated snippet of an actual listing file
MYD11A1_listing = [
    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n',
    '<html>\n',
    ' <head>\n',
    '  <title>Index of /MOLA/MYD11A1.005/2012.12.01</title>\n',
    ' </head>\n',
    ' <body>\n',
    '<pre><img src="/icons/blank.gif" alt="Icon "> <a href="?C=N;O=D">Name</a>',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MYD11A1.A2012336.h12v03.005.2012341040539.hdf">'
        'MYD11A1.A2012336.h12v03.005.2012341040539.hdf</a>          2012-12-05 22:15  2.4M  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MYD11A1.A2012336.h12v03.005.2012341040539.hdf.xml">'
        'MYD11A1.A2012336.h12v03.005.2012341040539.hdf.xml</a>      2012-12-06 02:22   11K  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MYD11A1.A2012336.h12v04.005.2012341040543.hdf">'
        'MYD11A1.A2012336.h12v04.005.2012341040543.hdf</a>          2012-12-05 22:15  1.2M  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MYD11A1.A2012336.h12v04.005.2012341040543.hdf.xml">'
        'MYD11A1.A2012336.h12v04.005.2012341040543.hdf.xml</a>      2012-12-06 02:22  9.5K  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MYD11A1.A2012336.h12v05.005.2012341040552.hdf">'
        'MYD11A1.A2012336.h12v05.005.2012341040552.hdf</a>          2012-12-05 22:15  382K  \n',
    '<hr></pre>\n',
    '</body></html>\n'
]


MOD11A1_listing = [
    '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n',
    '<html>\n',
    ' <head>\n',
    '  <title>Index of /MOLT/MOD11A1.005/2012.12.01</title>\n',
    ' </head>\n',
    ' <body>\n',
    '<pre><img src="/icons/blank.gif" alt="Icon "> <a href="?C=N;O=D">Name</a>',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MOD11A1.A2012336.h12v02.005.2012339180538.hdf.xml">'
        'MOD11A1.A2012336.h12v02.005.2012339180538.hdf.xml</a>      2012-12-05 02:13   14K  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MOD11A1.A2012336.h12v03.005.2012339180912.hdf">'
        'MOD11A1.A2012336.h12v03.005.2012339180912.hdf</a>          2012-12-04 12:29  3.6M  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MOD11A1.A2012336.h12v03.005.2012339180912.hdf.xml">'
        'MOD11A1.A2012336.h12v03.005.2012339180912.hdf.xml</a>      2012-12-05 02:13   10K  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MOD11A1.A2012336.h12v04.005.2012339180517.hdf">'
        'MOD11A1.A2012336.h12v04.005.2012339180517.hdf</a>          2012-12-04 12:29  1.8M  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MOD11A1.A2012336.h12v04.005.2012339180517.hdf.xml">'
        'MOD11A1.A2012336.h12v04.005.2012339180517.hdf.xml</a>      2012-12-05 02:13  9.0K  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MOD11A1.A2012336.h12v05.005.2012339042544.hdf">'
        'MOD11A1.A2012336.h12v05.005.2012339042544.hdf</a>          2012-12-03 23:44  385K  \n',
    '<img src="/icons/unknown.gif" alt="[   ]">'
        '<a href="MOD11A1.A2012336.h12v05.005.2012339042544.hdf.xml">'
        'MOD11A1.A2012336.h12v05.005.2012339042544.hdf.xml</a>      2012-12-04 02:12  9.4K  \n',
    '<hr></pre>\n',
    '</body></html>\n'
]

# everything for NH's tile for Dec 1 2012 that succeeds, including both inputs and outputs
http_200_params = (
    ('MYD11A1', 'h12v04', dt(2012, 12, 1, 0, 0),
        'MYD11A1.A2012336.h12v04.005.2012341040543.hdf',
        'https://e4ftl01.cr.usgs.gov/MOLT/MOD11A1.006/2012.12.01/himom.hdf'),

    ('MOD11A1', 'h12v04', dt(2012, 12, 1, 0, 0),
        'MOD11A1.A2012336.h12v04.005.2012339180517.hdf',
         'https://e4ftl01.cr.usgs.gov/MOLT/MOD11A1.006/2012.12.01/himom.hdf'),
)

# fake asset contents
asset_content = ("If you think you understand, you don't.\n"
                 "If you think you don't understand, you still don't.")

@pytest.mark.parametrize('a_type, tile, date, asset_fn, url', http_200_params)
def t_http_matching_listings(mocker, fetch_mocks, a_type, tile, date, asset_fn, url):
    """Query http server, extract asset URL, then download it."""
    (managed_request, m_get_setting, content, open, file) = fetch_mocks
    content.read.return_value = asset_content

    expected = ['driver-dir/stage/' + asset_fn]
    actual = modis.modisAsset.fetch(a_type, tile, date, asset_fn, url)

    # assertions
    assert (expected == actual
            and (url,) == managed_request.call_args[0]
            and 1 == content.read.call_count
            # did we open the right filename?
            and open.call_args[0][0].endswith(asset_fn)
            # file write assertions:  open(...) as fd && fd.write(...)
            and (asset_content,) == file.write.call_args[0])
