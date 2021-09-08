---
description: Welcome to v0tools!
geekdocAlign: left
geekdocDescription: Welcome to v0tools!
title: Home
weight: 99

---

[![github-issues](https://img.shields.io/github/issues/shollingsworth/v0tools?style=plastic "github-issues")](https://github.com/shollingsworth/v0tools/issues) [![github-languages-code-size](https://img.shields.io/github/languages/code-size/shollingsworth/v0tools?style=plastic "github-languages-code-size")](https://github.com/shollingsworth/v0tools) [![github-stars](https://img.shields.io/github/stars/shollingsworth/v0tools?style=plastic "github-stars")](https://github.com/shollingsworth/v0tools/stargazers) [![github-forks](https://img.shields.io/github/forks/shollingsworth/v0tools?style=plastic "github-forks")](https://github.com/shollingsworth/v0tools/network/members) 

[![pypi-v](https://img.shields.io/pypi/v/v0tools?style=plastic "pypi-v")](https://pypi.org/project/v0tools) [![pypi-status](https://img.shields.io/pypi/status/v0tools?style=plastic "pypi-status")](https://pypi.org/project/v0tools) [![pypi-l](https://img.shields.io/pypi/l/v0tools?style=plastic "pypi-l")](https://pypi.org/project/v0tools) [![pypi-dm](https://img.shields.io/pypi/dm/v0tools?style=plastic "pypi-dm")](https://pypi.org/project/v0tools) [![pypi-pyversions](https://img.shields.io/pypi/pyversions/v0tools?style=plastic "pypi-pyversions")](https://pypi.org/project/v0tools) [![pypi-implementation](https://img.shields.io/pypi/implementation/v0tools?style=plastic "pypi-implementation")](https://pypi.org/project/v0tools) 
{{< toc >}}
**This package is for those participating in hacking CTFs and want some tools to help with some of the more tedious tasks.**

**Enjoy!**

**Pull requests welcome. :)**




## Quickstart / Install
{{< expand "Arch Linux" "..." >}}

```bash
# Python / Package Pre-reqs
sudo pacman -S python-pip
```


```bash
# Provides fzf, konsole, socat, rlwrap, ffmpeg, nc, msfvenom, msfconsole, screenkey
sudo pacman -S fzf konsole socat rlwrap ffmpeg nmap metasploit screenkey

```


```bash
# install pip package
pip3 install v0tools
```

{{< /expand >}}
{{< expand "Ubuntu / Debian based OS's" "..." >}}

```bash
# Python / Package Pre-reqs
sudo apt install python3-pip
```


```bash
# Provides fzf, konsole, socat, rlwrap, ffmpeg, nc, msfvenom, msfconsole, screenkey
sudo apt install fzf konsole socat rlwrap ffmpeg ncat screenkey

# Install msfvenom
curl https://apt.metasploit.com/metasploit-framework.gpg.key | apt-key add -
echo deb http://apt.metasploit.com buster main >> /etc/apt/sources.list
apt update
apt install -y metasploit-framework

```


```bash
# install pip package
pip3 install v0tools
```

{{< /expand >}}
{{< expand "RHEL/CentOS/Fedora" "..." >}}

```bash
# Python / Package Pre-reqs
sudo yum -y install python3-pip python3-devel gcc git
```


```bash
# Provides fzf, konsole, socat, rlwrap, ffmpeg, nc, msfvenom, msfconsole, screenkey
sudo yum -y install konsole socat nmap-ncat screenkey

# Install fzf
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
source ~/.bashrc

# Install rlwrap
sudo yum -y group install "Development Tools"
sudo yum -y install readline-devel
git clone https://github.com/hanslub42/rlwrap.git
cd rlwrap
autoreconf --install
./configure
make
sudo make install

# Install ffmpeg
sudo yum -y install epel-release
sudo yum -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
sudo yum -y install ffmpeg ffmpeg-devel

# Install msfvenom
curl https://apt.metasploit.com/metasploit-framework.gpg.key > /tmp/msf.asc
rpm --import /tmp/msf.asc
sudo yum -y install yum-utils
sudo yum-config-manager --add-repo=https://rpm.metasploit.com/
sudo yum -y install metasploit-framework.x86_64

```


```bash
# install pip package
pip3 install v0tools
```

{{< /expand >}}
## Api
> **API Documentation can be found [here](https://v0tools.stev0.me/api)**
## Toc
{{< toc-tree >}}
