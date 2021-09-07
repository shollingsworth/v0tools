#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/cmdrec.py."""
import unittest
from io import StringIO
from v0tools import exceptions
from v0tools.cli import Cli
import sys
import contextlib
import pathlib
import tempfile

BASE = pathlib.Path(__file__).parent.parent.resolve()
INSPATH = BASE.joinpath("bin").resolve()
sys.path.append(str(INSPATH))
cli_mod = __import__("cmdrec")
cli = cli_mod.cli  # type: Cli


class Test_cmdrec(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

    def test_bad_file_ext(self):
        inp_args = "test.txt"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            self.assertRaises(exceptions.InvalidFileExtention, cli.run_nocatch, args)

    def test_no_file_ext(self):
        inp_args = "test"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            self.assertRaises(exceptions.InvalidFileExtention, cli.run_nocatch, args)

    def test_file_exists(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as file:
            inp_args = file.name
            with StringIO() as buf, contextlib.redirect_stdout(buf):
                args = cli.get_parse(inp_args)
                self.assertRaises(exceptions.FileExists, cli.run_nocatch, args)

    def test_invalid_geometry(self):
        inp_args = "--shell_geometry 3,3,3 test.mp4"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            self.assertRaises(exceptions.InvalidCliArgument, cli.run_nocatch, args)

    def test_invalid_shift(self):
        inp_args = "--recording_geometry 3,3,3 test.mp4"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            self.assertRaises(exceptions.InvalidCliArgument, cli.run_nocatch, args)


if __name__ == "__main__":
    unittest.main()
    # done
