#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli ::relpath::."""
import unittest
from v0tools.tests import CliTest

# from v0tools import exceptions


class Test___flat__(CliTest):
    SCRIPT_NAME = "::modname::.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_CHANGEME(self):
        assert True == False


if __name__ == "__main__":
    unittest.main()
