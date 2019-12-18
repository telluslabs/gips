# non-fancy run GIPS container
docker run -v /mnt/storage/gips:/archive -v ${PWD}/gips:/gips/gips -v ${HOME}:/root -it --rm gips1 bash
