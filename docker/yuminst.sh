#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

yum update -y
yum install -y \
    nmap-ncat \
    socat \
    readline-devel \
    epel-release \
    python3-pip \
    which \
    python3-devel

yum -y group install "Development Tools"
yum -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
yum -y install \
    ffmpeg \
    ffmpeg-devel



# FZF
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# rlwrap
git clone https://github.com/hanslub42/rlwrap.git ~/rlwrap
cd /root/rlwrap
autoreconf --install
./configure
make
make install

# Mock binaries we don't actually want to install it
touch /usr/bin/konsole
chmod 755 /usr/bin/konsole

# can't get this to work on centos
touch /usr/bin/screenkey
chmod 755 /usr/bin/screenkey
