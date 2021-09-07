#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
from glob import glob
from itertools import chain

SCRIPTS = [
    i
    for i in chain(
        glob("bin/*.py"),
        glob("bin/*.sh"),
    )
]

setup(
    name="v0tools",
    install_requires=[
        "beautifulsoup4 >= 4.8.2",
        "lxml >= 4.5.0",
        "pyfzf >= 0.2.2",
        "psutil>=5.8.0",
        "argcomplete>=1.12.3",
        "html2text>=2020.1.16",
        "requests>=2.25.1",
    ],
    scripts=SCRIPTS,
)
