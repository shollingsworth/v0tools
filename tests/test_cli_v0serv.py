#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/v0serv.py."""
from typing import List
from v0tools.cli import Cli
import unittest
from io import StringIO
import sys
import contextlib
import pathlib
import threading
import tempfile
from pathlib import Path
from v0tools.lib import util
import requests
import time

BASE = pathlib.Path(__file__).parent.parent.resolve()

sys.path.append(str(BASE.joinpath("bin")))
name = "v0serv"
cli_mod = __import__(name)
cli = cli_mod.cli  # type: Cli


def _bgserv(args):
    cli.run_nocatch(args)


class Test_v0serv(unittest.TestCase):
    def test_help(self):
        inp_args = "--help"
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn("--help", output)

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
            pass_args = cli.get_parse(f"-p {port} -i lo {tdir}")
            t = threading.Thread(target=_bgserv, args=(pass_args,))
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
            pass_args = cli.get_parse(f"-p {port} -i lo {rfile}")
            t = threading.Thread(target=_bgserv, args=(pass_args,))
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
