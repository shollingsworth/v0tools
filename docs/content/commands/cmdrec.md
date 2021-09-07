---
description: Terminal Recorder using ffmpeg and KDE Console.
geekdocAlign: left
geekdocDescription: Terminal Recorder using ffmpeg and KDE Console.
title: cmdrec.py
weight: 99

---

> **Terminal Recorder using ffmpeg and KDE Console.**

{{< tabs "80fa25b938f012e59809cb757f226fe1" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/cmdrec.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: cmdrec.py [-h] [--overwrite] [--shell_geometry SHELL_GEOMETRY] [--recording_geometry RECORDING_GEOMETRY] [--scr SCR]
                 [--noterm] [--terminal {konsole}]
                 dest_file

Terminal Recorder using ffmpeg and KDE Console.

positional arguments:
  dest_file             destination file, supported types mp4,gif,webm

optional arguments:
  -h, --help            show this help message and exit
  --overwrite, -y       Overwrite destination file
  --shell_geometry SHELL_GEOMETRY, -g SHELL_GEOMETRY
                        geometry in the following format x,y,pixel-width,pixel-height
  --recording_geometry RECORDING_GEOMETRY, -r RECORDING_GEOMETRY
                        geometry in the following format for recording area x,y,pixel-width,pixel-height
  --scr SCR, -k SCR     Screen Keys Screen
  --noterm, -n          Do not spawn a new terminal
  --terminal {konsole}, -t {konsole}
                        terminal command
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Terminal Recorder using ffmpeg and KDE Console."""
from v0tools.media import convert, screencast
from v0tools import cli, exceptions
import subprocess
import time
import signal
import os
import tempfile
import shutil
import pathlib


TERM_COMMANDS = {
    # "xterm": "xterm -class UXTerm -title uxterm -u8 -fa Mono -fs 18 -bg black -fg white -geometry __GEO__",
    "konsole": "konsole --nofork --geometry __GEO__",
}


def _mp4(srcfile, destfile):
    """This is the default action, just move the file."""
    shutil.move(srcfile, destfile)


def _gif(srcfile, destfile):
    """Convert to GIF."""
    out = convert.mp4_to_gif(srcfile, destfile, True)
    print(out)
    os.unlink(srcfile)


def _webm(srcfile, destfile):
    out = convert.mp4_to_webm(srcfile, destfile, True)
    print(out)
    os.unlink(srcfile)


FT_MAP = {
    "mp4": _mp4,
    "gif": _gif,
    "webm": _webm,
}

cli = cli.Cli()

parser = cli.parser

parser.add_argument(
    "dest_file",
    help=f'destination file, supported types {",".join(FT_MAP)}',
    type=str,
)

parser.add_argument(
    "--overwrite",
    "-y",
    help="Overwrite destination file",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--shell_geometry",
    "-g",
    help="geometry in the following format x,y,pixel-width,pixel-height",
    type=str,
    default="0,0,1920,1080",
)

parser.add_argument(
    "--recording_geometry",
    "-r",
    help="geometry in the following format for recording area x,y,pixel-width,pixel-height",
    type=str,
    default="0,0,1920,1080",
)

parser.add_argument(
    "--scr",
    "-k",
    help="Screen Keys Screen",
    type=int,
    default=0,
)

parser.add_argument(
    "--noterm",
    "-n",
    help="Do not spawn a new terminal",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--terminal",
    "-t",
    help="terminal command",
    type=str,
    choices=TERM_COMMANDS.keys(),
    default="konsole",
)


def _ffmpeg(args, tfile):
    win = WinProps(args)
    return screencast.x11_to_mp4(
        win.rx,
        win.ry,
        win.rwidth,
        win.rheight,
        tfile,
    )


class WinProps(object):
    """Window Properties."""

    def __init__(self, args):
        sarr = args.shell_geometry.split(",")
        rarr = args.recording_geometry.split(",")
        if len(sarr) != 4:
            parser.print_help()
            raise exceptions.InvalidCliArgument("--shell_geometry")
        if len(rarr) != 4:
            parser.print_help()
            raise exceptions.InvalidCliArgument("--recording_geometry")

        self.sx, self.sy, self.swidth, self.sheight = map(int, sarr)
        self.rx, self.ry, self.rwidth, self.rheight = map(int, rarr)


def shell(args):
    xo = WinProps(args)
    geo = f"{xo.swidth}x{xo.sheight}+{xo.sx}+{xo.sy}"
    cmd = [
        "konsole",
        "--nofork",
        "--geometry",
        geo,
    ]
    return subprocess.Popen(cmd)


def main(args):
    """Run main function."""
    ext = args.dest_file.rsplit(".", 1)
    if len(ext) == 1:
        raise exceptions.InvalidFileExtention(args.dest_file, list(FT_MAP))
    if ext[1] not in FT_MAP:
        raise exceptions.InvalidFileExtention(args.dest_file, list(FT_MAP))
    if os.path.exists(args.dest_file) and not args.overwrite:
        raise exceptions.FileExists(args.dest_file, "--overwrite not set")
    args.func = FT_MAP[ext[1]]
    pdir = pathlib.Path(args.dest_file).resolve().parent
    if not pdir.exists():
        raise exceptions.DirectoryNotExist(str(pdir))

    if not args.noterm:
        shell_proc = shell(args)
        time.sleep(1)

    tfile = tempfile.mktemp(suffix=".mp4")

    rec_proc = _ffmpeg(args, tfile)
    keys_proc = screencast.screenkey(args.scr)

    if not args.noterm:
        shell_proc.communicate()
        rec_proc.send_signal(signal.SIGTERM)
        keys_proc.send_signal(signal.SIGTERM)
        time.sleep(1)
    else:
        try:
            rec_proc.communicate()
        except KeyboardInterrupt:
            pass
        keys_proc.send_signal(signal.SIGTERM)
        time.sleep(1)

    args.func(tfile, args.dest_file)


# This needs to be set here
cli.set_entrypoint(main)
cli.set_required_binaries(["konsole", "ffmpeg", "screenkey"])

if __name__ == "__main__":
    args = cli.get_parse()
    cli.run(args)
    # args = cli.get_parse("--help")
    # args = cli.get_parse("foo.txt")

```

{{< /tab >}}
{{< /tabs >}}
