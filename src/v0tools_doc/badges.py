#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
import pathlib
import v0tools_doc

STYLE = "plastic"

keymap = {
    "github-stars": "stargazers",
    "github-forks": "network/members",
    "github-issues": "issues",
}


def githubs(github):
    user, ext = github.split("/")
    urls = [
        f"https://img.shields.io/github/issues/{github}",
        f"https://img.shields.io/github/languages/code-size/{github}",
        f"https://img.shields.io/github/stars/{github}",
        f"https://img.shields.io/github/forks/{github}",
    ]
    for i in urls:
        arr = i.split("/")
        key = "-".join(i for i in arr[3:6] if i != user)
        if key in keymap:
            url = f"https://github.com/{github}/{keymap[key]}"
        else:
            url = f"https://github.com/{github}"
        yield f'[![{key}]({i}?style={STYLE} "{key}")]({url}) '


def pypis(pkgname):
    urls = [
        f"https://img.shields.io/pypi/v/{pkgname}",  # latest version
        f"https://img.shields.io/pypi/status/{pkgname}",  # stable / dev
        f"https://img.shields.io/pypi/l/{pkgname}",  # license
        # this doesn't seem to be working
        # f"https://img.shields.io/pypi/dm/{pkgname}",  # downloads / month
        f"https://img.shields.io/pypi/pyversions/{pkgname}",  # python versions
        f"https://img.shields.io/pypi/implementation/{pkgname}",  # implimentation
    ]
    for i in urls:
        arr = i.split("/")
        key = "-".join(arr[3:5])
        url = f"https://pypi.org/project/{pkgname}"
        yield f'[![{key}]({i}?style={STYLE} "{key}")]({url}) '


def get_badges():
    config = configparser.ConfigParser()
    config.read(v0tools_doc.SETUP_CFG)
    pkgname = config.get("metadata", "name").replace("_", "-")
    github = "/".join(pathlib.Path(v0tools_doc.GITHUB_URL).parts[-2:])
    b_github = "".join(githubs(github))
    b_pypi = "".join(pypis(pkgname))
    return "\n\n".join([b_github, b_pypi])
