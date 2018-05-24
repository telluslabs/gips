#!/usr/bin/env bash

bash authorize.sh
gips_config env
tar xfvz aod.composites.tgz -C /archive
