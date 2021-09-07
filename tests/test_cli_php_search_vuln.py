#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/php_search_vuln.py."""
from v0tools.cli import Cli
from v0tools import exceptions
import unittest
from io import StringIO
import sys
import contextlib
import pathlib
import tempfile
import os
import pathlib

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "php_search_vuln"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


class Test_php_search_vuln(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

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
            with StringIO() as buf, contextlib.redirect_stdout(buf):
                args = cli.get_parse(inp_args)
                cli.run_nocatch(args)
                output = buf.getvalue()
        for i in should_see:
            self.assertIn(i, output)

    def test_no_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)
            no_files = tmpdir.joinpath("nofiles")
            no_files.mkdir()
            no_files.joinpath("test.txt").write_text("Testing")

            inp_args = str(no_files)
            args = cli.get_parse(inp_args)
            with StringIO() as buf, contextlib.redirect_stdout(buf):
                self.assertRaisesRegex(
                    exceptions.NoAction, r".*No files.*", cli.run_nocatch, args
                )

    def test_no_results(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)
            no_d = tmpdir.joinpath("nores")
            no_d.mkdir()
            no_d.joinpath("test.php").write_text("Testing")

            inp_args = str(no_d)
            args = cli.get_parse(inp_args)
            with StringIO() as buf, contextlib.redirect_stdout(buf):
                self.assertRaisesRegex(
                    exceptions.NoAction, r".*Could not find.*", cli.run_nocatch, args
                )


if __name__ == "__main__":
    unittest.main()
    # done
