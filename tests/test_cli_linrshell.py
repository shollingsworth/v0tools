#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/linrshell.py."""
import unittest
from v0tools.tests import CliTest


class Test_linrshell(CliTest):
    SCRIPT_NAME = "linrshell.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    # TODO figure out unit tests for rshell stuff


if __name__ == "__main__":
    unittest.main()
    # done
