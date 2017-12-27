"""Known-good outcomes for tests, mostly stdout and created files."""

t_project_no_warp = {
    'compare_stdout': False,
    'created': {
        '0': None,
        '0/2017004_MOD_aod.tif': -124661770,
        '0/2017005_MOD_aod.tif': -1798929705,
        '0/2017006_MOD_aod.tif': 1354760932,
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
            'h01v01/h01v01_2017004_MOD_aod.tif': 190937103,
            'h01v01/h01v01_2017005_MOD_aod.tif': -1587512880,
            'h01v01/h01v01_2017006_MOD_aod.tif': -2112843720,
    }
}

