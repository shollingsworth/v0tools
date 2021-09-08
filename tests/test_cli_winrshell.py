#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/winrshell.py."""
import unittest
from v0tools.tests import CliTest


class Test_winrshell(CliTest):
    SCRIPT_NAME = "winrshell.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    # TODO finish tests for rshells


if __name__ == "__main__":
    unittest.main()
