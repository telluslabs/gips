rm -rf /Users/braswell/data/gips
docker run --rm --name gips -h gips -v /Users/braswell/data/gips:/archive gips gips_config env
tar xfvz composites.tgz -C /Users/braswell/data/gips/aod/
docker run -it --rm --name gips -h gips -v /Users/braswell/data/gips:/archive gips
