#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# Get System packages installed
apt -y update
apt -y install \
        git \
        socat \
        rlwrap \
        screenkey \
        ffmpeg

# Install FZF
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# Mock konsole binary
touch /usr/bin/konsole
chmod 755 /usr/bin/konsole
