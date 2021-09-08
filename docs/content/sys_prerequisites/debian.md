---
geekdocAlign: left
title: Ubuntu / Debian based OS's
weight: 99

---


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

