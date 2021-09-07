#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sourceable Autocomplete for msfvenom flags."""
from v0tools.msf import get_venom_auto_complete
from v0tools.cli import Cli


def main(args):
    """Run main function."""
    print("##### Venom Autocomplete", flush=True)
    print(get_venom_auto_complete(), flush=True)


cli = Cli()
cli.set_entrypoint(main)
cli.set_required_binaries(["msfvenom"])

if __name__ == "__main__":
    args = cli.get_parse()
    cli.run(args)
