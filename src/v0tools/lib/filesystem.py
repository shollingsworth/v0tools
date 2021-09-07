#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Filesystem utils."""
import fnmatch
import os


def iterfiles(path: str, filename_filter: str):
    """Recursivly iterate through files filtering by filetype

    i.e. ::
        for i in iterfiles('/home/foo', '*.py'):
            print(i)
    """
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, filename_filter):
            filename = os.path.join(root, filename)
            yield filename
