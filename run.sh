# non-fancy run GIPS container
LOCAL_ARCHIVE="/mnt/storage"
docker run -v $HOME:/root -v $PWD/gips:/gips/gips -v ${LOCAL_ARCHIVE}/gips:/archive -it --rm gips-user bash
