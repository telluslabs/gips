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

# LOGGING is used for processes that generate log messages, such as workers.
# https://docs.python.org/2/library/logging.config.html#logging-config-dictschema
LOGGING = {
    'version': 1,
    'filters': {
        'dhfilter': {
            '()': 'gips.datahandler.custom_logging.DataHandlerLoggingFilter',
        },
    },
    'formatters': {
        'consoleformatter': {'format': '%(asctime)s %(message)s', 'dateformat': '%H:%M:%S'},
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler',
                    # This may be superior if RQ is installed:
                    # 'class': 'rq.utils.ColorizingStreamHandler',
                    'formatter': 'consoleformatter',
                    'level': 'DEBUG',
                    },
        'dhd': {
            'class': 'logging.handlers.SocketHandler',
            'host': GEOKIT_SERVER,
            'port': LOG_PORT,
            'filters': ['dhfilter'],
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console', 'dhd'],
        'level': 'DEBUG',
    },
    # this has to be specified explicitly to avoid breakage, but for unknown reasons
    # (maybe due to RQ's internal log config process)
    'loggers': { 'rq.worker': {} },
}

_format_string = ('%(levelname)s %(asctime)s --- %(dh_id)s:%(filename)s:%(funcName)s\n'
                  '%(message)s\n'
                  '--------------------------------------------------------')

# SERVER_LOGGING is used for configuring the datahandler logging server; it acts as a receiver
# for log messages, and this config determines how those log messages are handled.
SERVER_LOGGING = {
    'version': 1,
    'formatters': {
        'dhdformatter': {'format': _format_string},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'dhdformatter',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
