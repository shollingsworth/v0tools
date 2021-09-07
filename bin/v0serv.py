#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP Serve a directory, or serve a single isolated file."""
from v0tools import cli
from v0tools.servers import httpserv

cli = cli.Cli(__doc__)
cli.add_path()
cli.add_ipv_interface()
cli.add_port()
parser = cli.parser

parser.add_argument(
    "-d",
    "--display",
    help="display type",
    choices=httpserv.SERV_PREFIXES.keys(),
    default="none",
    type=str,
)


def main(args):
    """Run main function."""
    httpserv.serve(
        args.address,
        str(args.port),
        args.path,
        args.display,
    )


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse("-i lo ./")
    cli.run(args)
