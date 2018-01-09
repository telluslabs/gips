"""Known-good outcomes for tests, mostly stdout and created files."""

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
