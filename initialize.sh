#rm -rf /archive/*

bash authorize.sh
gips_config env

#wget -O aod.composites.tgz ftp://${AGSFTPCREDS}@agsftp.ags.io/gipsftp/aod.composites.tar.gz
tar xfvz aod.composites.tgz -C /archive
#rm aod.composites.tgz
