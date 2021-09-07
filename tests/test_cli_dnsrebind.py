#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/dnsrebind.py."""
from v0tools.cli import Cli
from v0tools import exceptions
import unittest
from io import StringIO
import sys
import contextlib
import pathlib

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "dnsrebind"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


class Test_dnsrebind(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

    def test_above_max_test_count(self):
        inp_args = "--test_count 1000 8.8.8.8 127.0.0.1"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            self.assertRaises(exceptions.InvalidCliArgument, cli.run_nocatch, args)

    def test_min_count(self):
        inp_args = "--test_count 25 8.8.8.8 127.0.0.1"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            self.assertRaises(exceptions.InvalidCliArgument, cli.run_nocatch, args)

    def test_run(self):
        inp_args = "--test_count 200 8.8.8.8 127.0.0.1"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            cli.run_nocatch(args)
            output = buf.getvalue()
        print(output)


if __name__ == "__main__":
    unittest.main()
    # done
