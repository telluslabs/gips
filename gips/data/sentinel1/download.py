import gips.data.sentinel1.sentinel_api.sentinel_api as api
import os

# use username and password for ESA DATA Hub authentication
#username = os.getenv('USERNAME')
#password = os.getenv('PASSWORD')

username = "rbraswell"
password = "eurocoolness"

#assert ((username is not None) and (password is not None))

# please also specify the Hub URL:
# All Sentinel-1 and -2 scenes beginning from 15th Nov. 2015: https://scihub.copernicus.eu/apihub/
# All historic Sentinel-1 scenes: https://scihub.copernicus.eu/dhus/
s1 = api.SentinelDownloader(username, password, api_url='https://scihub.copernicus.eu/apihub/')

# set directory for
# - filter scenes list with existing files
# - set directory path for data download
s1.set_download_dir('/archive/sentinel1/stage')

# load geometries from shapefile
#s1.load_sites('/archive/vector/{0}.shp'.format(os.getenv('SHAPEFILE')))
s1.load_sites('/archive/vector/563_344_boundary.shp')


start_date = "2018-04-09"
end_date = "2018-04-09"

# search for scenes with some restrictions (e.g., minimum overlap 1%)
s1.search('S1A*', min_overlap=0.01, start_date=start_date, end_date=end_date,
          date_type='beginPosition', productType='GRD', sensoroperationalmode='IW')

# add another search query (e.g., for Sentinel-1B); both search results will be merged
s1.search('S1B*', min_overlap=0.01, start_date=start_date, end_date=end_date,
          date_type='beginPosition', productType='GRD', sensoroperationalmode='IW')

# you can either write results to a bash file for wget or download files directly in this script
# s1.write_results('wget', 'sentinel_api_s1_download.sh')
s1.download_all()
