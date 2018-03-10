YOUR_REPO='/home/rbraswell/repo/gips'
cd ${YOUR_REPO}
export AGSFTPCREDS=gipstest:3sqrt2
wget -O sixs ftp://$AGSFTPCREDS@agsftp.ags.io/gipsftp/sixs
wget -O gitlab_ci ftp://$AGSFTPCREDS@agsftp.ags.io/gipsftp/gitlab_ci
wget -O gips_creds.sh.enc ftp://$AGSFTPCREDS@agsftp.ags.io/gipsftp/gips_creds.sh.enc
docker build -t gippy-0.x -f docker/gippy-install.docker docker
docker build -t gips_test  -f docker/gips-ci.docker .
docker system prune -f
docker run --rm -e GIPS_OVERRIDE_VERSION=0.8.2 gips_test pytest -vv --setup-repo --slow --sys -k 'cdl'
