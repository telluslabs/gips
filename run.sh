rm -rf /Users/braswell/data/gips
docker run --rm --name gips -h gips -v /Users/braswell/data/gips:/archive gips gips_config env
tar xfvz composites.tgz -C /Users/braswell/data/gips/aod/
# override version for testing only
docker run -it --rm --name gips -h gips -e GIPS_OVERRIDE_VERSION=0.8.2 -v /Users/braswell/data/gips:/archive gips
