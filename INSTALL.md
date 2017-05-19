# Set up system

Run apt-get update

`sudo apt-get update`

Install python, python-pip, and virtualenv 

```
sudo apt-get install -y python python-pip virtualenv
```

Clone the GIPS datahandler repositiory from GitHub

`git clone -b batch-scheduler https://github.com/Applied-GeoSolutions/gips.git`

# Create and activate a virtual environment

```
virtualenv --system-site-packages dh_venv
. dh_venv/bin/activate
```

# Install and Configure GIPS datahandler 

The GIPS datahandler is installed and configured using a convenience script named `install_datahandler.py`. A typical installation would use options such as the following:

```
python install_datahandler.py --gips-version '.' --driver modis merra --earthdata-user $USER --earthdata-password $PASSWORD --install-pg --create-db --enable-cron --enable-daemons
```

  * `--gips-version '.'`: install the version currently in your cloned repository
  * `--drivers modis merra`: enable the MODIS and MERRA data drivers
  * `--earthdata-user` and `--earthdata-password`: login credentials for EarthData ( https://earthdata.nasa.gov )
  * `--install-pg`: install the postgres database software -- not necessary if you plan on using an existing installation
  * `--create-db`: create the postgres database, user and grant privileges
  * `--enable-cron`: installs the `scheduler` crontab entry into the current users crontab
  * `--enable-daemons`: create `systemd` service configurations for the `rq` task queues and `xmlrpc` API server

There are a wide variety of additional optional arguments available, particularly database name, location and authentication, as well as hostname and ports for the associated daemon processes. See `python install_datahandler.py --help` for more details. The configuration options in use can be viewed using `gips_config print`

Once this installation is complete, you can launch the two necessary daemons using the following commands:
```
sudo systemctl start gips_dhd.service
sudo systemctl start gips_rqworker@{1..4}.service
```
The above command will launch four `rq` workers.

Unless specified otherwise, the xmlrpc API server will be listening on `localhost:8001` and logs written to `/var/log/gipd_dhd.log` 
