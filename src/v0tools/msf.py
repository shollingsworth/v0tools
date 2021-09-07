#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metaspoit Framework Related methods."""
from typing import Dict, List
from v0tools import Config
from datetime import datetime
import json
import subprocess
import pathlib
import os
import sys
from v0tools.net import get_interfaces
from v0tools import ansi

MAX_CACHE_AGE = 86400  # 1 day
"""Maximum age from now in seconds when the file was last modified."""


class VenomCache(object):
    """VenomCache Class."""

    def __init__(self):
        """Return VenomCache Object."""
        self.cache_file = Config.V0_VENOM_CACHE()  # type: pathlib.Path
        """Cache file location."""
        self.regen_cache()

    def _getoptions(self, opt_type):
        """Get msf venom options."""
        retval = []
        cmd = [
            "msfvenom",
            "--list",
            opt_type,
        ]
        out = subprocess.check_output(cmd)

        vals = [i.strip().decode("utf-8") for i in out.split(b"\n") if i.strip()]

        ignores = ("==", "Frame", "Name", "--")
        for i in vals:
            val = i.split()[0]
            if val.startswith(ignores):
                continue
            retval.append(val)
        return retval

    @property
    def cache_file_age(self):
        """Get time cache file was last modified."""
        stat = os.stat(self.cache_file)
        return datetime.utcfromtimestamp(stat.st_mtime)

    def regen_cache(self, force=False):
        """See if we need to regnerate cache."""
        if not self.cache_file.exists():
            self._gencache()
        elif force:
            self._gencache()
        elif self.is_stale:
            self._gencache()

    @property
    def is_stale(self):
        """Returns true if cache age is over MAX_CACHE_AGE."""
        now = datetime.utcnow()
        sec_old = (self.cache_file_age - now).total_seconds()
        self._seconds = sec_old
        if abs(sec_old) > MAX_CACHE_AGE:
            print(ansi.red("Cache is stale"), file=sys.stderr)
            return True
        return False

    @property
    def cache(self) -> Dict[str, List]:
        """Return cached json dictionary from cache file."""
        with self.cache_file.open("r") as fileh:
            return json.load(fileh)

    def _gencache(self):
        """Routine that generates the cache dictionary."""
        retval = {}
        print(
            ansi.banner(f"Rebuilding metasploit venom cache file at {self.cache_file}"),
            file=sys.stderr,
        )
        opts = ["payloads", "encoders", "formats", "archs", "encrypt", "platforms"]
        for opt in opts:
            print(ansi.section(f"Regenerating {opt}"), file=sys.stderr)
            retval[opt] = self._getoptions(opt)
            print(ansi.blue(f"count: {len(retval[opt])}"), file=sys.stderr)
        with self.cache_file.open("w") as fileh:
            json.dump(retval, fileh)


OPTS = """
-l  --list
-p  --payload
--list-options
-f  --format
-e  --encoder
--service-name
--sec-name
--smallest
--encrypt
--encrypt-key
--encrypt-iv 
-a  --arch
--platform
-o  --out
-b  --bad-chars
-n  --nopsled
--pad-nops
-s  --space
--encoder-space
-i  --iterations
-c  --add-code
-x  --template
-k  --keep
-v  --var-name
-t  --timeout
-h  --help
--help-formats
LHOST=
LPORT=
""".strip().split()
"""MSF Venom cli options."""


def get_venom_auto_complete():
    """Print out an autocomplete string that can be sourced in bash."""
    dat = VenomCache().cache
    fmt = "".join([f"\t{i}\n" for i in dat["formats"]])
    pay = "".join([f"\t{i}\n" for i in dat["payloads"]])
    enc = "".join([f"\t{i}\n" for i in dat["encoders"]])
    archs = "".join([f"\t{i}\n" for i in dat["archs"]])
    encrypt = "".join([f"\t{i}\n" for i in dat["encrypt"]])
    platforms = "".join([f"\t{i}\n" for i in dat["platforms"]])
    addresses = "".join([f"{i[2]}\n" for i in get_interfaces()])
    other_opt = "".join(f"\t{i}\n" for i in OPTS)
    TEMPLATE = (
        """
# Bash completion by Steven Hollingsworth
_msfvenom() {
    # local cur prev words cword
    # _init_completion -n = || return
    local cur prev

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # printf "%s\\n" "${COMP_WORDS[@]}" >> test.txt

    if [[ ${prev} == "L"* && ${cur} == "="* ]] ; then
        COMPREPLY=( $( compgen -W ' __addresses__ ' ) )
        return 0
    elif [[ "${prev}" = "=" && ${COMP_WORDS[*]} =~ "LHOST" ]]; then
        COMPREPLY=( $( compgen -W ' __addresses__ ' -- "$cur" ) )
        return 0
    # Don't allow repeats #TODO
    else
        case $prev in
            -f|--format)
                COMPREPLY=( $( compgen -W ' __fmt__ ' -- "$cur" ) )
                return 0
                ;;
            -e|--encoder)
                COMPREPLY=( $( compgen -W ' __enc__ ' -- "$cur" ) )
                return 0
                ;;
            -p|--payload)
                COMPREPLY=( $( compgen -W ' __pay__ ' -- "$cur" ) )
                return 0
                ;;
            -a|--arch)
                COMPREPLY=( $( compgen -W ' __arch__ ' -- "$cur" ) )
                return 0
                ;;
            --encrypt)
                COMPREPLY=( $( compgen -W ' __encrypt__ ' -- "$cur" ) )
                return 0
                ;;
            --platform)
                COMPREPLY=( $( compgen -W ' __platform__ ' -- "$cur" ) )
                return 0
                ;;
            -o|--out)
                _filedir
                return 0
                ;;
            -c|--add-code)
                _filedir
                return 0
                ;;
            -x|--template)
                _filedir
                return 0
                ;;
            *)
                COMPREPLY=($(compgen -W ' __other__ ' -- "${cur}") )
                # compopt +o nospace
                return 0
                ;;
        esac
    fi
} && complete -o nospace -F _msfvenom msfvenom
# } && complete -F _msfvenom msfvenom
    """.lstrip()
        .replace("__fmt__", fmt)
        .replace("__pay__", pay)
        .replace("__enc__", enc)
        .replace("__platform__", platforms)
        .replace("__encrypt__", encrypt)
        .replace("__arch__", archs)
        .replace("__addresses__", addresses)
        .replace("__other__", other_opt)
    )
    return TEMPLATE
