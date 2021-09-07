#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Logging Module."""
import logging
import inspect
import os

logging.basicConfig()
LOG = logging.getLogger()
"""Main LOG object."""
LOG.setLevel(logging.INFO)


def get_log():
    """Return logger object."""
    caller = inspect.stack()[1]
    bn = os.path.basename(caller.filename)
    return LOG.getChild(bn)
