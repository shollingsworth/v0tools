#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/unicodes.py."""
import unittest
from v0tools.tests import CliTest


class Test_unidoes(CliTest):
    SCRIPT_NAME = "unicodes.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_cat_output(self):
        inp_args = ""
        output = self.run_cli(inp_args)
        output = [i for i in output.split("\n") if " cat " in i]
        self.assertEqual(len(output), 14)


if __name__ == "__main__":
    unittest.main()
    # done
