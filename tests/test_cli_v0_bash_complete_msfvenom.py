#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/v0complete_msfvenom.py."""
from v0tools.cli import Cli
from v0tools import tests
import unittest
from io import StringIO
import sys
import contextlib
import pathlib
import tempfile

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "v0_bash_complete_msfvenom"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


class Test_v0complete_msfvenom_Completions(tests.BashCompletionTest):
    def setUp(self):
        self.program = "msfvenom"

    def run_test(self, partial, expected):
        with tempfile.NamedTemporaryFile() as fileh:
            with StringIO() as buf, contextlib.redirect_stdout(buf):
                args = cli.get_parse()
                cli.run_nocatch(args)
                output = buf.getvalue()
                print(output)
            fileh.write(output.encode())
            fileh.flush()
            self.run_complete(fileh.name, self.program, partial, expected)

    def test_payload(self):
        partial = "-p linux/x64/meterpreter/reve"
        expected = "linux/x64/meterpreter/reverse_tcp"
        self.run_test(partial, expected)

    def test_format(self):
        partial = "-f exe-ser"
        expected = "exe-service"
        self.run_test(partial, expected)

    def test_encoder(self):
        partial = "-e x64/xor_d"
        expected = "x64/xor_dynamic"
        self.run_test(partial, expected)

    def test_HOST(self):
        partial = "LHOST=127"
        expected = "127.0.0.1"
        self.run_test(partial, expected)


class Test_v0complete_msfvenom(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)


if __name__ == "__main__":
    unittest.main()
