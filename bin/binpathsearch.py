#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search for executable names in PATH

Helpful for finding the names of commands you can't remember
"""
import os
from pathlib import Path
from v0tools.cli import Cli

cli = Cli()
parser = cli.parser
cli.add_filter()


def vals():
    paths = os.environ["PATH"].split(":")
    dirs = [Path(p) for p in paths]
    vals = set()
    for path in dirs:
        for file in path.iterdir():
            if file.is_dir():
                continue
            _apath = file.resolve()
            is_exec = os.access(str(_apath), os.X_OK)
            if not is_exec:
                continue
            if _apath.name not in vals:
                yield _apath.name
            vals.add(_apath.name)


def main(args):
    """Run main function."""
    for i in sorted(vals()):
        if args.filter:
            if all([z in i for z in args.filter]):
                print(i)
        else:
            print(i)


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse(["-f", "crack"])
    cli.run(args)
