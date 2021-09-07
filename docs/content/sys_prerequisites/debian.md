
```bash
# Provides fzf, konsole, socat, rlwrap, ffmpeg, nc, msfvenom, msfconsole, screenkey
sudo apt install fzf konsole socat rlwrap ffmpeg ncat screenkey

# Install msfvenom
curl https://apt.metasploit.com/metasploit-framework.gpg.key | apt-key add -
echo deb http://apt.metasploit.com buster main >> /etc/apt/sources.list
apt update
apt install -y metasploit-framework

```
