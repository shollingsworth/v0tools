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
parser = cli.parser

parser.add_argument(
    "-f",
    "--filter",
    nargs="*",
    help="Filter string",
    action="append",
    type=str,
    required=False,
    default=None,
)


def main(args):
    """Run main function."""
    if args.filter:
        fvalues = [i[0] for i in args.filter]
    else:
        fvalues = []
    for _, i in enumerate(chars.unicodes()):
        _int, _hex, _chr, name, uval, htmlent = i.values()
        line = f"{_chr} {name} int:{_int} hex:{_hex.zfill(2)} {uval} {htmlent}"
        if not fvalues:
            print(line, flush=True)
            continue
        if all([i in line for i in fvalues]):
            print(line, flush=True)


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse(["-f", "cat", "-f", "grin"])
    cli.run(args)
    # args = cli.get_parse("--help")
