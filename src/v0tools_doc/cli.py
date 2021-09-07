#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cli Documentation class."""
from inspect import cleandoc
from typing import Dict
from types import ModuleType
from inspect import cleandoc
from pathlib import Path
from v0tools.cli import Cli
import v0tools_doc
from v0tools_doc import hugo
from v0tools_doc.hugo import ShortCode
import shutil
import os

ME = Path(__file__).resolve()

DOC_PATH = "commands"

EXT = ".webm"


class CliInfo(object):
    def __init__(self, script: Path):
        self.help = ""
        self.script = script
        self.name = script.name
        self.media_file = v0tools_doc.MEDIA_DIR.joinpath(script.name + EXT)
        self.media_path = self.media_file.relative_to(v0tools_doc.ROOT_DIR)
        self.module = ModuleType(script.name)  # type: ModuleType
        self._setvals()

    def _setvals(self):
        script = self.script
        if script.name.endswith(".py"):
            mod_name = script.name.replace(".py", "")
            self.module = __import__(mod_name)
            self.doc = cleandoc(self.module.__doc__)
            cli = self.module.cli  # type: Cli
            help_txt = cli.parser.format_help().splitlines()
            l1 = help_txt[0].split(" ")
            l1[1] = script.name
            help_txt[0] = " ".join(l1)
            # usage = re.sub(r"^usage: \w.+ ", f"usage: {script.name} ", help_txt)
            self.help = "\n".join(help_txt)

    @property
    def has_media(self):
        return self.media_file.exists()

    @property
    def is_executable(self):
        return not any(
            [
                self.script.is_dir(),
                not os.access(self.script, os.X_OK),
            ]
        )

    @property
    def url_relative(self):
        return f"{DOC_PATH}/{self.script.name.rstrip('.py')}/"

    @property
    def url(self):
        return f"{v0tools_doc.SITE_BASE}/{self.url_relative}"

    @property
    def readme_text(self):
        txt = []
        docstr = cleandoc(self.module.__doc__)
        if docstr:
            docstr = [i for i in self.module.__doc__.splitlines() if i.strip()][0]

        docpath = f"{v0tools_doc.SITE_BASE}/commands/{self.script.name}"
        pagelink = f"*[{self.name}]({docpath})*"
        txt.append(f"* {pagelink}")
        if docstr:
            txt.append(f"    * {docstr}")
        return "\n".join(txt)

    @property
    def doc_text(self):
        txt = []
        # strip static for path
        munge = "/".join(i for i in self.media_path.parts if i != "static")
        media_link = f"/{munge}"
        txt.append(ShortCode.quote_bold(self.doc))
        tab = hugo.Tab()
        txt.append("")
        tab.add_tab("Screencast", ShortCode.webm(media_link))
        tab.add_tab("Help", ShortCode.code(self.help, "bash"))
        tab.add_tab("Source", ShortCode.code(self.script.read_text(), "python"))
        txt.append(tab.content)
        return "\n".join(txt)


class DocGroup(object):
    def __init__(self):
        self._no_media = []
        self._main_lines = []
        self.collection = {}  # type: Dict[str, CliInfo]
        self._gen()
        self.doc_dir = v0tools_doc.CONTENT_DIR.joinpath("commands")
        self.doc_dir.exists() or self.doc_dir.mkdir()
        self.command_index = self.doc_dir.joinpath("_index.md")

    def get_command_main(self):
        for k, cliobj in self.collection.items():
            yield k, cliobj.doc, cliobj.url_relative

    def write_content(self):
        with self.command_index.open("w") as fileh:
            obj = hugo.Page("Commands", "CLI Utilities")
            obj.body = "{{< toc-tree >}}"
            fileh.write(obj.content)

        for k, cliobj in self.collection.items():
            path = self.doc_dir.joinpath(k.rstrip(".py") + ".md")
            page = hugo.Page(k, cliobj.doc)
            if "rshell" in str(path):
                page.weight = 10
            elif cliobj.name.startswith("v0"):
                page.weight = 20
            page.body = cliobj.doc_text
            with path.open("w") as fileh:
                fileh.write(page.content)

    def _gen(self):
        for script in sorted(v0tools_doc.BINDIR.glob("*")):
            obj = CliInfo(script)
            if not obj.is_executable:
                continue

            if not obj.has_media:
                self._no_media.append(obj.name)

            if self._no_media:
                continue

            self._main_lines.append(obj.readme_text)
            self.collection[script.name] = obj

        if self._no_media:
            msg = ["The following cli commands are missing media...."]
            for i in self._no_media:
                msg.append(f"\t{i}")
            msg.append("Bailing... please fix")
            raise SystemExit("\n".join(msg))

    def __iter__(self):
        for k, obj in self.collection.items():
            single_line = obj.doc.splitlines()[0]
            yield k, {
                "url": obj.url,
                "url_relative": obj.url_relative,
                "description": obj.doc,
                "single": single_line,
            }

    @property
    def __dict__(self):
        return {k: v for k, v in self}
