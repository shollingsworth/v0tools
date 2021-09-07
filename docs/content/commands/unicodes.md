---
description: print unicode values and associated information to stdout.
geekdocAlign: left
geekdocDescription: print unicode values and associated information to stdout.
title: unicodes.py
weight: 99

---

> **print unicode values and associated information to stdout.**

{{< tabs "d2bc39555ba1405a38c6e1860ac479d2" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/unicodes.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: unicodes.py [-h] [-f [FILTER [FILTER ...]]]

print unicode values and associated information to stdout.

example:
    unicodes.py | fzf

optional arguments:
  -h, --help            show this help message and exit
  -f [FILTER [FILTER ...]], --filter [FILTER [FILTER ...]]
                        Filter string
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""print unicode values and associated information to stdout."""
from v0tools import chars, cli
import os

dstring = f"""
{__doc__}

example:
    {os.path.basename(__file__)} | fzf
"""

cli = cli.Cli(dstring)
parser = cli.parser

parser.add_argument(
    "-f",
    "--filter",
    nargs="*",
    help="Filter string",
    action="append",
    type=str,
    required=False,
    default=None,
)


def main(args):
    """Run main function."""
    if args.filter:
        fvalues = [i[0] for i in args.filter]
    else:
        fvalues = []
    for _, i in enumerate(chars.unicodes()):
        _int, _hex, _chr, name, uval, htmlent = i.values()
        line = f"{_chr} {name} int:{_int} hex:{_hex.zfill(2)} {uval} {htmlent}"
        if not fvalues:
            print(line, flush=True)
            continue
        if all([i in line for i in fvalues]):
            print(line, flush=True)


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse(["-f", "cat", "-f", "grin"])
    cli.run(args)
    # args = cli.get_parse("--help")

```

{{< /tab >}}
{{< /tabs >}}
