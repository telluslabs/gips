## Installation

Currently the datahandler xmlrpc and logging daemon are started from an upstart script:

usage: `sudo service geokitd start`

`/etc/init/geokitd.conf`

```
# start geokitd
# shawn patti

start on runlevel [2345]

script

export VIRTUAL_ENV="/usr/local/dh_venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

alias pydoc="python -m pydoc"
echo $$ > /var/run/geokitd.pid

exec /usr/local/dh_venv/bin/geokitd.py >> /var/log/geokitd.log 2>&1

end script

pre-start script
  echo "[`date`] Starting Geokitd" >> /var/log/geokitd.log
end script

pre-stop script
  rm /var/run/geokitd.pid
  echo "[`date`] Stopping Geokitd" >> /var/log/geokitd.log
end script
```

### Installing RQ

When you run `install.sh`, specify `dhrq` as an argument to install the redis-server system
package, and to install RQ into the python virtualenv.


## Configuration

The ORM is required to run the datahandler, therefore set the environment variable `GIPS_ORM=true`.

### Configuring the Datahandler

Set these gips settings; the values given are useful for a local dev setup:

```
GEOKIT_SERVER = 'localhost'
XMLRPC_PORT   = 9000
LOG_PORT      = 9001
LOG_LEVEL     = 1
EXPORT_DIR = '/path/to/export'

# for gips acting as a front-end, attempting to send API requests,
# where can it find the installed API server?
DH_API_SERVER = 'http://localhost:9000/'
```

### Configuring TORQUE

To use TORQUE set these settings:

```
# path to the correct python binary on the worker node
REMOTE_PYTHON = '/path/to/.worker-venv/bin/python'
# named queue to which jobs should be submitted
TORQUE_QUEUE  = 'somequeue@someserver.io'
# prints out the generated torque jobs; may enable more debugging in the future
DH_DEBUG = True
# see nodes entry in:
# http://docs.adaptivecomputing.com/torque/4-0-2/Content/topics/2-jobs/requestingRes.htm
TORQUE_NODE   = 'worker-node'
# place to put torque job output files
TORQUE_OUTPUT = '/path/to/torque-output'
```

### Configuring RQ

Set this GIPS setting to choose RQ & Redis as the job queueing system instead of TORQUE:

```
TASK_QUEUE = 'rq'
```

In addition these GIPS settings may be required; the example values are defaults:

```
RQ_QUEUE_NAME   = 'datahandler' # RQ supports named queues
RQ_TASK_TIMEOUT = 8 * 3600      # seconds, thus 8 hours

# These are also redis's defaults
RQ_REDIS_HOST     = 'localhost'
RQ_REDIS_PORT     = 6379
RQ_REDIS_DB       = 0
RQ_REDIS_PASSWORD = None        # ie no password
```

#### Development Mode

It is assumed that a python virtualenv is activated, the one created by `install.sh`.

Once the redis system package is installed, redis should be running.  Its defaults should
match RQ's defaults, thus no additional config is necessary.  Start an RQ worker to listen for
jobs, and geokitd to listen to for logging and API connections:

```
$ rq worker datahandler # if you set RQ_QUEUE_NAME, change 'datahandler' to that value
$ python gips/datahandler/scripts/geokitd.py
```

Now calls can be submitted to the datahandler API, either through the XMLRPC interface or via
python call.  The API call will require access to whatever database is configured for the GIPS ORM:

```
#!/usr/bin/env python

import datetime
from gips.datahandler import api

product_name = 'modis_fsnow_fractional-snow-cover'
shp_full_path = '/path/to/some/shapefile.shp'
four_years_ago = datetime.datetime.now() - datetime.timedelta(years=4)

job_id = api.submit_job('tolson-test-site', product_name,
        {'key':'shaid', 'site': shp_full_path}, {'dates': four_years_ago.strftime('%Y-%j')})
print "Got a job id: ", job_id
```

After that, one may manually run the scheduler to emulate the cron job that periodically checks for
new work and schedules it:

```
$ python gips/datahandler/scheduler.py
```
