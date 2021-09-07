#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dns rebinding builder."""

BASE = "rbndr.us"
"""
Generously hosted domain see
see: https://lock.cmpxchg8b.com/rebinder.html
"""


def get_fqdn(normalip: str, rebindip: str):
    """Get FQDN for rbndr.us."""
    arr1 = normalip.split(".")
    arr2 = rebindip.split(".")
    v1 = "".join(f"{int(i):02x}" for i in arr1)
    v2 = "".join(f"{int(i):02x}" for i in arr2)
    fqdn = f"{v1}.{v2}.{BASE}"
    return fqdn
