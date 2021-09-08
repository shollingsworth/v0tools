---
description: print unicode values and associated information to stdout.
geekdocAlign: left
geekdocDescription: print unicode values and associated information to stdout.
title: unicodes.py
weight: 99

---

> **print unicode values and associated information to stdout.**

{{< tabs "31cb1d5436440ad9a2295116961afaa4" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/unicodes.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: unicodes.py [-h] [-f [FILTER ...]]

print unicode values and associated information to stdout.

example:
    unicodes.py | fzf

optional arguments:
  -h, --help            show this help message and exit
  -f [FILTER ...], --filter [FILTER ...]
                        filter results based on fixed string.
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
cli.add_filter()
parser = cli.parser


def main(args):
    """Run main function."""
    for _, i in enumerate(chars.unicodes()):
        _int, _hex, _chr, name, uval, htmlent = i.values()
        line = f"{_chr} {name} int:{_int} hex:{_hex.zfill(2)} {uval} {htmlent}"
        if not args.filter:
            print(line, flush=True)
            continue
        if all([i in line for i in args.filter]):
            print(line, flush=True)


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    cli.run(args)

```

{{< /tab >}}
{{< /tabs >}}
