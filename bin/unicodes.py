#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""print unicode values and associated information to stdout."""
from v0tools import chars, cli
import os

dstring = f"""
{__doc__}

example:
    {os.path.basename(__file__)} | fzf
"""

cli = cli.Cli(dstring)
cli.add_filter()
parser = cli.parser


def main(args):
    """Run main function."""
    for _, i in enumerate(chars.unicodes()):
        _int, _hex, _chr, name, uval, htmlent = i.values()
        line = f"{_chr} {name} int:{_int} hex:{_hex.zfill(2)} {uval} {htmlent}"
        if not args.filter:
            print(line, flush=True)
            continue
        if all([i in line for i in args.filter]):
            print(line, flush=True)


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    cli.run(args)
