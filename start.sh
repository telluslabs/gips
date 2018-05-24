#!/usr/bin/env bash

ARCHIVEDIR=/mnt/storage/gips_octopus
GIPSDIR=${PWD}

source credentials.sh

docker run -itd --rm -v ${GIPSDIR}:/gips -v ${ARCHIVEDIR}:/archive --name gips_octopus registry.gitlab.com/rbraswell/gips

docker exec gips_octopus bash initialize.sh
