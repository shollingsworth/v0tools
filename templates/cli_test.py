#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli ::relpath::."""
from v0tools.cli import Cli
from v0tools import exceptions
import unittest
from io import StringIO
import sys
import contextlib
import pathlib

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "::modname::"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


class Test___flat__(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

    def test_err_system_exit(self):
        assert True == False


if __name__ == "__main__":
    unittest.main()
