#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/cmd-not-found.py."""
from v0tools.cli import Cli
import unittest
from io import StringIO
import sys
import contextlib
import pathlib

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "cmd-not-found"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


class Test_cmd_not_found(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

    def test_valid(self):
        inp_args = "socat"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            cli_mod.main(args)
            output = buf.getvalue()
        self.assertIn("apt-get install socat", output)

    def test_bad(self):
        inp_args = "booga"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            cli_mod.main(args)
            output = buf.getvalue().strip()
        self.assertEqual("{}", output)


if __name__ == "__main__":
    unittest.main()
    # Done
