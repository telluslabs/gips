#!/usr/bin/env bash

TAG=${1:-latest}

docker login registry.gitlab.com
docker build -t registry.gitlab.com/rbraswell/gips:${TAG} .
docker push registry.gitlab.com/rbraswell/gips:${TAG}
