#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/linrshell.py."""
from v0tools.cli import Cli
from v0tools import exceptions
import unittest
from io import StringIO
import sys
import contextlib
import pathlib

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "linrshell"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


class Test_linrshell(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

    # TODO figure out unit tests for rshell stuff


if __name__ == "__main__":
    unittest.main()
    # done
