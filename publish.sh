#!/bin/bash

TAG=latest
ECR_URI=304548020545.dkr.ecr.us-east-1.amazonaws.com/telluslabs/gips1
eval $(aws ecr get-login --region us-east-1 --no-include-email)
docker tag telluslabs/gips1:$TAG $ECR_URI:$TAG
docker push $ECR_URI:$TAG
