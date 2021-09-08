#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/cmdrec.py."""
import unittest
from v0tools import exceptions
from v0tools.tests import CliTest
import tempfile


class Test_cmdrec(CliTest):
    SCRIPT_NAME = "cmdrec.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_bad_file_ext(self):
        inp_args = "test.txt"
        self.exception_raises(inp_args, exceptions.InvalidFileExtention)

    def test_no_file_ext(self):
        inp_args = "test"
        self.exception_raises(inp_args, exceptions.InvalidFileExtention)

    def test_file_exists(self):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as file:
            inp_args = file.name
            self.exception_raises(inp_args, exceptions.FileExists)

    def test_invalid_geometry(self):
        inp_args = "--shell_geometry 3,3,3 test.mp4"
        self.exception_raises(inp_args, exceptions.InvalidCliArgument)

    def test_invalid_shift(self):
        inp_args = "--recording_geometry 3,3,3 test.mp4"
        self.exception_raises(inp_args, exceptions.InvalidCliArgument)


if __name__ == "__main__":
    unittest.main()
    # done
