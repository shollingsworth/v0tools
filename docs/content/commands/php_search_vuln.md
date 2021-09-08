---
description: 'Search for vulnerable calls / strings in php code.


  Example Repo: https://github.com/OWASP/Vulnerable-Web-Application.git'
geekdocAlign: left
geekdocDescription: 'Search for vulnerable calls / strings in php code.


  Example Repo: https://github.com/OWASP/Vulnerable-Web-Application.git'
title: php_search_vuln.py
weight: 99

---

> **Search for vulnerable calls / strings in php code.**
> 
> **Example Repo: https://github.com/OWASP/Vulnerable-Web-Application.git**

{{< tabs "0dcba41fafdfab9ca18b874d6477c3bf" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/php_search_vuln.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: php_search_vuln.py [-h] [--filter_ext FILTER_EXT] [--inc_lines INC_LINES] path

Search for vulnerable calls / strings in php code.

Example Repo: https://github.com/OWASP/Vulnerable-Web-Application.git

positional arguments:
  path                  Directory or file path.

optional arguments:
  -h, --help            show this help message and exit
  --filter_ext FILTER_EXT, -f FILTER_EXT
                        i.e. *.php or *.py
  --inc_lines INC_LINES, -l INC_LINES
                        number of lines to include before / after match
```

{{< /tab >}}
{{< tab "Source" >}}

```python
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
    "--filter_ext",
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
    for filename in iterfiles(args.path, args.filter_ext):
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

```

{{< /tab >}}
{{< /tabs >}}
