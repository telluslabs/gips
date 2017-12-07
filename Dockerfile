# copied from a version jfisk had circa dec 5 2017
FROM ubuntu:16.04
  
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    python python-apt python-pip \
    gfortran libboost-all-dev libfreetype6-dev libgnutls-dev \
    libatlas-base-dev libgdal-dev libgdal1-dev gdal-bin python-numpy \
    python-scipy python-gdal swig2.0 
#    && rm -rf /var/lib/apt/lists/*
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y less vim
RUN pip install -U pip setuptools wheel

ADD requirements.txt /tmp/requirements.txt
ADD dev_requirements.txt /tmp/dev_requirements.txt
RUN pip install -r /tmp/dev_requirements.txt

ADD . /gips
RUN cd /gips && pip install . --process-dependency-links
#RUN cd /gips && pip install -e .[dh-rq] --process-dependency-links
#RUN rm -rf /gips
