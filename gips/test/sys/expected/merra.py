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
    # test this too?  'frland': [],
    # t_process[srad] recording:
    'srad':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_srad.tif',
          'hash',
          'sha256',
          '882a44af70e337bf905c8695936f101792a518507a4304b23781a2f30aaabab4')],
    # t_process[tave] recording:
    'tave':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_tave.tif',
          'hash',
          'sha256',
          '5185aebd7cda54157cad2ddbde9f6fec4871c1b85fe78d0738634ba0211f2c9b')],
    # t_process[shum] recording:
    'shum':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_shum.tif',
          'hash',
          'sha256',
          '558f567c1e931891553d396f81b2b90929ad48a0ae88fa95d3894eae23ab3eba')],
    # t_process[rhum] recording:
    'rhum':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_rhum.tif',
          'hash',
          'sha256',
          '058161eb8488f1fb3df7f5c8719833c9d68c56aa082d4605938f62c2ee0035f6')],
    # t_process[tmin] recording:
    'tmin':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_tmin.tif',
          'hash',
          'sha256',
          '35a850769a3bb8f5209574ea4835bf417d8f99024567f4af9cdee9e623d0c567')],
    # t_process[tmax] recording:
    'tmax':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_tmax.tif',
          'hash',
          'sha256',
          '5963fcf346f388fc347355153996a078f1eb5ecbbc094394b72be382ba491865')],
    # t_process[prcp] recording:
    'prcp':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_prcp.tif',
          'hash',
          'sha256',
          '348fd7072ef0a8625f5268e29acbf3a69a959a412327102ef6558c992e62bc9f')],
    # t_process[patm] recording:
    'patm':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_patm.tif',
          'hash',
          'sha256',
          '7d9deca613973cb8ffb8f15a3dfa2013e6783556b520915e89b97fe41de638e3')],
    # t_process[wind] recording:
    'wind':
        [('data-root/merra/tiles/h01v01/2015135/h01v01_2015135_merra_wind.tif',
          'hash',
          'sha256',
          'a90c1d87fdb1c0926bd5b3004408a1f9d42ef08c38deb9d0572bc7536dbbf08a')],
}

t_project = {
    'created': {
        '0': None,
        '0/2015135_merra_patm.tif': 147353283,
        '0/2015135_merra_prcp.tif': 1755012780,
        '0/2015135_merra_rhum.tif': -157842459,
        '0/2015135_merra_shum.tif': -1248597053,
        '0/2015135_merra_srad.tif': 335947606,
        '0/2015135_merra_tave.tif': 362688260,
        '0/2015135_merra_tmax.tif': -711449232,
        '0/2015135_merra_tmin.tif': 1704871784,
        '0/2015135_merra_wind.tif': 1730702417,
    }
}

t_project_no_warp = {
    'created': {
        '0': None,
        '0/2015135_merra_patm.tif': -1358396856,
        '0/2015135_merra_prcp.tif': -853804546,
        '0/2015135_merra_rhum.tif': 1810084110,
        '0/2015135_merra_shum.tif': -451670363,
        '0/2015135_merra_srad.tif': -872759650,
        '0/2015135_merra_tave.tif': 1065221007,
        '0/2015135_merra_tmax.tif': 1169791704,
        '0/2015135_merra_tmin.tif': 892785210,
        '0/2015135_merra_wind.tif': -15824969,
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
        'h01v01/h01v01_2015135_merra_patm.tif': -700661020,
        'h01v01/h01v01_2015135_merra_prcp.tif': -61013249,
        'h01v01/h01v01_2015135_merra_rhum.tif': 191746518,
        'h01v01/h01v01_2015135_merra_shum.tif': -1653055419,
        'h01v01/h01v01_2015135_merra_srad.tif': 777698408,
        'h01v01/h01v01_2015135_merra_tave.tif': 479810606,
        'h01v01/h01v01_2015135_merra_tmax.tif': 366977711,
        'h01v01/h01v01_2015135_merra_tmin.tif': 882403888,
        'h01v01/h01v01_2015135_merra_wind.tif': 301026612,
    }
}

t_stats = {
    'created': {
        'patm_stats.txt': 1367728250,
        'prcp_stats.txt': 1367728250,
        'rhum_stats.txt': 1367728250,
        'shum_stats.txt': 1367728250,
        'srad_stats.txt': 1367728250,
        'tave_stats.txt': 1367728250,
        'tmax_stats.txt': 1367728250,
        'tmin_stats.txt': 1367728250,
        'wind_stats.txt': 1367728250,
    }
}
