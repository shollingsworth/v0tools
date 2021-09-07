---
description: Sourceable Autocomplete for msfvenom flags.
geekdocAlign: left
geekdocDescription: Sourceable Autocomplete for msfvenom flags.
title: v0_bash_complete_msfvenom.py
weight: 20

---

> **Sourceable Autocomplete for msfvenom flags.**

{{< tabs "b537894e61193dd4fa751b8c7a0db5ac" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/v0_bash_complete_msfvenom.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: v0_bash_complete_msfvenom.py [-h]

Sourceable Autocomplete for msfvenom flags.

optional arguments:
  -h, --help  show this help message and exit
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sourceable Autocomplete for msfvenom flags."""
from v0tools.msf import get_venom_auto_complete
from v0tools.cli import Cli


def main(args):
    """Run main function."""
    print("##### Venom Autocomplete", flush=True)
    print(get_venom_auto_complete(), flush=True)


cli = Cli()
cli.set_entrypoint(main)
cli.set_required_binaries(["msfvenom"])

if __name__ == "__main__":
    args = cli.get_parse()
    cli.run(args)

```

{{< /tab >}}
{{< /tabs >}}
