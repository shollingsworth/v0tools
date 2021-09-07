#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

if grep -i centos /etc/os-release; then
    curl https://apt.metasploit.com/metasploit-framework.gpg.key > /tmp/msf.asc
    rpm --import /tmp/msf.asc
    yum -y install yum-utils
    yum-config-manager --add-repo=https://rpm.metasploit.com/
    yum -y install metasploit-framework.x86_64
elif grep -i debian /etc/os-release; then
    curl https://apt.metasploit.com/metasploit-framework.gpg.key | apt-key add -
    echo deb http://apt.metasploit.com buster main >> /etc/apt/sources.list
    apt update
    apt install -y metasploit-framework
elif grep -i arch /etc/os-release; then
    pacman -S --noconfirm metasploit
else
    echo "Error, unknown distro"
    cat /etc/os-release
    exit 1
fi


# Mock konsole we don't actually want to install it
touch /usr/bin/konsole
chmod 755 /usr/bin/konsole
