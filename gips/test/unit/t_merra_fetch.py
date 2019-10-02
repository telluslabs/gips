"""Unit tests for merraAsset.fetch."""

import datetime

from gips.data.merra import merra

# VERY truncated snippet of an actual listing file; python 3 urlwhatever emits bytes hence encode():
FLX_listing = [l.encode() for l in [
    '<html xmlns="https://www.w3.org/1999/xhtml">\n',
    '<head>\n',
    '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" />\n',
    '<meta name="description" content="Default Index Page">\n',
    '        <title>NASA IT Security Warning Banner</title>\n',
    '</head>\n',
    '\n',
    '<p>\n',
    '    Once registered, you can blah balbh albhabl abhlab',
    '</p>\n',
    '<table><tr><th><img src="/icons/blank.gif" alt="[ICO]"></th><th>Name</th>'
    '<th>Last modified</th><th>Size</th></tr><tr><th colspan="4"><hr></th></tr>\n',

    '<tr><td valign="top"><a href="/data/MERRA2/M2T1NXFLX.5.12.4/2015/">'
    '<img src="/icons/back.gif" alt="[DIR]"></a></td><td>'
    '<a href="/data/MERRA2/M2T1NXFLX.5.12.4/2015/">Parent Directory</a></td>'
    '<td>&nbsp;</td><td align="right">  - </td></tr>\n',

    # this line is the one that trips the query method
    '<tr><td valign="top"><a href="MERRA2_400.tavg1_2d_flx_Nx.20150515.nc4">'
    '<img src="/icons/unknown.gif" alt="[   ]"></a></td><td>'
    '<a href="MERRA2_400.tavg1_2d_flx_Nx.20150515.nc4">'
    'MERRA2_400.tavg1_2d_flx_Nx.20150515.nc4</a></td>'
    '<td align="right">31-Jul-2015 00:40  </td><td align="right">380M</td>'
    '</tr>\n',

    '<tr><td valign="top"><a href="MERRA2_400.tavg1_2d_flx_Nx.20150515.nc4.xml">'
    '<img src="/icons/text.gif" alt="[TXT]"></a></td><td>'
    '<a href="MERRA2_400.tavg1_2d_flx_Nx.20150515.nc4.xml">'
    'MERRA2_400.tavg1_2d_flx_Nx.20150515.nc4.xml</a></td><td align="right">'
    '31-Jul-2015 00:41  </td><td align="right">3.1K</td></tr>\n',

    '<tr><td valign="top"><a href="MERRA2_400.tavg1_2d_flx_Nx.20150531.nc4.xml">'
    '<img src="/icons/text.gif" alt="[TXT]"></a></td><td>'
    '<a href="MERRA2_400.tavg1_2d_flx_Nx.20150531.nc4.xml">'
    'MERRA2_400.tavg1_2d_flx_Nx.20150531.nc4.xml</a></td><td align="right">'
    '31-Jul-2015 00:59  </td><td align="right">3.1K</td></tr>\n',

    '<tr><th colspan="4"><hr></th></tr>\n',
    '</table>\n',
    '<p>\n',
    '</body>\n',
    '</html>\n',
]]

def t_fetch_asset_found_case(mocker, mock_context_manager):
    """Query http server, extract asset URL, then download it."""

    # various useful values
    listing_url = ('https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/'
                   'M2T1NXFLX.5.12.4/2015/05')
    asset_fn = 'MERRA2_400.tavg1_2d_flx_Nx.20150515.nc4'

    ### mocks
    open = mocker.patch.object(merra, 'open')
    file = open.return_value.__enter__.return_value # context manager
    # called once to get a listing of files then again when one is chosen to download
    managed_request = mocker.patch.object(merra.merraRepository, 'managed_request')
    listing = mocker.Mock(code=200, msg='OK')
    listing.__iter__ = mocker.Mock(return_value=iter(FLX_listing))
    content = mocker.Mock(code=200, msg='OK')
    managed_request.side_effect = [listing, content]
    # don't care about these, just need them to not do I/O
    mock_context_manager(merra.utils, 'make_temp_dir', 'fake-temp-dir')
    mocker.patch.object(merra, 'Dataset')
    mocker.patch.object(merra.os, 'rename')

    # faked content of the fetched asset
    content_data = ("If you think you understand, you don't.\n"
                    "If you think you don't understand, you still don't.")
    content.read.return_value = content_data

    ### call being tested
    actual =  merra.merraAsset.fetch('FLX', 'h01v01', datetime.datetime(2015, 5, 15))

    ### assertions
    assert len(actual) == 1 and actual[0].endswith(asset_fn)
    assert mocker.call(listing_url, 2, 0) == managed_request.call_args_list[0]
    # request assertions:  response = request.get(...) && response.iter_content()
    managed_request.assert_called_with(listing_url + '/' + asset_fn)
    content.read.assert_called_once_with()
    # file write assertions:  open(...) as fd && fd.write(...)
    assert open.call_args[0][0].endswith(asset_fn) # did we open the right filename?
    file.write.assert_called_once_with(content_data)
