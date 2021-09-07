#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Documentation Generator Classes."""
from pathlib import Path
from v0tools import Config
from inspect import cleandoc
import sys

_ME = Path(__file__)
BASE = _ME.resolve().parent.parent.parent
ROOT_DIR = BASE.joinpath("docs")
CONTENT_DIR = ROOT_DIR.joinpath("content")
API_DIR = CONTENT_DIR.joinpath("api")
BINDIR = BASE.joinpath("bin")
MEDIA_DIR = ROOT_DIR.joinpath("static", "cli")
TEMPLATE_DIR = BASE.joinpath("templates")


# DOC_MAIN = CONTENT_DIR.joinpath("_index.md")

SETUP_CFG = BASE.joinpath("setup.cfg")
VERSION_FILE = BASE.joinpath("VERSION")
GITHUB_README = BASE.joinpath("README.md")
SITE_MAIN = CONTENT_DIR.joinpath("_index.md")


if not MEDIA_DIR.exists():
    MEDIA_DIR.mkdir()

GITHUB_URL = "https://github.com/shollingsworth/v0tools"
SITE_BASE = "https://v0tools.stev0.me"

sys.path.append(str(BINDIR.absolute()))


def iterfiles(path: Path):
    """Iterate over all files in directory."""
    for i in path.iterdir():
        if i.is_dir():
            yield from iterfiles(i)
        else:
            yield i


class EnvGroup:
    def __init__(self):
        self.vals = []
        for i in sorted(dir(Config)):
            if not i.startswith("V0_"):
                continue
            func = getattr(Config, i)
            self.vals.append({"name": i, "doc": cleandoc(func.__doc__)})
