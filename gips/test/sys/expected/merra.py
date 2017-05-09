"""Known-good outcomes for tests, mostly stdout and created files."""

t_info = { 'stdout':  u"""\x1b[1mGIPS Data Repositories (v0.8.2)\x1b[0m
\x1b[1m
merra Products v1.0.0\x1b[0m
\x1b[1m
Standard Products
\x1b[0m   frland      Fraction of land (fraction)             
   patm        Surface atmospheric pressure (mb)       
   prcp        Daily total precipitation (mm day-1)    
   rhum        Relative humidity (%)                   
   shum        Relative humidity (kg kg-1)             
   srad        Incident solar radiation (W m-2)        
   tave        Ave daily air temperature data (K)      
   tmax        Max daily air temperature data          
   tmin        Min daily air temperature data          
   wind        Daily mean wind speed (m s-1)           
""" }


t_inventory = {
    'stdout': u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site NHseacoast-0

\x1b[1mAsset Coverage for site NHseacoast-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
  h01v01      100.0%        0.0%

\x1b[1m\x1b[4m    DATE       ASM       FLX       RAD       SLV     Product  \x1b[0m
\x1b[1m2015        
\x1b[0m    135                 100.0%     100.0%     100.0%   


1 files on 1 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mmerra: Modern Era Retrospective-analysis for Research and Applications\x1b[0m
"""
}


t_process = {
    'updated': {'merra/tiles/h01v01/2015135': None},
    'created': {
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_patm.tif': -832862627,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_prcp.tif': -1814551991,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_rhum.tif': 1203124684,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_shum.tif': -97846975,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_srad.tif': -1745572576,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_tave.tif': 165650774,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_tmax.tif': 463728356,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_tmin.tif': -1469140067,
	'merra/tiles/h01v01/2015135/h01v01_2015135_merra_wind.tif': 1771906367,
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
  h01v01      100.0%        0.0%

\x1b[1m\x1b[4m    DATE       ASM       FLX       RAD       SLV     Product  \x1b[0m
\x1b[1m2015        
\x1b[0m    135                 100.0%     100.0%     100.0%     \x1b[35mpatm\x1b[0m  \x1b[35mprcp\x1b[0m  \x1b[35mrhum\x1b[0m  \x1b[35mshum\x1b[0m  \x1b[35msrad\x1b[0m  \x1b[35mtave\x1b[0m  \x1b[35mtmax\x1b[0m  \x1b[35mtmin\x1b[0m  \x1b[35mwind\x1b[0m


1 files on 1 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mmerra: Modern Era Retrospective-analysis for Research and Applications\x1b[0m
""",
}

t_project = {
    'created': {
        '0': None,
        '0/1982335_merra_patm.tif': -1194096458,
        '0/1982335_merra_prcp.tif': -921844888,
        '0/1982335_merra_rhum.tif': 1745414028,
        '0/1982335_merra_shum.tif': 417603371,
        '0/1982335_merra_srad.tif': -954280707,
        '0/1982335_merra_tave.tif': 1924194126,
        '0/1982335_merra_tmax.tif': -166083279,
        '0/1982335_merra_tmin.tif': 387002882,
        '0/1982335_merra_wind.tif': -1497701075,
        '0/1982336_merra_patm.tif': -1191517626,
        '0/1982336_merra_prcp.tif': 1315767506,
        '0/1982336_merra_rhum.tif': 1747029372,
        '0/1982336_merra_shum.tif': 63867242,
        '0/1982336_merra_srad.tif': 1082004295,
        '0/1982336_merra_tave.tif': 1922676158,
        '0/1982336_merra_tmax.tif': -164581439,
        '0/1982336_merra_tmin.tif': 389568754,
        '0/1982336_merra_wind.tif': 567943831,
        '0/1982337_merra_patm.tif': 238208553,
        '0/1982337_merra_prcp.tif': 860702276,
        '0/1982337_merra_rhum.tif': -555112173,
        '0/1982337_merra_shum.tif': -1140328086,
        '0/1982337_merra_srad.tif': 1029591505,
        '0/1982337_merra_tave.tif': -1001287215,
        '0/1982337_merra_tmax.tif': 1090030510,
        '0/1982337_merra_tmin.tif': -1578074979,
        '0/1982337_merra_wind.tif': 1559912449,
    }
}

t_project_no_warp = {
    'created': {
        '0': None,
        '0/1982335_merra_patm.tif': -200939895,
        '0/1982335_merra_prcp.tif': 476729020,
        '0/1982335_merra_rhum.tif': 1881289075,
        '0/1982335_merra_shum.tif': -266188484,
        '0/1982335_merra_srad.tif': -295322069,
        '0/1982335_merra_tave.tif': 57100650,
        '0/1982335_merra_tmax.tif': 1384839193,
        '0/1982335_merra_tmin.tif': 1305954097,
        '0/1982335_merra_wind.tif': -1883883804,
        '0/1982336_merra_patm.tif': -324096410,
        '0/1982336_merra_prcp.tif': 1578328747,
        '0/1982336_merra_rhum.tif': 706517899,
        '0/1982336_merra_shum.tif': 1826967430,
        '0/1982336_merra_srad.tif': -870962363,
        '0/1982336_merra_tave.tif': 964633652,
        '0/1982336_merra_tmax.tif': -424248397,
        '0/1982336_merra_tmin.tif': -1512048653,
        '0/1982336_merra_wind.tif': -2077895192,
        '0/1982337_merra_patm.tif': -957718525,
        '0/1982337_merra_prcp.tif': 1906386999,
        '0/1982337_merra_rhum.tif': 536898658,
        '0/1982337_merra_shum.tif': -1866900765,
        '0/1982337_merra_srad.tif': -2062677144,
        '0/1982337_merra_tave.tif': -473239447,
        '0/1982337_merra_tmax.tif': -556754512,
        '0/1982337_merra_tmin.tif': 1413034388,
        '0/1982337_merra_wind.tif': -927923442,
     }
}

# haven't ever used tiles
t_tiles = {
    'created': {
        'h01v01': None,
   },
}

t_tiles_copy = {
    'created': {
        'h01v01': None,
        'h01v01/h01v01_1982335_merra_patm.tif': 1814180181,
        'h01v01/h01v01_1982335_merra_prcp.tif': 1257409151,
        'h01v01/h01v01_1982335_merra_rhum.tif': -190565914,
        'h01v01/h01v01_1982335_merra_shum.tif': -2101265486,
        'h01v01/h01v01_1982335_merra_srad.tif': -2033706964,
        'h01v01/h01v01_1982335_merra_tave.tif': -1894854482,
        'h01v01/h01v01_1982335_merra_tmax.tif': 803457496,
        'h01v01/h01v01_1982335_merra_tmin.tif': 879158605,
        'h01v01/h01v01_1982335_merra_wind.tif': -926149814,
        'h01v01/h01v01_1982336_merra_patm.tif': -928795564,
        'h01v01/h01v01_1982336_merra_prcp.tif': -1127494438,
        'h01v01/h01v01_1982336_merra_rhum.tif': -951401242,
        'h01v01/h01v01_1982336_merra_shum.tif': -15455067,
        'h01v01/h01v01_1982336_merra_srad.tif': 309053247,
        'h01v01/h01v01_1982336_merra_tave.tif': -1729387075,
        'h01v01/h01v01_1982336_merra_tmax.tif': 379446921,
        'h01v01/h01v01_1982336_merra_tmin.tif': 1618171658,
        'h01v01/h01v01_1982336_merra_wind.tif': -1251411284,
        'h01v01/h01v01_1982337_merra_patm.tif': -503681924,
        'h01v01/h01v01_1982337_merra_prcp.tif': 806657839,
        'h01v01/h01v01_1982337_merra_rhum.tif': -1619657092,
        'h01v01/h01v01_1982337_merra_shum.tif': -1500337138,
        'h01v01/h01v01_1982337_merra_srad.tif': -76875084,
        'h01v01/h01v01_1982337_merra_tave.tif': -5910063,
        'h01v01/h01v01_1982337_merra_tmax.tif': 1531039402,
        'h01v01/h01v01_1982337_merra_tmin.tif': 1249094654,
        'h01v01/h01v01_1982337_merra_wind.tif': 473398098,
    }
}

t_stats = {
    'created': {
        'patm_stats.txt': -262438993,
        'prcp_stats.txt': -262438993,
        'rhum_stats.txt': -262438993,
        'shum_stats.txt': -262438993,
        'srad_stats.txt': -262438993,
        'tave_stats.txt': -262438993,
        'tmax_stats.txt': -262438993,
        'tmin_stats.txt': -262438993,
        'wind_stats.txt': -262438993,
    }
}
