FROM ubuntu:16.04

RUN apt-get -y update \
    && apt-get install -y \
    python python-apt \
    python-pip \
    gfortran \
    libboost-all-dev \
    libfreetype6-dev \
    libgnutls-dev \
    libatlas-base-dev \
    libgdal-dev \
    libgdal1-dev \
    gdal-bin \
    python-numpy \
    python-scipy \
    python-gdal \
    swig2.0 \
    wget \
    emacs-nox \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip setuptools wheel

COPY . /gips

RUN cd /gips \
    && pip install -r dev_requirements.txt \
    && pip install -e . --process-dependency-links \
    && mv sixs /usr/local/bin/sixs

VOLUME /archive
VOLUME /gips
WORKDIR /gips


#COPY trial.sh /trial.sh
#RUN chmod +x /trial.sh
#CMD /trial.sh
