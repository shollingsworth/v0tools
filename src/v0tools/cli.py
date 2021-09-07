#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module that helps manage the CLI commands and documentation."""
import typing
import inspect
import argparse
from v0tools import net
from v0tools import fzfhelper
from v0tools.lib import util
from v0tools import exceptions, syspkgs
import shlex
import pathlib


class Cli(object):
    """Cli Class."""

    def __init__(self, description=None):
        """Return Cli Object."""
        caller = inspect.stack()[1]
        if description is None:
            description = caller.frame.f_globals["__doc__"]
        self.description = description
        """Argument description."""

        self.entrypoint = ""  # type: typing.Callable
        """Function entrypoint."""

        self.required_binaries = []
        """Required Binary list."""

        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=str(description),
        )
        """ArgumentParser object."""

    def add_path(self):
        """Directory or file path."""
        self.parser.add_argument(
            "path",
            help=self.add_path.__doc__,
            type=str,
        )

    def add_ipv_interface(self):
        """Add ipv / interface combo."""
        self.parser.add_argument(
            "--interface",
            "-i",
            help="network interface: i.e. tun0, eth0, if undefined, an fzf prompt will appear",
            type=str,
        )
        self.parser.add_argument(
            "--ipv",
            help="IP Version",
            choices=["4", "6"],
            default="4",
            type=str,
        )

    def add_port(self):
        """port number, or default random port in range:1025-65535."""
        self.parser.add_argument(
            "-p",
            "--port",
            help=self.add_path.__doc__,
            type=str,
        )

    def set_entrypoint(self, function: typing.Callable):
        """Set cli entrypoint value."""
        self.entrypoint = function

    def set_required_binaries(self, binlist: typing.List):
        """Set required binary list."""
        self.required_binaries = binlist

    def checks(self):
        """Run checks."""
        syspkgs.check_installs(self.required_binaries)

    def run_nocatch(self, args: argparse.Namespace):
        """Run without catching exceptions.

        Useful in unit tests
        """
        self.checks()
        self.entrypoint(args)

    def run(self, args: argparse.Namespace):
        """Run cli program normally."""
        try:
            self.checks()
            self.entrypoint(args)
        except exceptions.Error as err:
            raise SystemExit(err)
        except KeyboardInterrupt:
            print("Bye!")

    def get_parse(self, test_arr=None):
        """Parge args."""
        if test_arr is not None:
            if isinstance(test_arr, str):
                test_arr = shlex.split(test_arr)
            args = self.parser.parse_args(test_arr)
        else:
            args = self.parser.parse_args()

        action_names = [i.dest for i in self.parser._actions]
        if "path" in action_names and args.path:
            args.path = pathlib.Path(args.path).expanduser().resolve()
        if "interface" in action_names and not args.interface:
            ipv, interface, address = fzfhelper.network_interfaces()
            args.ipv = ipv
            args.address = address
            args.interface = interface
        if "interface" in action_names and args.interface:
            args.address = net.get_interface_address(args.ipv, args.interface)
        if "port" in action_names and not args.port:
            args.port = util.randport()
        return args
