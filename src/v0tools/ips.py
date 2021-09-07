#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ip URL obfs script."""
import itertools
from v0tools.lib.util import splitter

FUNKY_PERIOD = chr(0xFF0E)
"""A period, but not a period."""
BUBBLE_MAP = {str(idx + 1): chr(i) for idx, i in enumerate(range(9312, 9321))}
"""
Dictionary of bubble map values
{'1': '①', '2': '②', ...}
"""
BUBBLE_MAP["."] = FUNKY_PERIOD
BUBBLE_MAP["0"] = chr(9450)


def all_ip_encodings(ip):
    r"""Show all variations of different ip obsfucation types.

    code: ::
        import json
        res = all_ip_encodings("127.0.0.1")
        print(json.dumps(res, indent=4, separators=(",", " : ")))

    output: ::
        {
            "base" : [
                "127.0.0.1",
                "0x7f000001",
                "2130706433",
                "017700000001",
                "\u2460\u2461\u2466\uff0e\u24ea\uff0e\u24ea\uff0e\u2460",
                "%31%32%37%2e%30%2e%30%2e%31"
            ],
            "int" : [
                "127.1",
                "127.0.1",
                "127.0.0.1"
            ],
            "hex" : [
                "0x7f.0x000001",
                "0x7f.0x00.0x0001",
                "0x7f.0x00.0x00.0x01"
            ],
            "oct" : [
                "0177.01",
                "0177.00.01",
                "0177.00.00.01"
            ],
            "mix" : [
                "127.1",
                "127.0x000001",
                "127.01",
                "0x7f.1",
                "0x7f.0x000001",
                "0x7f.01",
                "0177.1",
                "0177.0x000001",
                "0177.01",
                "127.0.1",
                "127.0.0x0001",
                "127.0.01",
                "127.0x00.1",
                "127.0x00.0x0001",
                "127.0x00.01",
                "127.00.1",
                "127.00.0x0001",
                "127.00.01",
                "0x7f.0.1",
                "0x7f.0.0x0001",
                "0x7f.0.01",
                "0x7f.0x00.1",
                "0x7f.0x00.0x0001",
                "0x7f.0x00.01",
                "0x7f.00.1",
                "0x7f.00.0x0001",
                "0x7f.00.01",
                "0177.0.1",
                "0177.0.0x0001",
                "0177.0.01",
                "0177.0x00.1",
                "0177.0x00.0x0001",
                "0177.0x00.01",
                "0177.00.1",
                "0177.00.0x0001",
                "0177.00.01",
                "127.0.0.1",
                "127.0.0.0x01",
                "127.0.0.01",
                "127.0.0x00.1",
                "127.0.0x00.0x01",
                "127.0.0x00.01",
                "127.0.00.1",
                "127.0.00.0x01",
                "127.0.00.01",
                "127.0x00.0.1",
                "127.0x00.0.0x01",
                "127.0x00.0.01",
                "127.0x00.0x00.1",
                "127.0x00.0x00.0x01",
                "127.0x00.0x00.01",
                "127.0x00.00.1",
                "127.0x00.00.0x01",
                "127.0x00.00.01",
                "127.00.0.1",
                "127.00.0.0x01",
                "127.00.0.01",
                "127.00.0x00.1",
                "127.00.0x00.0x01",
                "127.00.0x00.01",
                "127.00.00.1",
                "127.00.00.0x01",
                "127.00.00.01",
                "0x7f.0.0.1",
                "0x7f.0.0.0x01",
                "0x7f.0.0.01",
                "0x7f.0.0x00.1",
                "0x7f.0.0x00.0x01",
                "0x7f.0.0x00.01",
                "0x7f.0.00.1",
                "0x7f.0.00.0x01",
                "0x7f.0.00.01",
                "0x7f.0x00.0.1",
                "0x7f.0x00.0.0x01",
                "0x7f.0x00.0.01",
                "0x7f.0x00.0x00.1",
                "0x7f.0x00.0x00.0x01",
                "0x7f.0x00.0x00.01",
                "0x7f.0x00.00.1",
                "0x7f.0x00.00.0x01",
                "0x7f.0x00.00.01",
                "0x7f.00.0.1",
                "0x7f.00.0.0x01",
                "0x7f.00.0.01",
                "0x7f.00.0x00.1",
                "0x7f.00.0x00.0x01",
                "0x7f.00.0x00.01",
                "0x7f.00.00.1",
                "0x7f.00.00.0x01",
                "0x7f.00.00.01",
                "0177.0.0.1",
                "0177.0.0.0x01",
                "0177.0.0.01",
                "0177.0.0x00.1",
                "0177.0.0x00.0x01",
                "0177.0.0x00.01",
                "0177.0.00.1",
                "0177.0.00.0x01",
                "0177.0.00.01",
                "0177.0x00.0.1",
                "0177.0x00.0.0x01",
                "0177.0x00.0.01",
                "0177.0x00.0x00.1",
                "0177.0x00.0x00.0x01",
                "0177.0x00.0x00.01",
                "0177.0x00.00.1",
                "0177.0x00.00.0x01",
                "0177.0x00.00.01",
                "0177.00.0.1",
                "0177.00.0.0x01",
                "0177.00.0.01",
                "0177.00.0x00.1",
                "0177.00.0x00.0x01",
                "0177.00.0x00.01",
                "0177.00.00.1",
                "0177.00.00.0x01",
                "0177.00.00.01"
            ]
        }
    """
    # splitter lengths that are invalid
    bad_cmaps = (
        (1, 2, 1),
        (2, 2),
        (2, 1, 1),
        (3, 1),
    )

    octs = ip.split(".")
    hval = "".join(f"{int(i):02x}" for i in octs)
    ival = int(hval, 16)

    ouput_map = {
        "base": [
            ip,
            f"0x{hval}",
            str(ival),
            f"0{int(hval, 16):o}",
            "".join(BUBBLE_MAP[i] for i in ip),
            "".join("%" + f"{ord(i):02x}" for i in ip),
        ],
    }

    for _, vset in enumerate(splitter(octs)):
        hexset = [bytearray(map(int, i)).hex() for i in vset]
        cmap = tuple(len(i) for i in vset)
        # Skip invalid maps
        if cmap in bad_cmaps:
            continue
        fstrs = {
            # 216.58.214.227 (google)
            "int": [f"{int(n, 16)}" for n in hexset],
            # hex: 0xd8.0x3a.0xd6.0xe3
            "hex": [f"0x{n}" for n in hexset],
            # octal: 0330.072.0326.0343
            "oct": [f"0{int(n, 16):o}" for n in hexset],
        }

        # common vals
        for key, i in fstrs.items():
            val = ".".join(i)
            ouput_map.setdefault(key, [])
            if val in ouput_map[key]:
                continue
            ouput_map[key].append(val)

        # mixing up all the values
        z = list(zip(*fstrs.values()))
        for i in itertools.product(*z):
            val = ".".join(i)
            ouput_map.setdefault("mix", [])
            if val in ouput_map["mix"]:
                continue
            ouput_map["mix"].append(val)
    return ouput_map


