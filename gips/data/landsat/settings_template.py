REPOS['landsat'] = {
    'repository': '$TLD/landsat',
    # Landsat specific settings
    '6S': False,            # atm correction for VIS/NIR/SWIR bands
    'MODTRAN': False,       # atm correction for LWIR
    'extract': False,       # extract files from tar.gz before processing instead of direct access
    # 'ACOLITE_DIR':  '',   # ACOLITE installation for atm correction over water
}
