#!/usr/bin/env bash

docker login registry.gitlab.com
docker build -t registry.gitlab.com/rbraswell/gips .
docker push registry.gitlab.com/rbraswell/gips
