GEOKIT_SERVER = '$DH_SERVER'
XMLRPC_PORT   = $DH_PORT
# Port to log to on GEOKIT_SERVER
LOG_PORT      = $DH_LOG_PORT
# Logging verbosity level
LOG_LEVEL     = 1
# scratch space to put gips export files
EXPORT_DIR    = '$DH_EXPORT_DIR'

DATABASES['inventory'] = {
    #'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '$DB_NAME',
    'USER': '$DB_USER',
    'PASSWORD': '$DB_PASSWORD',
    'HOST': '$DB_HOST',
    'PORT': '$DB_PORT',
}
