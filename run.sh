#!/usr/bin/env bash

source credentials.sh

docker run -it --rm --name gips -h gips \
    -v ${GIPSDIR}:/gips \
    -v ${ARCHIVEDIR}:/archive \
    --user gips gips
