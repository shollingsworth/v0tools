#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helper script for unit testing."""
import pathlib
from types import ModuleType
import sys
import os
import argparse

BASE = pathlib.Path(__file__).parent.parent.resolve()
BINDIR = BASE.joinpath("bin")
TESTDIR = BASE.joinpath("tests")
SRCDIR = BASE.joinpath("src/v0tools")
TEMPLATE_DIR = BASE.joinpath("templates")
sys.path.append(str(BINDIR.absolute()))


class ModInfo(object):
    def __init__(self, script: pathlib.Path):
        self.script = script
        self.name = script.name
        self.module = ModuleType(script.name)  # type: ModuleType
        self._setvals()

    def _setvals(self):
        script = self.script
        if script.name.endswith(".py"):
            mod_name = script.name.replace(".py", "")
            self.module = __import__(mod_name)

    @property
    def is_executable(self):
        return not any(
            [
                self.script.is_dir(),
                not os.access(self.script, os.X_OK),
            ]
        )


def get_cli_template(path: pathlib.Path):
    relpath = path.relative_to(BASE)
    modname = relpath.name.split(".", 1)[0]
    flat = modname.replace("-", "_")
    template = TEMPLATE_DIR.joinpath("cli.py").read_text()
    return (
        template.replace(f"::relpath::", str(relpath))
        .replace("::modname::", modname)
        .replace("__flat__", flat)
    )


def cli_gen():
    """Generate CLI test files if they don't exist."""
    for i in BINDIR.iterdir():
        if not str(i).endswith(".py"):
            continue
        obj = ModInfo(i)
        if not obj.is_executable:
            continue
        dest_file = TESTDIR.joinpath("test_cli_" + i.name)
        if dest_file.exists():
            continue
        content = get_cli_template(i)
        with dest_file.open("w") as fileh:
            print(f"Writing new file: {dest_file}")
            fileh.write(content)
        dest_file.chmod(0o755)


def main():
    """."""
    cli_gen()


if __name__ == "__main__":
    # import unittest
    main()
