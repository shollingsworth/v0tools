FROM archlinux:base

COPY ./docker/arch.mirrorlist /etc/pacman.d/mirrorlist
COPY ./docker/archinstall.sh /
COPY ./docker/install_msf.sh /

WORKDIR /
RUN ./archinstall.sh
RUN ./install_msf.sh

COPY . /app/

WORKDIR /app

RUN pip3 install .
