#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/v0complete_msfvenom.py."""
from v0tools.tests import CliTest, CliRun, BashCompletionTest
import unittest
from io import StringIO
import contextlib
import tempfile


class Test_v0complete_msfvenom(CliTest):
    SCRIPT_NAME = "v0_bash_complete_msfvenom.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")


class Test_v0complete_msfvenom_Completions(BashCompletionTest):
    def setUp(self):
        self.program = "msfvenom"
        self.clirun = CliRun("v0_bash_complete_msfvenom.py")

    def run_test(self, partial, expected):
        with tempfile.NamedTemporaryFile() as fileh:
            with StringIO() as buf, contextlib.redirect_stdout(buf):
                args = self.clirun.cli.get_parse()
                self.clirun.cli.run_nocatch(args)
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


if __name__ == "__main__":
    unittest.main()
