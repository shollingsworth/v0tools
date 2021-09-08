#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Version bumper on upload."""
import subprocess
from datetime import datetime
import configparser
import v0tools_doc


DTFMT = "%Y-%m-%d %H:%M UTC"


def commits(start, end):
    cmd = f"git rev-list {start}...{end}".split()
    return subprocess.check_output(cmd, encoding="utf-8").splitlines()


def commit_details(commit):
    cmd = ["git", "show", "--quiet", commit, "--pretty=%ct:::%s:::%b"]
    epoch, msg, desc = subprocess.check_output(cmd, encoding="utf-8").split(":::")
    dto = datetime.utcfromtimestamp(int(epoch))
    return dto.strftime(DTFMT), msg.strip(), desc.strip()


def get_repo_url():
    config = configparser.ConfigParser()
    config.read(v0tools_doc.SETUP_CFG)
    vals = [
        list(map(str.strip, i.strip().split("=")))
        for i in config.get("metadata", "project_urls").splitlines()
        if i.strip()
    ]
    urls = {i[0]: i[1] for i in vals}
    return urls["Source Code"]


def _sort_tags(tag):
    arr = map(int, tag.replace("v", "").split("."))
    return tuple(arr)


def get_changlog():
    cmd = "git rev-list --max-parents=0 HEAD".split()
    initial_commit = subprocess.check_output(cmd, encoding="utf-8").strip()
    tags = subprocess.check_output(
        ["git", "tag", "-l"],
        encoding="utf-8",
    ).splitlines()
    tags = sorted(tags, key=_sort_tags)[::-1]
    # tags.insert(0, "HEAD")
    content = []
    url = get_repo_url()
    for i in range(len(tags)):
        try:
            end, start = tags[i], tags[i + 1]
        except IndexError:
            end, start = tags[i], initial_commit

        endtxt = "v" + v0tools_doc.VERSION_FILE.read_text() if end == "HEAD" else end
        commit_list = commits(start, end)
        if not commit_list:
            continue
        content.append(f"# {endtxt}")
        for idx, com in enumerate(commit_list):
            dt, msg, desc = commit_details(com)
            content.append(f"{msg}")
            if idx == 0 and end == "HEAD":
                content.append(f"> {dt} [HEAD]({url}/commit/HEAD)")
            else:
                content.append(f"> {dt} [{com[:7]}]({url}/commit/{com})")
            content.append("")
            if desc:
                content.append(f"```")
                content.append(desc)
                content.append(f"```")
        content.append("---")
    return "\n".join(content)
