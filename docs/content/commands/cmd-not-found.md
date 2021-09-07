---
description: "Print how to install packages on different operating systems\n\nThanks\
  \ to https://command-not-found.com/ and\n\u023Dukasz Lach https://twitter.com/lach_dev\
  \ for hosting the site"
geekdocAlign: left
geekdocDescription: "Print how to install packages on different operating systems\n\
  \nThanks to https://command-not-found.com/ and\n\u023Dukasz Lach https://twitter.com/lach_dev\
  \ for hosting the site"
title: cmd-not-found.py
weight: 99

---

> **Print how to install packages on different operating systems**
> 
> **Thanks to https://command-not-found.com/ and**
> **Ƚukasz Lach https://twitter.com/lach_dev for hosting the site**

{{< tabs "d903902a44e8ed0455175edd709eb497" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/cmd-not-found.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: cmd-not-found.py [-h] command

Print how to install packages on different operating systems

Thanks to https://command-not-found.com/ and
Ƚukasz Lach https://twitter.com/lach_dev for hosting the site

positional arguments:
  command     command help

optional arguments:
  -h, --help  show this help message and exit
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print how to install packages on different operating systems

Thanks to https://command-not-found.com/ and
Ƚukasz Lach https://twitter.com/lach_dev for hosting the site

"""
from bs4 import BeautifulSoup
import requests
import json
from v0tools.cli import Cli

cli = Cli()
parser = cli.parser
parser.add_argument(
    "command",
    help="command help",
    type=str,
)


def main(args):
    """Run main function."""
    # txt = pathlib.Path("./test.html").read_text()
    txt = requests.get(f"https://command-not-found.com/{args.command}")
    val = BeautifulSoup(txt.content, "lxml")
    vals = {}
    for i in val.findAll("div"):
        if "command-install" not in i.attrs["class"]:
            continue
        os = i.attrs.get("data-os")
        if not os:
            continue
        code = i.find("code").getText()
        vals[os] = code
    print(json.dumps(vals, indent=4, separators=(",", " : ")))


if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse("booga")
    cli.set_entrypoint(main)
    cli.run(args)

```

{{< /tab >}}
{{< /tabs >}}
