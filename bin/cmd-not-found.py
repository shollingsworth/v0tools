#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print how to install packages on different operating systems

Thanks to https://command-not-found.com/ and
Ƚukasz Lach https://twitter.com/lach_dev for hosting the site

"""
from bs4 import BeautifulSoup
import requests
import json
from v0tools.cli import Cli

cli = Cli()
parser = cli.parser
parser.add_argument(
    "command",
    help="command help",
    type=str,
)


def main(args):
    """Run main function."""
    # txt = pathlib.Path("./test.html").read_text()
    txt = requests.get(f"https://command-not-found.com/{args.command}")
    val = BeautifulSoup(txt.content, "lxml")
    vals = {}
    for i in val.findAll("div"):
        if "command-install" not in i.attrs["class"]:
            continue
        os = i.attrs.get("data-os")
        if not os:
            continue
        code = i.find("code").getText()
        vals[os] = code
    print(json.dumps(vals, indent=4, separators=(",", " : ")))


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse("booga")
    cli.run(args)