def get_urls(ip):
    """
    code: ::
        print(get_urls("216.58.194.196"))

    output: ::
        base http://216.58.194.196
        base http://0xd83ac2c4
        base http://3627729604
        base http://033016541304
        base http://②①⑥．⑤⑧．①⑨④．①⑨⑥
        base http://%32%31%36%2e%35%38%2e%31%39%34%2e%31%39%36
        int http://216.3850948
        int http://216.58.49860
        int http://216.58.194.196
        hex http://0xd8.0x3ac2c4
        hex http://0xd8.0x3a.0xc2c4
        hex http://0xd8.0x3a.0xc2.0xc4
        oct http://0330.016541304
        oct http://0330.072.0141304
        oct http://0330.072.0302.0304
        mix http://216.3850948
        mix http://216.0x3ac2c4
        mix http://216.016541304
        mix http://0xd8.3850948
        mix http://0xd8.0x3ac2c4
        mix http://0xd8.016541304
        mix http://0330.3850948
        mix http://0330.0x3ac2c4
        mix http://0330.016541304
        mix http://216.58.49860
        mix http://216.58.0xc2c4
        mix http://216.58.0141304
        mix http://216.0x3a.49860
        mix http://216.0x3a.0xc2c4
        mix http://216.0x3a.0141304
        mix http://216.072.49860
        mix http://216.072.0xc2c4
        mix http://216.072.0141304
        mix http://0xd8.58.49860
        mix http://0xd8.58.0xc2c4
        mix http://0xd8.58.0141304
        mix http://0xd8.0x3a.49860
        mix http://0xd8.0x3a.0xc2c4
        mix http://0xd8.0x3a.0141304
        mix http://0xd8.072.49860
        mix http://0xd8.072.0xc2c4
        mix http://0xd8.072.0141304
        mix http://0330.58.49860
        mix http://0330.58.0xc2c4
        mix http://0330.58.0141304
        mix http://0330.0x3a.49860
        mix http://0330.0x3a.0xc2c4
        mix http://0330.0x3a.0141304
        mix http://0330.072.49860
        mix http://0330.072.0xc2c4
        mix http://0330.072.0141304
        mix http://216.58.194.196
        mix http://216.58.194.0xc4
        mix http://216.58.194.0304
        mix http://216.58.0xc2.196
        mix http://216.58.0xc2.0xc4
        mix http://216.58.0xc2.0304
        mix http://216.58.0302.196
        mix http://216.58.0302.0xc4
        mix http://216.58.0302.0304
        mix http://216.0x3a.194.196
        mix http://216.0x3a.194.0xc4
        mix http://216.0x3a.194.0304
        mix http://216.0x3a.0xc2.196
        mix http://216.0x3a.0xc2.0xc4
        mix http://216.0x3a.0xc2.0304
        mix http://216.0x3a.0302.196
        mix http://216.0x3a.0302.0xc4
        mix http://216.0x3a.0302.0304
        mix http://216.072.194.196
        mix http://216.072.194.0xc4
        mix http://216.072.194.0304
        mix http://216.072.0xc2.196
        mix http://216.072.0xc2.0xc4
        mix http://216.072.0xc2.0304
        mix http://216.072.0302.196
        mix http://216.072.0302.0xc4
        mix http://216.072.0302.0304
        mix http://0xd8.58.194.196
        mix http://0xd8.58.194.0xc4
        mix http://0xd8.58.194.0304
        mix http://0xd8.58.0xc2.196
        mix http://0xd8.58.0xc2.0xc4
        mix http://0xd8.58.0xc2.0304
        mix http://0xd8.58.0302.196
        mix http://0xd8.58.0302.0xc4
        mix http://0xd8.58.0302.0304
        mix http://0xd8.0x3a.194.196
        mix http://0xd8.0x3a.194.0xc4
        mix http://0xd8.0x3a.194.0304
        mix http://0xd8.0x3a.0xc2.196
        mix http://0xd8.0x3a.0xc2.0xc4
        mix http://0xd8.0x3a.0xc2.0304
        mix http://0xd8.0x3a.0302.196
        mix http://0xd8.0x3a.0302.0xc4
        mix http://0xd8.0x3a.0302.0304
        mix http://0xd8.072.194.196
        mix http://0xd8.072.194.0xc4
        mix http://0xd8.072.194.0304
        mix http://0xd8.072.0xc2.196
        mix http://0xd8.072.0xc2.0xc4
        mix http://0xd8.072.0xc2.0304
        mix http://0xd8.072.0302.196
        mix http://0xd8.072.0302.0xc4
        mix http://0xd8.072.0302.0304
        mix http://0330.58.194.196
        mix http://0330.58.194.0xc4
        mix http://0330.58.194.0304
        mix http://0330.58.0xc2.196
        mix http://0330.58.0xc2.0xc4
        mix http://0330.58.0xc2.0304
        mix http://0330.58.0302.196
        mix http://0330.58.0302.0xc4
        mix http://0330.58.0302.0304
        mix http://0330.0x3a.194.196
        mix http://0330.0x3a.194.0xc4
        mix http://0330.0x3a.194.0304
        mix http://0330.0x3a.0xc2.196
        mix http://0330.0x3a.0xc2.0xc4
        mix http://0330.0x3a.0xc2.0304
        mix http://0330.0x3a.0302.196
        mix http://0330.0x3a.0302.0xc4
        mix http://0330.0x3a.0302.0304
        mix http://0330.072.194.196
        mix http://0330.072.194.0xc4
        mix http://0330.072.194.0304
        mix http://0330.072.0xc2.196
        mix http://0330.072.0xc2.0xc4
        mix http://0330.072.0xc2.0304
        mix http://0330.072.0302.196
        mix http://0330.072.0302.0xc4
        mix http://0330.072.0302.0304
    """
    for k, arr in all_ip_encodings(ip).items():
        for enc_ip in arr:
            print(k, f"http://{enc_ip}", flush=True)
