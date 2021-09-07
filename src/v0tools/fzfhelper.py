#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FZF helpers that are routinely called."""
from typing import Tuple
from v0tools import net
from pyfzf.pyfzf import FzfPrompt


def network_interfaces() -> Tuple[str, str, str]:
    """Returns ipversion, interface, address tuple."""
    fzf = FzfPrompt()
    net_opts = sorted(
        [
            f"{ipv}::{interface}::{address}"
            for ipv, interface, address in net.get_interfaces()
        ]
    )
    val = fzf.prompt(net_opts)
    return val[0].split("::")
