"""Known-good outcomes for tests, mostly stdout and created files."""

t_process = {
    'compare_stderr': False,
    'updated': {
        'landsat/stage': None,
        'landsat/tiles/012030/2015352': None
    },
    'created': {
        'landsat/tiles/012030/2015352/012030_2015352_LC8_acca.tif': -531492048,
        'landsat/tiles/012030/2015352/012030_2015352_LC8_bqashadow.tif': -1819149482,
        'landsat/tiles/012030/2015352/012030_2015352_LC8_ndvi-toa.tif': 329107382,
        'landsat/tiles/012030/2015352/012030_2015352_LC8_rad-toa.tif': -1222249885,
        'landsat/tiles/012030/2015352/012030_2015352_LC8_ref-toa.tif': -871936054,
        'landsat/tiles/012030/2015352/LC08_L1GT_012030_20151218_20170224_01_T2.tar.gz.index': -394988487,
        'landsat/tiles/012030/2015352/LC08_L1GT_012030_20151218_20170224_01_T2_MTL.txt': -1453474890,
    },
    'ignored': [
        'gips-inv-db.sqlite3',
    ]
}

t_process_acolite = {
    'created': {
        'landsat/tiles/012030/2017213/012030_2017213_LC8_acoflags.tif': -514981863,
        'landsat/tiles/012030/2017213/012030_2017213_LC8_fai.tif': -1820016301,
        'landsat/tiles/012030/2017213/012030_2017213_LC8_oc2chl.tif': -794776169,
        'landsat/tiles/012030/2017213/012030_2017213_LC8_oc3chl.tif': 337875725,
        'landsat/tiles/012030/2017213/012030_2017213_LC8_rhow.tif': 1044772611,
        'landsat/tiles/012030/2017213/012030_2017213_LC8_spm655.tif': 1437263134,
        'landsat/tiles/012030/2017213/012030_2017213_LC8_turbidity.tif': -1347918033,
    },
    'updated': {
        'landsat/stage': None,
        'landsat/tiles/012030/2017213': None
    },
    'ignored': [
        'gips-inv-db.sqlite3',
    ],
}

t_project = {
    'compare_stderr': False,
    'created': {
        '0': None,
        '0/2015352_LC8_acca.tif': 402348046,
        '0/2015352_LC8_bqashadow.tif': 923940030,
        '0/2015352_LC8_ndvi-toa.tif': 728893178,
        '0/2015352_LC8_rad-toa.tif': -1053542955,
        '0/2015352_LC8_ref-toa.tif': -1149010214,
    }
}

t_project_no_warp = {
    'compare_stderr': False,
    'created': {
        '0': None,
        '0/2015352_LC8_acca.tif': -126711306,
        '0/2015352_LC8_bqashadow.tif': 1681911857,
        '0/2015352_LC8_ndvi-toa.tif': 1662486138,
        '0/2015352_LC8_rad-toa.tif': -196115636,
        '0/2015352_LC8_ref-toa.tif': -1147999741,
    }
}

# TODO this bug rearing its ugly head again?
# See https://github.com/Applied-GeoSolutions/gips/issues/54
t_tiles = { 'created': {'012030': None}}

t_tiles_copy = {
    'compare_stderr': False,
    'created': {
        '012030': None,
        '012030/012030_2015352_LC8_acca.tif': 176561467,
        '012030/012030_2015352_LC8_bqashadow.tif': 912021217,
        '012030/012030_2015352_LC8_ndvi-toa.tif': -1333295744,
        '012030/012030_2015352_LC8_rad-toa.tif': 1609412102,
        '012030/012030_2015352_LC8_ref-toa.tif': -1797834447,
    }
}

t_stats = { 'created': {
    'acca_stats.txt': -174967201,
    'bqashadow_stats.txt': 1868908586,
    'ndvi-toa_stats.txt': -1084861813,
    'rad-toa_stats.txt': -545320378,
    'ref-toa_stats.txt': -1132928652,
}}
