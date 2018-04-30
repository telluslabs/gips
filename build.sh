docker build -t gips --no-cache -f Dockerfile \
    --build-arg UID=$(id -u) \
    .


docker run --rm \
    -v /home/braswell/repo/gips-rb:/gips \
    -v /data/gips:/archive \
    gips bash initialize.sh

#docker run --rm \
#    -v /home/braswell/repo/gips-rb:/gips \
#    -v /data/gips:/archive \
#    gips bash initialize.sh
