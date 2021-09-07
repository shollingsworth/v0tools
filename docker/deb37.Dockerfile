FROM python:3.7-bullseye

COPY ./docker/debinstall.sh /
COPY ./docker/install_msf.sh /

WORKDIR /
RUN ./debinstall.sh
RUN ./install_msf.sh

COPY . /app/

WORKDIR /app

RUN pip3 install .
