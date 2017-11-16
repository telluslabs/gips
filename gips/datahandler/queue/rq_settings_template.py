TASK_QUEUE      = 'rq'
RQ_QUEUE_NAME   = '$QUEUE_NAME' # RQ supports named queues
RQ_TASK_TIMEOUT = 8 * 3600      # seconds, thus 8 hours

# These are also redis's defaults
RQ_REDIS_HOST     = '$QUEUE_SERVER'
RQ_REDIS_PORT     = 6379
RQ_REDIS_DB       = 0
RQ_REDIS_PASSWORD = None        # ie no password
