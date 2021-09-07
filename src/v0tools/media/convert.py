#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert media formats."""
import subprocess
from v0tools import syspkgs


def mp4_to_gif(srcfile, destfile, overwrite=False):
    """Convert MP4 to GIF."""
    syspkgs.check_installs(["ffmpeg"])
    cmd = [
        "ffmpeg",
        "-i",
        srcfile,
        "-filter_complex",
        "[0:v] fps=24,scale=1000:-1,split [a][b];[a] palettegen [p];[b][p] paletteuse",
        destfile,
    ]
    if overwrite:
        cmd.insert(1, "-y")
    print(" ".join(cmd))
    return subprocess.check_output(cmd, encoding="utf-8")


def mp4_to_webm(srcfile, destfile, overwrite=False):
    """Convert an MP4 file to WEBM file."""
    syspkgs.check_installs(["ffmpeg"])
    cmd = [
        "ffmpeg",
        "-i",
        srcfile,
        "-c:v",
        "libvpx",
        "-crf",
        "10",
        "-b:v",
        "1M",
        "-c:a",
        "libvorbis",
        destfile,
    ]
    if overwrite:
        cmd.insert(1, "-y")
    print(" ".join(cmd))
    return subprocess.check_output(cmd, encoding="utf-8")
