#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate a list of obfuscated ip variations and print to stdout."""
from v0tools.ips import get_urls
from v0tools.lib.log import get_log
from v0tools.cli import Cli, exceptions
import ipaddress

LOG = get_log()
cli = Cli()
cli.parser.add_argument(
    "ip",
    help="ip address",
    type=str,
)


def main(args):
    """Run main function."""
    LOG.info(f"Showing IP Variations for {args.ip}")
    try:
        ok = ipaddress.ip_address(args.ip)
    except ValueError:
        ok = None
    if not ok:
        raise exceptions.InvalidIp(args.ip)
    get_urls(args.ip)


cli.set_entrypoint(main)

if __name__ == "__main__":
    # args = cli.get_parse("--help")
    # args = cli.get_parse("172.217.5.110")
    # args = cli.get_parse("172.217.5")
    args = cli.get_parse()
    cli.run(args)
