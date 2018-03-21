REPOS['sentinel2'] = {
    'repository': '$TLD/sentinel2',
    # sign up for access to data source here:  https://scihub.copernicus.eu/dhus/#/self-registration
    'username': ESA_USER,
    'password': ESA_PASS,
    'extract': False,  # extract files from tar.gz before processing instead of direct access
}
