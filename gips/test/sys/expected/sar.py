"""Known-good outcomes for tests, mostly stdout and created files."""

t_info = { 'stdout':  u"""""" }


t_inventory = {
    'stdout': u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site tiles

\x1b[1mAsset Holdings for tile N07E099\x1b[0m
\x1b[1m\x1b[4m    DATE      alos1     alos2    Product  \x1b[0m
\x1b[1m2015        
\x1b[0m    101                 100.0%   


1 files on 1 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mAFBD: PALSAR FineBeam Dual Polarization\x1b[0m
\x1b[31mAFBS: PALSAR FineBeam Single Polarization\x1b[0m
\x1b[32mAWB1: PALSAR WideBeam (ScanSAR Short Mode)\x1b[0m
\x1b[34mAWBD: PALSAR-2 WideBeam (ScanSAR w/Ortho Slope Correction)\x1b[0m
\x1b[33mJFBS: JERS-1 FineBeam Single Polarization\x1b[0m
""",
}

otro = u"""\x1b[1mGIPS Data Inventory (v0.8.2)\x1b[0m
Retrieving inventory for site tiles

\x1b[1mAsset Holdings for tile N07E099\x1b[0m
\x1b[1m\x1b[4m    DATE      alos1     alos2    Product  \x1b[0m
\x1b[1m2015        
\x1b[0m    101                 100.0%   


1 files on 1 dates
\x1b[1m
SENSORS\x1b[0m
\x1b[35mAFBD: PALSAR FineBeam Dual Polarization\x1b[0m
\x1b[31mAFBS: PALSAR FineBeam Single Polarization\x1b[0m
\x1b[32mAWB1: PALSAR WideBeam (ScanSAR Short Mode)\x1b[0m
\x1b[34mAWBD: PALSAR-2 WideBeam (ScanSAR w/Ortho Slope Correction)\x1b[0m
\x1b[33mJFBS: JERS-1 FineBeam Single Polarization\x1b[0m
"""


t_process = {
    'updated': {
    },
    'created': {
    },
    '_symlinks': {
    },
    'ignored': [
        'gips-inv-db.sqlite3',
    ],
    '_inv_stdout': """
""",
}

t_project = {
    'created': {
    }
}

t_project_no_warp = {
    'created': {'0': None,
    }
}


t_tiles_copy = {
    'created': {
    }
}

t_tiles_copy = {
    'created': {
    }
}

t_stats = { 
    'created': {
    }
}

