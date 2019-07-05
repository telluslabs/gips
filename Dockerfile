FROM gippy-0.3.x

ARG GIPS_UID
RUN apt-get update \
    && apt-get -y install libcurl4-gnutls-dev \
        python-geopandas awscli

COPY . /gips

COPY gips_init/sixs /usr/local/bin/sixs
COPY gips_init/ortho /usr/local/bin/ortho

ENV GIPS_OVERRIDE_VERSION='0.0.0-dev'

# note settings.py is removed, then regenerated with gips_config, then edited.
# pre-install cython to work around a cftime issue; no longer needed when this
# is fixed:  https://github.com/Unidata/cftime/issues/34
# GIPS_ORM is set false for hls; once hls is compatible with the ORM, that
# line can be removed
RUN cd /gips \
    && chmod +x /usr/local/bin/sixs \
    && chmod +x /usr/local/bin/ortho \
    && pip install -U pip 'idna<2.8' Cython \
    && /usr/local/bin/pip install -r dev_requirements.txt \
    && /usr/local/bin/pip install -e file:///gips/ \
    && rm -f /gips/gips/settings.py /gips/pytest.ini \
    && gips_config env -r /archive -e rbraswell@indigoag.com \
    && eval $(cat gips_creds.sh) \
    && sed -i~ \
 	   -e "s/^EARTHDATA_USER.*/EARTHDATA_USER = \"${EARTHDATA_USER}\"/" \
 	   -e "s/^EARTHDATA_PASS.*/EARTHDATA_PASS = \"${EARTHDATA_PASS}\"/" \
	   -e "s/^USGS_USER.*/USGS_USER = \"${USGS_USER}\"/" \
 	   -e "s/^USGS_PASS.*/USGS_PASS = \"${USGS_PASS}\"/" \
	   -e "s/^ESA_USER.*/ESA_USER = \"${ESA_USER}\"/" \
 	   -e "s/^ESA_PASS.*/ESA_PASS = \"${ESA_PASS}\"/" \
           /gips/gips/settings.py \
    && echo 'GIPS_ORM = False\n' >> /gips/gips/settings.py \
    && tar xfvz gips_init/aod.composites.tgz -C /archive > /dev/null \
    && pip install --no-cache-dir -U sharedmem \
    && pip install --no-cache-dir https://github.com/indigo-ag/multitemporal/archive/v1.0.0-in02.zip \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /gips/gips_init* \
    && apt-get -y autoremove \
    && apt-get -y autoclean

COPY docker/pytest-ini /gips/pytest.ini

WORKDIR /gips
