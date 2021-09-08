#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search for executable names in PATH

Helpful for finding the names of commands you can't remember
"""
import os
from pathlib import Path
from v0tools.cli import Cli
from pyfzf.pyfzf import FzfPrompt

cli = Cli()
parser = cli.parser
parser.add_argument(
    "-f",
    "--fzf",
    help="Use fzf to filter results",
    action="store_true",
    default=False,
)


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
    fzf = FzfPrompt()
    if args.fzf:
        val = fzf.prompt(sorted(vals()))
        print(val[0])
    else:
        for i in sorted(vals()):
            print(i)


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    cli.run(args)
