#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/v0serv.py."""
from typing import List
from v0tools.tests import CliTest
import unittest
import threading
import tempfile
from pathlib import Path
from v0tools.lib import util
import requests
import time


class Test_v0serv(CliTest):
    SCRIPT_NAME = "v0serv.py"

    def setUp(self):
        self.init()

    def _bgserv(self, args):
        self.cli.run_nocatch(args)

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_serv_dir(self):
        r_files = {f"file/{idx}/file_{idx}.txt": util.randstr(20) for idx in range(50)}
        vfiles = []  # type: List[Path]
        port = util.randport()
        with tempfile.TemporaryDirectory() as tdir:
            tdir = Path(tdir)
            tdir.joinpath("file").mkdir()
            for fn, content in r_files.items():
                fobj = tdir.joinpath(fn)
                fobj.parent.mkdir()
                vfiles.append(fobj)
                fobj.write_text(content)
            pass_args = self.cli.get_parse(f"-p {port} -i lo {tdir}")
            t = threading.Thread(target=self._bgserv, args=(pass_args,))
            t.daemon = True
            t.start()
            time.sleep(3)
            # Let's goooooo
            for i in vfiles:
                expected_content = i.read_text()
                relpath = str(i).replace(str(tdir), "")
                url = f"http://127.0.0.1:{port}{relpath}"
                content = requests.get(url).text
                self.assertEqual(expected_content, content)
            time.sleep(3)

    def test_serv_single(self):
        port = util.randport()
        rtxt = util.randstr(100)
        fn = "randofile.txt"
        with tempfile.TemporaryDirectory() as tdir:
            tdir = Path(tdir)
            rfile = tdir.joinpath(fn)
            rfile.write_text(rtxt)
            pass_args = self.cli.get_parse(f"-p {port} -i lo {rfile}")
            t = threading.Thread(target=self._bgserv, args=(pass_args,))
            t.daemon = True
            t.start()
            time.sleep(3)
            expected_content = rtxt
            relpath = str(rfile).replace(str(tdir), "")
            url = f"http://127.0.0.1:{port}{relpath}"
            content = requests.get(url).text
            self.assertEqual(expected_content, content)
            time.sleep(3)


if __name__ == "__main__":
    unittest.main()
    # done
