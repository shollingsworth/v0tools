---
description: 'Search for executable names in PATH


  Helpful for finding the names of commands you can''t remember'
geekdocAlign: left
geekdocDescription: 'Search for executable names in PATH


  Helpful for finding the names of commands you can''t remember'
title: binpathsearch.py
weight: 99

---

> **Search for executable names in PATH**
> 
> **Helpful for finding the names of commands you can't remember**

{{< tabs "9f56a86668b170115249c348e4b8604c" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/binpathsearch.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: binpathsearch.py [-h] [-f [FILTER ...]]

Search for executable names in PATH

Helpful for finding the names of commands you can't remember

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
"""
Search for executable names in PATH

Helpful for finding the names of commands you can't remember
"""
import os
from pathlib import Path
from v0tools.cli import Cli

cli = Cli()
parser = cli.parser
cli.add_filter()


def vals():
    paths = os.environ["PATH"].split(":")
    dirs = [Path(p) for p in paths]
    vals = set()
    for path in dirs:
        for file in path.iterdir():
            if file.is_dir():
                continue
            _apath = file.resolve()
            is_exec = os.access(str(_apath), os.X_OK)
            if not is_exec:
                continue
            if _apath.name not in vals:
                yield _apath.name
            vals.add(_apath.name)


def main(args):
    """Run main function."""
    for i in sorted(vals()):
        if args.filter:
            if all([z in i for z in args.filter]):
                print(i)
        else:
            print(i)


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse(["-f", "crack"])
    cli.run(args)

```

{{< /tab >}}
{{< /tabs >}}
