"""Known-good outcomes for tests, mostly stdout and created files."""

t_project = {
    'compare_stdout': False,
    'compare_stderr': False,
    'created': {
        '0': None,
        '0/2017004_MOD_aod.tif': -766418958,
        '0/2017005_MOD_aod.tif': 1283286056,
        '0/2017006_MOD_aod.tif': -2004417139,
    }
}

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

t_stats = {
    'stdout': u"""\x1b[1mGIPS Image Statistics (v0.1.0)\x1b[0m
Stats for Project directory: /tmp/test-output
Calculating statistics for 2017-01-04
Calculating statistics for 2017-01-05
Calculating statistics for 2017-01-06
""",
    'created': {
        'aod_stats.txt': -769515142
    }
}
