#!/usr/bin/env bash

source credentials.sh

docker build -t gips --no-cache -f Dockerfile \
    --build-arg UID=$(id -u) \
    --squash .

docker run --rm \
    -v ${GIPSDIR}:/gips \
    -v ${ARCHIVEDIR}:/archive \
    gips bash initialize.sh
