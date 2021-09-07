#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""System Packing Information."""
from typing import List, Dict
from v0tools import exceptions
import pathlib
import shutil


COMMANDS = {}  # type: Dict[str, Pkg]
"""Command map."""


def check_installs(bins: List):
    """
    Check if binaries exist

    Show instructions if they do not exist and exit
    """
    pkgs = [COMMANDS[i] for i in bins]
    missing = [i for i in pkgs if not i.path]
    if missing:
        raise exceptions.MultiBinaryNotFound(missing)


class Pkg(object):
    """Package Object."""

    DIST_DEB = "debian"
    """Distro fixed string."""

    DIST_RH = "fedora"
    """Distro fixed string."""

    DIST_ARCH = "arch"
    """Distro fixed string."""

    PKG_RH = "sudo yum -y install"
    """Distro package prefix."""

    PKG_ARCH = "sudo pacman -S"
    """Distro package prefix."""

    PKG_DEB = "sudo apt install"
    """Distro package prefix."""

    def __init__(self, name: str, testing=False):
        """Initialize Pkg"""

        self.is_testing = testing
        """Denote if the package is for testing purposes."""

        self.name = name
        """Binary name."""

        self.rh = name
        """rh instructions."""

        self.arch = name
        """Arch instructions."""

        self.deb = name
        """Debian instructions."""

        COMMANDS[self.name] = self
        """Supported dists."""

    def add_binary(self, name):
        """Add binary name to commands."""
        COMMANDS[name] = self
        return self

    @property
    def path(self):
        """Return binary path."""
        return shutil.which(self.name)

    def set_arch(self, value):
        """Set Arch value self.arch."""
        self.arch = value
        return self

    def set_rh(self, value):
        """Set Redhat value self.rh."""
        self.rh = value
        return self

    def set_deb(self, value):
        """Set Debian value self.deb."""
        self.deb = value
        return self

    @property
    def dist_map(self):
        """Distribution value map."""
        return {
            self.DIST_RH: self.rh,
            self.DIST_DEB: self.deb,
            self.DIST_ARCH: self.arch,
        }

    @property
    def pkg_prefix(self):
        """Package prefix map."""
        return {
            self.DIST_RH: self.PKG_RH,
            self.DIST_DEB: self.PKG_DEB,
            self.DIST_ARCH: self.PKG_ARCH,
        }

    def instruction(self, override=None):
        """Install Instruction in shell script."""
        if override is None:
            key = self.dist
        else:
            key = override

        txt = self.map[key]
        if len(txt.splitlines()) > 1:
            return txt
        else:
            pmanager, pkg = self.dists[key]
            return f"{pmanager} {pkg}"

    @property
    def dist(self):
        """Get Linux Distribution Information."""
        fc = pathlib.Path("/etc/os-release").read_text()
        os_info = {
            i.split("=")[0].strip('"'): i.split("=")[1].strip('"')
            for i in fc.splitlines()
            if i.strip()
        }
        retval = os_info.get("ID_LIKE", os_info.get("ID"))
        if not retval:
            raise RuntimeError(f"Unknown Dist type: {os_info}")
        if "fedora" in retval:
            return "fedora"
        return retval


Pkg("fzf").set_rh(
    """
git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install
source ~/.bashrc
""".strip()
)
Pkg("konsole")
Pkg("socat")
Pkg("rlwrap").set_rh(
    """
sudo yum -y group install "Development Tools"
sudo yum -y install readline-devel
git clone https://github.com/hanslub42/rlwrap.git
cd rlwrap
autoreconf --install
./configure
make
sudo make install
""".strip()
)
Pkg("ffmpeg").set_rh(
    """
sudo yum -y install epel-release
sudo yum -y localinstall --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm
sudo yum -y install ffmpeg ffmpeg-devel
""".strip()
)

Pkg("nc").set_deb("ncat").set_rh("nmap-ncat").set_arch("nmap")
Pkg("socat")

Pkg("msfvenom").add_binary("msfconsole").set_arch("metasploit").set_deb(
    """
curl https://apt.metasploit.com/metasploit-framework.gpg.key | apt-key add -
echo deb http://apt.metasploit.com buster main >> /etc/apt/sources.list
apt update
apt install -y metasploit-framework
""".lstrip()
).set_rh(
    """
curl https://apt.metasploit.com/metasploit-framework.gpg.key > /tmp/msf.asc
rpm --import /tmp/msf.asc
sudo yum -y install yum-utils
sudo yum-config-manager --add-repo=https://rpm.metasploit.com/
sudo yum -y install metasploit-framework.x86_64
""".lstrip()
)

Pkg("screenkey")
# For testing purposes
Pkg("nonexist", testing=True)


def get_install_instructions() -> Dict[str, str]:
    """Return install instruction dict."""
    objects = {}  # type: Dict[Pkg, list]
    inst_helper = {}
    instructions = {}

    for k, v in COMMANDS.items():
        objects.setdefault(v, [])
        objects[v].append(k)

    for obj, binaries in objects.items():
        if obj.is_testing:
            continue
        for i in [obj.DIST_ARCH, obj.DIST_DEB, obj.DIST_RH]:
            inst_helper.setdefault(i, {})
            inst_helper[i]["object"] = obj
            inst_helper[i].setdefault("customs", [])
            inst_helper[i].setdefault("pkgs", [])
            inst_helper[i].setdefault("binaries", [])
            for z in binaries:
                inst_helper[i]["binaries"].append(z)
            if len(obj.dist_map[i].split()) > 1:
                inst_helper[i]["customs"].append([obj.name, obj.dist_map[i].strip()])
            else:
                inst_helper[i]["pkgs"].append(obj.dist_map[i])

    for distro, d1 in inst_helper.items():
        pkgs = d1["pkgs"]
        binaries = d1["binaries"]
        obj = d1["object"]  # type: Pkg
        pkg_prefix = obj.pkg_prefix[distro]
        inst = f'{pkg_prefix} {" ".join(pkgs)}'
        assemble = []
        assemble = [
            f'# Provides {", ".join(binaries)}',
            inst,
            "",
        ]
        for name, cust in d1["customs"]:
            assemble.append(f"# Install {name}")
            assemble.append(cust)
            assemble.append("")
        instructions[distro] = "\n".join(assemble)

    return instructions
