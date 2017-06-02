#!/bin/bash

# This script manages the deployment of the datahandler
# to a fresh linux container:
#
# if a container named $CONT doesn't exist, this:
#  + launches a fesh container named $CONT
#  + updates it
#  + installs some system package requirements
#  + snapshots it
# endif
# + restores the container to its `pipped` snapshot
# +
set -e
CONT=dh
SNAP=pipped

function create_or_reset_container() {
    lxc info $CONT 2>/dev/null 1>/dev/null || {
        lxc launch ubuntu-daily:16.04 $CONT
        sleep 10
        lxc exec $CONT -- apt-get update
        sleep 10
        lxc exec $CONT -- apt-get install -y python python-apt python-pip
        # extra due to strange apt fetching issue
        lxc exec $CONT -- apt-get install -y gfortran libboost-all-dev libfreetype6-dev libgnutls-dev libatlas-base-dev libgdal-dev libgdal1-dev gdal-bin python-numpy python-scipy python-gdal swig2.0
        lxc exec $CONT -- pip install -U pip
    } ;

    HAVE_SNAP=$(lxc info $CONT | grep ${SNAP} || true)
    echo "HAVE_SNAP: $HAVE_SNAP"
    if [ "$HAVE_SNAP" ] ; then
        lxc restore $CONT $SNAP ;
        echo "$CONT restored to snapshot $SNAP"
    else
        lxc snapshot $CONT $SNAP ;
        echo "$CONT snapshot taken as $SNAP"
    fi
    if $(lxc list $CONT | grep STOPPED) ; then
        lxc start $CONT
        sleep 1
    fi
}

read -sp "Enter your NASA EarthData username: " EDUSER
echo ''
read -sp "Enter your NASA EarthData password: " EDPASS
echo ''
create_or_reset_container
lxc file push install_datahandler.py $CONT/root/
lxc exec $CONT -- python /root/install_datahandler.py \
    --drivers modis merra \
    --earthdata-user $EDUSER \
    --earthdata-password $EDPASS \
    --enable-cron \
    --install-pg \
    --create-db \
    --enable-daemons
