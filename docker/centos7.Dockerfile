FROM centos:7

COPY ./docker/yuminst.sh /
COPY ./docker/install_msf.sh /

WORKDIR /
RUN ./yuminst.sh
RUN ./install_msf.sh

COPY . /app/
WORKDIR /app

RUN pip3 install .
