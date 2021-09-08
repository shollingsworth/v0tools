---
geekdocAlign: left
title: RHEL/CentOS/Fedora
weight: 99

---


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

