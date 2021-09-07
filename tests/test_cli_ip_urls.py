#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/ip_urls.py."""
from v0tools.cli import Cli
from v0tools import exceptions
import unittest
from io import StringIO
import sys
import contextlib
import pathlib
import random
from v0tools.net import get_ip
from v0tools.web import requests

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "ip_urls"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


class Test_ip_urls(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

    def test_invalid_ip(self):
        inp_args = "10.10.10"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            self.assertRaises(exceptions.InvalidIp, cli.run_nocatch, args)

    def test_valid(self):
        inp_args = get_ip("www.google.com")
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = cli.get_parse(inp_args)
            cli.run_nocatch(args)
            output = buf.getvalue()
        rurl = random.choice(output.split("\n"))
        url = rurl.split()[1]
        req = requests.get(url)
        self.assertEqual(req.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    # done
