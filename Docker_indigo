FROM geographica/gdal2:latest

COPY . /gips
WORKDIR /gips

RUN apt-get -y update \
    && apt-get install -y \
       python3-pip \
       curl \
       wget \
       gfortran \
       libgnutls28-dev \
       emacs-nox

RUN mkdir /tmp/sixs \
    && curl http://rtwilson.com/downloads/6SV-1.1.tar -o /tmp/sixs/6SV-1.1.tar \
    && cd /tmp/sixs \
    && tar xf 6SV-1.1.tar \
    && cd /tmp/sixs/6SV1.1 \
    && sed -i 's/g77/gfortran -std=legacy -ffixed-line-length-none -ffpe-summary=none/g' Makefile \
    && make \
    && mv sixsV1.1 /usr/local/bin/sixs \
    && rm -rf /tmp/sixs

RUN pip3 install gippy \
    && pip3 install https://bitbucket.org/chchrsc/rios/downloads/rios-1.4.3.zip#egg=rios-1.4.3 \
    && pip3 install https://bitbucket.org/chchrsc/python-fmask/downloads/python-fmask-0.5.0.zip#egg=python-fmask-0.5.0 \
    && python3 setup.py develop

RUN apt-get -y autoremove \
    && apt-get -y autoclean
