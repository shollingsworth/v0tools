#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/dnsrebind.py."""
from v0tools import exceptions
import unittest
from v0tools.tests import CliTest


class Test_dnsrebind(CliTest):

    SCRIPT_NAME = "dnsrebind.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_above_max_test_count(self):
        inp_args = "--test_count 1000 8.8.8.8 127.0.0.1"
        self.exception_raises(inp_args, exceptions.InvalidCliArgument)

    def test_min_count(self):
        inp_args = "--test_count 25 8.8.8.8 127.0.0.1"
        self.exception_raises(inp_args, exceptions.InvalidCliArgument)

    def test_run(self):
        inp_args = "--test_count 200 8.8.8.8 127.0.0.1"
        print(self.run_cli(inp_args))


if __name__ == "__main__":
    unittest.main()
    # done
