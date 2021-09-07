---
description: HTTP Serve a directory, or serve a single isolated file.
geekdocAlign: left
geekdocDescription: HTTP Serve a directory, or serve a single isolated file.
title: v0serv.py
weight: 20

---

> **HTTP Serve a directory, or serve a single isolated file.**

{{< tabs "51fe5bc2ee3531b6e12278a2177c41af" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/v0serv.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: v0serv.py [-h] [--interface INTERFACE] [--ipv {4,6}] [-p PORT] [-d {none,certutil,ps-download,ps-exec}] path

HTTP Serve a directory, or serve a single isolated file.

positional arguments:
  path                  Directory or file path.

optional arguments:
  -h, --help            show this help message and exit
  --interface INTERFACE, -i INTERFACE
                        network interface: i.e. tun0, eth0, if undefined, an fzf prompt will appear
  --ipv {4,6}           IP Version
  -p PORT, --port PORT  Directory or file path.
  -d {none,certutil,ps-download,ps-exec}, --display {none,certutil,ps-download,ps-exec}
                        display type
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP Serve a directory, or serve a single isolated file."""
from v0tools import cli
from v0tools.servers import httpserv

cli = cli.Cli(__doc__)
cli.add_path()
cli.add_ipv_interface()
cli.add_port()
parser = cli.parser

parser.add_argument(
    "-d",
    "--display",
    help="display type",
    choices=httpserv.SERV_PREFIXES.keys(),
    default="none",
    type=str,
)


def main(args):
    """Run main function."""
    httpserv.serve(
        args.address,
        str(args.port),
        args.path,
        args.display,
    )


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    # args = cli.get_parse("-i lo ./")
    cli.run(args)

```

{{< /tab >}}
{{< /tabs >}}
