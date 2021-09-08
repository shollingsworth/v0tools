#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UNIT Test for Cli bin/v0upload.py."""
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
from v0tools.tests import CliTest


class Test_v0serv(CliTest):
    SCRIPT_NAME = "v0upload.py"

    def setUp(self):
        self.init()

    def _bgserv(self, args):
        self.cli.run_nocatch(args)

    def test_help(self):
        self.match_zero_exit_code("--help", "--help")

    def test_serv_dir(self):
        r_files = {f"file_{idx}.txt": util.randstr(20) for idx in range(50)}
        vfiles = []  # type: List[Path]
        port = util.randport()
        with tempfile.TemporaryDirectory() as tdir:
            tdir = Path(tdir)
            upload_dir = tdir.joinpath("upload_path")
            upload_dir.mkdir()
            # Write rando files
            for fn, content in r_files.items():
                fobj = tdir.joinpath(fn)
                vfiles.append(fobj)
                fobj.write_text(content)
            # start upload server
            pass_args = self.cli.get_parse(f"-p {port} -i lo {upload_dir}")
            t = threading.Thread(target=self._bgserv, args=(pass_args,))
            t.daemon = True
            t.start()
            time.sleep(3)

            # Let's goooooo
            for i in vfiles:
                url = f"http://127.0.0.1:{port}/{i.name}"
                with i.open("rb") as fileh:
                    requests.put(url, data=fileh)
            for i in vfiles:
                expected = i.read_text()
                npath = upload_dir.joinpath(i.name)
                upl_content = npath.read_text()
                self.assertEqual(expected, upl_content)
            time.sleep(3)


if __name__ == "__main__":
    unittest.main()
    # done
