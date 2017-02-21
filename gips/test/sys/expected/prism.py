"""Known-good outcomes for tests, mostly stdout and created files."""

t_info = { 'stdout':  u"""\x1b[1mGIPS Data Repositories (v0.8.2)\x1b[0m
\x1b[1m
PRISM Products v0.0.1\x1b[0m
  Optional qualifiers listed below each product.
  Specify by appending '-option' to product (e.g., ref-toa)
\x1b[1m
Standard Products
\x1b[0m   ppt         Precipitate                             
   pptsum      Cumulative Precipitate                  
                 days: temporal window width (default: 3 days) .
   tmax        Daily Maximum Temperature               
   tmin        Daily Minimum Temperature               
""" }


t_inventory = {
    'stdout': u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site NHseacoast-0

\x1b[1mAsset Coverage for site NHseacoast-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
   CONUS       99.2%        0.0%

\x1b[1m\x1b[4m    DATE       _ppt     _tmax     _tmin    Product  \x1b[0m
\x1b[1m1982        
\x1b[0m    335       99.2%     99.2%     99.2%   
    336       99.2%     99.2%     99.2%   
    337       99.2%     99.2%     99.2%   


3 files on 3 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mprism: Daily Gridded Climate Data\x1b[0m
""",
}


t_process = {
    'updated': {
        'prism/tiles/CONUS/19821201': None,
        'prism/tiles/CONUS/19821202': None,
        'prism/tiles/CONUS/19821203': None
    },
    'created': {
        'prism/tiles/CONUS/19821201/CONUS_19821201_prism_ppt.tif': None,
        'prism/tiles/CONUS/19821201/CONUS_19821201_prism_tmax.tif': None,
        'prism/tiles/CONUS/19821201/CONUS_19821201_prism_tmin.tif': None,
        'prism/tiles/CONUS/19821202/CONUS_19821202_prism_ppt.tif': None,
        'prism/tiles/CONUS/19821202/CONUS_19821202_prism_tmax.tif': None,
        'prism/tiles/CONUS/19821202/CONUS_19821202_prism_tmin.tif': None,
        'prism/tiles/CONUS/19821203/CONUS_19821203_prism_ppt.tif': None,
        'prism/tiles/CONUS/19821203/CONUS_19821203_prism_tmax.tif': None,
        'prism/tiles/CONUS/19821203/CONUS_19821203_prism_tmin.tif': None,
        'prism/tiles/CONUS/19821203/CONUS_19821203_prism_pptsum-3.tif': -1313341182,
        'prism/tiles/CONUS/19821201/PRISM_tmax_stable_4kmD1_19821201_bil.zip.index': -74851230,
        'prism/tiles/CONUS/19821203/PRISM_ppt_stable_4kmD2_19821203_bil.zip.index': 1520480318,
        'prism/tiles/CONUS/19821203/PRISM_tmin_stable_4kmD1_19821203_bil.zip.index': -946867120,
        'prism/tiles/CONUS/19821202/PRISM_tmax_stable_4kmD1_19821202_bil.zip.index': 280913761,
        'prism/tiles/CONUS/19821202/PRISM_tmin_stable_4kmD1_19821202_bil.zip.index': 676175726,
        'prism/tiles/CONUS/19821203/PRISM_tmax_stable_4kmD1_19821203_bil.zip.index': -8647585,
        'prism/tiles/CONUS/19821202/PRISM_ppt_stable_4kmD2_19821202_bil.zip.index': -1251812608,
        'prism/tiles/CONUS/19821201/PRISM_tmin_stable_4kmD1_19821201_bil.zip.index': -1015405459,
        'prism/tiles/CONUS/19821201/PRISM_ppt_stable_4kmD2_19821201_bil.zip.index': 1582653443,
    },
    'ignored': [
        'gips-inv-db.sqlite3',
    ],
    '_inv_stdout': """\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site NHseacoast-0

\x1b[1mAsset Coverage for site NHseacoast-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
   CONUS       99.2%        0.0%

\x1b[1m\x1b[4m    DATE       _ppt     _tmax     _tmin    Product  \x1b[0m
\x1b[1m1982        
\x1b[0m    335       99.2%     99.2%     99.2%     \x1b[35mppt\x1b[0m  \x1b[35mtmax\x1b[0m  \x1b[35mtmin\x1b[0m
    336       99.2%     99.2%     99.2%     \x1b[35mppt\x1b[0m  \x1b[35mtmax\x1b[0m  \x1b[35mtmin\x1b[0m
    337       99.2%     99.2%     99.2%     \x1b[35mppt\x1b[0m  \x1b[35mpptsum-3\x1b[0m  \x1b[35mtmax\x1b[0m  \x1b[35mtmin\x1b[0m


3 files on 3 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mprism: Daily Gridded Climate Data\x1b[0m
""",
}
