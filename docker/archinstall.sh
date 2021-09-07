#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

pacman -Syu --noconfirm
pacman -S --noconfirm \
        nmap \
        fzf \
        socat \
        rlwrap \
        ffmpeg \
        python-pip \
        make \
        git \
        screenkey \
        python3


# Mock konsole we don't actually want to install it
touch /usr/bin/konsole
chmod 755 /usr/bin/konsole
