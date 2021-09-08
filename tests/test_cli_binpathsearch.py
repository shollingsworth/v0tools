#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/binpathsearch.py."""
import unittest
from v0tools.tests import CliTest

# from v0tools import exceptions


class Test_binpathsearch(CliTest):
    SCRIPT_NAME = "binpathsearch.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_grep_in_path(self):
        args = "-f grep"
        match_lines = [
            "zgrep",
            "grep",
            "fgrep",
        ]
        self.match_lines_in_output(args, match_lines)


if __name__ == "__main__":
    unittest.main()
