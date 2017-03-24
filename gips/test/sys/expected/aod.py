"""Known-good outcomes for tests, mostly stdout and created files."""

t_info = { 'stdout':  u"""""" }


t_inventory = {
    'stdout': u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site NE-0

\x1b[1mAsset Coverage for site NE-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
  h01v01      100.0%      100.0%

\x1b[1m\x1b[4m    DATE      MOD08    Product  \x1b[0m
\x1b[1m2017        
\x1b[0m    004       100.0%     \x1b[35maod\x1b[0m
    005       100.0%     \x1b[35maod\x1b[0m
    006       100.0%     \x1b[35maod\x1b[0m


3 files on 3 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mMOD: MODIS Terra\x1b[0m
""",
}


t_process = {
    'updated': {
    },
    'created': {
    },
    'ignored': [
        'gips-inv-db.sqlite3',
    ],
    '_inv_stdout': """\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site NE-0

\x1b[1mAsset Coverage for site NE-0\x1b[0m
\x1b[1m
Tile Coverage
\x1b[4m  Tile      % Coverage   % Tile Used\x1b[0m
  h01v01      100.0%      100.0%

\x1b[1m\x1b[4m    DATE      MOD08    Product  \x1b[0m
\x1b[1m2017        
\x1b[0m    004       100.0%     \x1b[35maod\x1b[0m
    005       100.0%     \x1b[35maod\x1b[0m
    006       100.0%     \x1b[35maod\x1b[0m


3 files on 3 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mMOD: MODIS Terra\x1b[0m
""",
}

t_project = {
    'created': {
    }
}

t_project_no_warp = {
    'created': {
     }
}

# haven't ever used tiles
t_tiles = {
    'created': {
   },
}

t_tiles_copy = {
    'created': {
    }
}

t_stats = {
    'created': {
    }
}
