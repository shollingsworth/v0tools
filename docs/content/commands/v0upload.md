---
description: HTTP server that accepts PUT requests from remotes.
geekdocAlign: left
geekdocDescription: HTTP server that accepts PUT requests from remotes.
title: v0upload.py
weight: 20

---

> **HTTP server that accepts PUT requests from remotes.**

{{< tabs "9e48072b0ee29e699173479724cb3f20" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/v0upload.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: v0upload.py [-h] [--interface INTERFACE] [--ipv {4,6}] [-p PORT] path

HTTP server that accepts PUT requests from remotes.

positional arguments:
  path                  Directory or file path.

optional arguments:
  -h, --help            show this help message and exit
  --interface INTERFACE, -i INTERFACE
                        network interface: i.e. tun0, eth0, if undefined, an fzf prompt will appear
  --ipv {4,6}           IP Version
  -p PORT, --port PORT  Directory or file path.
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP server that accepts PUT requests from remotes."""
from v0tools import cli
from v0tools.servers import httpserv

cli = cli.Cli()
cli.add_path()
cli.add_ipv_interface()
cli.add_port()

parser = cli.parser


def main(args):
    """Run main function."""
    httpserv.uploader(
        args.address,
        str(args.port),
        args.path,
    )


cli.set_entrypoint(main)

if __name__ == "__main__":
    args = cli.get_parse()
    main(args)

```

{{< /tab >}}
{{< /tabs >}}
