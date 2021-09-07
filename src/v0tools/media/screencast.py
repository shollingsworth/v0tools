#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module for doing screencast / media work."""
import subprocess
from v0tools import syspkgs


def screenkey(scr_num: int) -> subprocess.Popen:
    """Launch the screenkey program for showing keys during terminal work."""
    syspkgs.check_installs(["screenkey"])
    cmd = list(map(str, ["screenkey", "--scr", scr_num]))
    print(" ".join(cmd))
    return subprocess.Popen(cmd)


def x11_to_mp4(
    x: int,
    y: int,
    width: int,
    height: int,
    destination_file: str,
) -> subprocess.Popen:
    """FFMPEG recording x11 to MP4 file (no audio)."""
    syspkgs.check_installs(["ffmpeg"])
    cmd = list(
        map(
            str,
            [
                "ffmpeg",
                "-y",
                "-video_size",
                f"{width}x{height}",
                "-framerate",
                25,
                "-f",
                "x11grab",
                f"-i",
                f":0.0+{x},{y}",
                destination_file,
            ],
        )
    )
    print(" ".join(cmd))
    return subprocess.Popen(cmd)
