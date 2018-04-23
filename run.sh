docker run -it --rm --name gips -h gips \
    -v /home/braswell/repo/gips-rb:/gips \
    -v /data/gips:/archive \
    --user $(id -un) gips
