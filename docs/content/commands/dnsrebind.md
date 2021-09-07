---
description: dns rebinding fqdn.
geekdocAlign: left
geekdocDescription: dns rebinding fqdn.
title: dnsrebind.py
weight: 99

---

> **dns rebinding fqdn.**

{{< tabs "c7fe28b3a12331a1d37071baa535c7d5" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/dnsrebind.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: dnsrebind.py [-h] [--test_count TEST_COUNT] [--verbose] normalip rebindip

dns rebinding fqdn.

positional arguments:
  normalip              initial ip
  rebindip              rebind ip

optional arguments:
  -h, --help            show this help message and exit
  --test_count TEST_COUNT, -t TEST_COUNT
                        test count
  --verbose, -v         verbose
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dns rebinding fqdn."""
from v0tools.attacks.dnsrebind import get_fqdn
from v0tools.lib.log import get_log
from v0tools.cli import Cli, exceptions
import argparse
import socket
import concurrent.futures as confu
import random
import time
from collections import Counter

SECONDS = 5
MAX_TEST_COUNT = 250
MIN_TEST_COUNT = 50

LOG = get_log()

cli = Cli()


parser = cli.parser

parser.add_argument(
    "normalip",
    help="initial ip",
    type=str,
)
parser.add_argument(
    "rebindip",
    help="rebind ip",
    type=str,
)

parser.add_argument(
    "--test_count",
    "-t",
    help="test count",
    default=0,
    type=int,
)

parser.add_argument(
    "--verbose",
    "-v",
    action="store_true",
    help="verbose",
    default=False,
)


def _q(fqdn):
    sl_int = random.randint(200, SECONDS * 1000)
    time.sleep(0.001 * sl_int)
    return socket.gethostbyname(fqdn)


def main(args):
    """Run main function."""
    fqdn = get_fqdn(args.normalip, args.rebindip)
    responses = Counter()
    if args.test_count:
        if args.test_count >= MAX_TEST_COUNT:
            msg = f"test count should be below {MAX_TEST_COUNT}"
            raise exceptions.InvalidCliArgument("--test_count", msg)
        if args.test_count <= MIN_TEST_COUNT:
            msg = f"test count should be above {MIN_TEST_COUNT}"
            raise exceptions.InvalidCliArgument("--test_count", msg)

        LOG.info(f"Running tests on: {fqdn}")
        LOG.info(f"This will finish in ~{SECONDS} seconds")
        with confu.ThreadPoolExecutor(args.test_count) as executor:
            futures = [executor.submit(_q, fqdn) for _ in range(args.test_count)]
            for future in confu.as_completed(futures):
                res = future.result()
                responses[res] += 1
                if args.verbose:
                    LOG.info("Query result: %s", res)
        LOG.info("Result Count Summary:")
        for k, v in responses.most_common():
            LOG.info("%s: %s", k, v)
    else:
        print(fqdn)


cli.set_entrypoint(main)

if __name__ == "__main__":
    # args = parser.parse_args(["8.8.8.8", "127.0.0.1", "-t", "100"])
    args = cli.get_parse()
    cli.run(args)

```

{{< /tab >}}
{{< /tabs >}}
