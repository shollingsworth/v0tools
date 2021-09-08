#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/php_search_vuln.py."""
from v0tools import exceptions
import unittest
import pathlib
import tempfile
import os
import pathlib
from v0tools.tests import CliTest


class Test_php_search_vuln(CliTest):
    SCRIPT_NAME = "php_search_vuln.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_run(self):
        should_see = [
            "lvl1.php : 24",
            "lvl2.php : 31",
            "lvl3.php : 33",
            "lvl4.php : 34",
            "XSS_level3.php : 20",
            "XSS_level4.php : 22",
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)
            dest = tmpdir.joinpath("repo")
            os.system(
                f"git clone https://github.com/OWASP/Vulnerable-Web-Application.git {dest}"
            )
            if not dest.is_dir():
                raise RuntimeError("git clone didn't work")
            inp_args = str(dest)
            output = self.run_cli(inp_args)
        for i in should_see:
            self.assertIn(i, output)

    def test_no_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)
            no_files = tmpdir.joinpath("nofiles")
            no_files.mkdir()
            no_files.joinpath("test.txt").write_text("Testing")

            inp_args = str(no_files)
            self.exception_raises_with_regex(
                inp_args,
                exceptions.NoAction,
                r".*No files.*",
            )

    def test_no_results(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)
            no_d = tmpdir.joinpath("nores")
            no_d.mkdir()
            no_d.joinpath("test.php").write_text("Testing")

            inp_args = str(no_d)
            self.exception_raises_with_regex(
                inp_args,
                exceptions.NoAction,
                r".*Could not find.*",
            )


if __name__ == "__main__":
    unittest.main()
    # done
