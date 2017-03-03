"""Known-good outcomes for tests, mostly stdout and created files."""

t_inventory = { 'stdout': u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site durham-0

\x1b[1mAsset Coverage for site durham-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
   19TCH      100.0%        0.1%

\x1b[1m\x1b[4m    DATE       L1C     Product  \x1b[0m
\x1b[1m2017        
\x1b[0m    010       100.0%   
    030       100.0%   


2 files on 2 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mS2A: Sentinel-2, Satellite A\x1b[0m
\x1b[31mS2B: Sentinel-2, Satellite B\x1b[0m
"""
}

t_process = {
    'compare_stderr': False,
    'updated': {
        'sentinel2/tiles/19TCH/2017010': None,
    },
    'created': {
        # jan 10
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_bi-toa.tif': 541673910,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_brgt-toa.tif': 38425695,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_crc-toa.tif': -692365694,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_crcm-toa.tif': -838929383,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_evi-toa.tif': -850280958,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_isti-toa.tif': -1580129686,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_lswi-toa.tif': 1676471139,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_msavi2-toa.tif': -536630164,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_ndsi-toa.tif': -2118476257,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_ndti-toa.tif': -716676364,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_ndvi-toa.tif': 1460522898,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_ref-toa.tif': -711062552,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_satvi-toa.tif': 1636524188,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_sti-toa.tif': 530354401,
        'sentinel2/tiles/19TCH/2017010/19TCH_2017010_S2A_vari-toa.tif': 1830182386,
        # jan 30
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_bi-toa.tif': -1803674796,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_brgt-toa.tif': 38425695,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_crc-toa.tif': 1709338205,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_crcm-toa.tif': -409438165,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_evi-toa.tif': 323913491,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_isti-toa.tif': -1749541518,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_lswi-toa.tif': 2114258079,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_msavi2-toa.tif': 2091111873,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_ndsi-toa.tif': 1825007655,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_ndti-toa.tif': 42954357,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_ndvi-toa.tif': 1854221224,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_ref-toa.tif': -1762824208,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_satvi-toa.tif': 102386778,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_sti-toa.tif': 1625215040,
        #'sentinel2/tiles/19TCH/2017030/19TCH_2017030_S2A_vari-toa.tif': -1662958906,
    },
    'ignored': [
        'gips-inv-db.sqlite3',
        'sentinel2/tiles/19TCH/2017010/S2A_MSIL1C_20170110T153611_N0204_R111_T19TCH_20170110T154029.zip',
        'sentinel2/tiles/19TCH/2017030',
        'sentinel2/tiles/19TCH/2017030/S2A_MSIL1C_20170130T153551_N0204_R111_T19TCH_20170130T153712.zip',
    ],
    '_inv_stdout': u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site durham-0

\x1b[1mAsset Coverage for site durham-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
   19TCH      100.0%        0.1%

\x1b[1m\x1b[4m    DATE       L1C     Product  \x1b[0m
\x1b[1m2017        
\x1b[0m    010       100.0%     \x1b[35mbi-toa\x1b[0m  \x1b[35mbrgt-toa\x1b[0m  \x1b[35mcrc-toa\x1b[0m  \x1b[35mcrcm-toa\x1b[0m  \x1b[35mevi-toa\x1b[0m  \x1b[35misti-toa\x1b[0m  \x1b[35mlswi-toa\x1b[0m  \x1b[35mmsavi2-toa\x1b[0m  \x1b[35mndsi-toa\x1b[0m  \x1b[35mndti-toa\x1b[0m  \x1b[35mndvi-toa\x1b[0m  \x1b[35mref-toa\x1b[0m  \x1b[35msatvi-toa\x1b[0m  \x1b[35msti-toa\x1b[0m  \x1b[35mvari-toa\x1b[0m


1 files on 1 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mS2A: Sentinel-2, Satellite A\x1b[0m
\x1b[31mS2B: Sentinel-2, Satellite B\x1b[0m
"""
}


t_info = { 'stdout': u"""\x1b[1mGIPS Data Repositories (v0.8.2)\x1b[0m
\x1b[1m
Sentinel-2 Products v0.1.0\x1b[0m
\x1b[1m
Index Products
\x1b[0m   bi          Brightness Index                        
   evi         Enhanced Vegetation Index               
   lswi        Land Surface Water Index                
   ndsi        Normalized Difference Snow Index        
   ndvi        Normalized Difference Vegetation Index  
\x1b[1m
Standard Products
\x1b[0m   ref         Surface reflectance                     
"""
}
