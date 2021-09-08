#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/ip_urls.py."""
from v0tools import exceptions
import unittest
import random
from v0tools.net import get_ip
from v0tools.web import requests
from v0tools.tests import CliTest


class Test_ip_urls(CliTest):

    SCRIPT_NAME = "ip_urls.py"

    def setUp(self):
        self.init()

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_invalid_ip(self):
        inp_args = "10.10.10"
        self.exception_raises(inp_args, exceptions.InvalidIp)

    def test_valid(self):
        inp_args = get_ip("www.google.com")
        output = self.run_cli(inp_args)
        rurl = random.choice(output.split("\n"))
        url = rurl.split()[1]
        req = requests.get(url)
        self.assertEqual(req.status_code, 200)


if __name__ == "__main__":
    unittest.main()
    # done
