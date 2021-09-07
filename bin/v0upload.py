#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP server that accepts PUT requests from remotes."""
from v0tools import cli
from v0tools.servers import httpserv

cli = cli.Cli()
cli.add_path()
cli.add_ipv_interface()
cli.add_port()

parser = cli.parser


def main(args):
    """Run main function."""
    httpserv.uploader(
        args.address,
        str(args.port),
        args.path,
    )


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    main(args)
