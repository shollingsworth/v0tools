#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search for vulnerable calls / strings in php code.

Example Repo: https://github.com/OWASP/Vulnerable-Web-Application.git
"""
from v0tools import exceptions
from v0tools.ansi import green, red, magenta
from v0tools.lib.filesystem import iterfiles
from v0tools.cli import Cli

VULN_STRINGS = {
    # str: url (if applicable)
    # "${": None,
    b"eval": None,
    b"assert": None,
    b"preg_replace": None,
    b"create_function": None,
    b"include": None,
    b"require": None,
    b"ReflectionFunction": None,
    b"invoke": None,
    b"serialize": b"https://book.hacktricks.xyz/pentesting-web/deserialization#php",
}

cli = Cli()

parser = cli.parser
cli.add_path()

parser.add_argument(
    "--filter",
    "-f",
    help="i.e. *.php or *.py",
    default="*.php",
    type=str,
)
parser.add_argument(
    "--inc_lines",
    "-l",
    help="number of lines to include before / after match",
    type=int,
    default=3,
)


def _check_vuln(filename, args):
    with open(filename, "rb") as fileh:
        lines = list(fileh.readlines())
        for idx, line in enumerate(lines):
            for cstr, url in VULN_STRINGS.items():
                if cstr in line:
                    retlines = lines[idx - args.inc_lines : idx + args.inc_lines]
                    yield idx, retlines, cstr, url


def main(args):
    """Run main function."""
    files = []
    fcnt = 0
    for filename in iterfiles(args.path, args.filter):
        fcnt += 1
        for idx, lines, cstr, url in _check_vuln(filename, args):
            url = green(url) if url else ""
            title = magenta(f"\n{filename} : {idx} {url}\n")
            print(title)
            output = b"".join(lines).replace(cstr, red(cstr.decode()).encode())
            for line in output.splitlines():
                print(f"   {line.decode()}")
            files.append([idx, filename])
    if fcnt == 0:
        raise exceptions.NoAction(
            "No files were scanned, maybe try adjusting the filter?"
        )
    if not files:
        raise exceptions.NoAction(f"Could not find any vulns in dir {args.path}")
    print("\n\n")
    vimcmd = ["vim"] + [f'-c "tabnew +{ln + 1} {fn}"' for ln, fn in files]
    print(magenta(" ".join(vimcmd)))


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse("--help")
    # args = cli.get_parse("~/repos/Vulnerable-Web-Application -f '*.php' -l 3")
    cli.run(args)
