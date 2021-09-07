#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Network Related Functions."""
import socket
import psutil
import socket


def get_ip(fqdn: str):
    """Get IP Address of fqdn."""
    return socket.gethostbyname(fqdn)


def get_interfaces():
    """Get All System Interfaces."""
    fmap = {
        socket.AF_INET: "4",
        socket.AF_INET6: "6",
    }
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family not in fmap:
                continue
            yield (fmap[snic.family], interface, snic.address)


def get_interface_address(ipv: str, interface: str) -> str:
    """Return interface, and ipaddress of interface."""
    for _ipv, _int, _addr in get_interfaces():
        if _ipv == ipv and _int == interface:
            return _addr
    raise RuntimeError(f"Could not find {ipv}:{interface}")
