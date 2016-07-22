import datetime

import pytest

from ...data.modis import modis

dt = datetime.datetime

# everything for NH's tile for Dec 1 2012:
params = (
    (
        ('MOD11A2', 'h12v04', dt(2012, 12, 1, 0, 0)),               # call
        'http://e4ftl01.cr.usgs.gov/MOLT/MOD11A2.005/2012.12.01',   # passed to urlopen
    ),
    (
        ('MYD11A1', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOLA/MYD11A1.005/2012.12.01',
    ),

    (
        ('MOD11A1', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOLT/MOD11A1.005/2012.12.01',
    ),

        # probably test separately; it preumaturely returns
        # ('MCD12Q1', 'h12v04', dt(2012, 12, 1, 0, 0)),

    (
        ('MCD43A2', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOTA/MCD43A2.005/2012.12.01',
    ),

    (
        ('MOD09Q1', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOLT/MOD09Q1.005//2012.12.01',
    ),

    (
        ('MCD43A4', 'h12v04', dt(2012, 12, 1, 0, 0)),
        'http://e4ftl01.cr.usgs.gov/MOTA/MCD43A4.005/2012.12.01',
    ),
)


@pytest.fixture
def fetch_mocks(mocker):
    urlopen = mocker.patch.object(modis.urllib, 'urlopen')

    # called in a loop for items in the listing that match criteria
    urlopen2 = mocker.patch.object(modis.urllib2, 'urlopen')
    conn = urlopen2.return_value
    # conn.read.return_value = "omnia dicta fortiora si dicta Latina."
    open = mocker.patch.object(modis, 'open')
    file = open.return_value
    return (urlopen, urlopen2, conn, open, file)


class T_modisAsset_fetch(object):

    @pytest.mark.parametrize("call, expected", params)
    def t_no_matching_listings(self, fetch_mocks, call, expected):
	"""Unit test for modisAsset.fetch; uses mocking to prevent I/O."""
	(urlopen, urlopen2, conn, open, file) = fetch_mocks

	# give the listing from which names of asset files are extracted
	urlopen.return_value.readlines.return_value = ("not", "your", "files")

	modis.modisAsset.fetch(*call)

        # It should skip the I/O code except for fetching the directory listing
        uncalled_fns = (conn.read, urlopen2, open, file.write, file.close)
        readlines = urlopen.return_value.readlines
        assert not any([f.called for f in uncalled_fns]) and all([
            readlines.call_count == 1,
            readlines.call_args  == (),
            urlopen.call_count   == 1,
            urlopen.call_args    == ((expected,), {}) # (args, kwargs)
        ])
