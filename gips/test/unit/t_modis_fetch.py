"""Unit tests for data.modis.modis.modisAsset.fetch."""

import sys
import datetime
import urllib2

import pytest

from ...data.modis import modis

dt = datetime.datetime

# probably test separately; it preumaturely returns: ('MCD12Q1', 'h12v04', dt(2012, 12, 1, 0, 0)),

# everything for NH's tile for Dec 1 2012 that fails:
http_404_params = (
    (('MOD11A2', 'h12v04', dt(2012, 12, 1, 0, 0)),                  # call
        'http://e4ftl01.cr.usgs.gov/MOLT/MOD11A2.005/2012.12.01'),  # passed to urlopen

    (('MCD43A2', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOTA/MCD43A2.005/2012.12.01'),

    (('MOD09Q1', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOLT/MOD09Q1.005//2012.12.01'),

    (('MCD43A4', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOTA/MCD43A4.005/2012.12.01'),
)


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
def fetch_mocks(mocker):
    """Mock out all I/O used in modisAsset.fetch; used for unit tests below."""
    urlopen = mocker.patch.object(modis.urllib, 'urlopen')

    # called in a loop for items in the listing that match criteria
    get = mocker.patch.object(modis.requests, 'get')
    response = get.return_value
    open = mocker.patch.object(modis, 'open')
    file = open.return_value
    return (urlopen, get, response, open, file)


@pytest.mark.parametrize("call, expected", http_404_params)
def t_no_matching_listings(fetch_mocks, call, expected):
    """Unit test for modisAsset.fetch for assets that 404."""
    (urlopen, get, response, open, file) = fetch_mocks

    # give the listing from which names of asset files are extracted
    urlopen.return_value.readlines.return_value = model_404

    modis.modisAsset.fetch(*call)

    # It should skip the I/O code except for fetching the directory listing
    uncalled_fns = (response.iter_content, get, open, file.write)
    readlines = urlopen.return_value.readlines
    assert not any([f.called for f in uncalled_fns]) and all([
        readlines.call_count == 1,
        readlines.call_args  == (),
        urlopen.call_count   == 1,
        urlopen.call_args    == ((expected,), {}) # (args, kwargs)
    ])


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
    (('MYD11A1', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOLA/MYD11A1.005/2012.12.01',
        MYD11A1_listing, # HTML index page
        'MYD11A1.A2012336.h12v04.005.2012341040543.hdf'),

    (('MOD11A1', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOLT/MOD11A1.005/2012.12.01',
        MOD11A1_listing, # HTML index page
        'MOD11A1.A2012336.h12v04.005.2012339180517.hdf'),
)


@pytest.mark.parametrize("call, listing_url, listing, asset_fn", http_200_params)
def t_matching_listings(fetch_mocks, call, listing_url, listing, asset_fn):
    """test modisAsset.fetch:  Query server, extract URL, then download it."""
    (urlopen, urlopen2, conn, open, file) = fetch_mocks

    # give the listing from which names of asset files are extracted
    urlopen.return_value.readlines.return_value = listing
    conn.read.return_value == ("If you think you understand, you don't.  "
                               "If you think you don't understand, you still don't.")

    modis.modisAsset.fetch(*call)

    # These assertions are too involved, possibly, because fetch() does too much
    readlines = urlopen.return_value.readlines
    (open_fn, open_mode) = open.call_args[0] # [1] is kwargs remember
    assert all([
        readlines.call_count == 1,
        readlines.call_args  == (),
        urlopen.call_count   == 1,
        urlopen.call_args    == ((listing_url,), {}), # (args, kwargs)
        urlopen2.call_count  == 1,
        urlopen2.call_args   == ((listing_url + '/' + asset_fn,), {}),
        open.call_count      == 1,
        open_fn.endswith(asset_fn),
        open_mode            == 'wb',
        conn.read.call_count == 1,
        conn.read.call_args  == (),
        # not checking file.close because its failure is believed to be low-impact.
        file.write.call_count == 1,
        file.write.call_args  == ((conn.read.return_value,), {}),
    ])


@pytest.mark.parametrize("call, listing_url, listing, asset_fn", http_200_params)
def t_auth_error(fetch_mocks, mocker, call, listing_url, listing, asset_fn):
    """Confirm auth failures are handled gracefully."""
    (urlopen, urlopen2, conn, open, file) = fetch_mocks
    print_mock = mocker.patch.object(modis, 'print') # to confirm user notification is produced

    urlopen.return_value.readlines.return_value = listing # coerce the loop to start

    # rig urllib2.urlopen to explode
    urlopen2.side_effect = urllib2.HTTPError('http://example.com/', 401, 'Unauthorized', None, None)

    modis.modisAsset.fetch(*call)

    assert all([
        not open.called, # Confirm short-circuiting by showing open was never called
        print_mock.call_count == 2,
        # making sure the errors go to stderr important; precise wording probably isn't
        print_mock.mock_calls[0][-1] == dict(file=sys.stderr),
        print_mock.mock_calls[1][-1] == dict(file=sys.stderr),
    ])
