#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/cmd-not-found.py."""
import unittest
from v0tools.tests import CliTest


class Test_cmd_not_found(CliTest):
    SCRIPT_NAME = "cmd-not-found.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_valid(self):
        self.match_txt_in_output("socat", "apt-get install socat")

    def test_bad(self):
        self.match_txt_in_output("booga", "{}")


if __name__ == "__main__":
    unittest.main()
    # Done
