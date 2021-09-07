#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Jinja Template Engine."""
import jinja2
import v0tools_doc

_template_loader = jinja2.FileSystemLoader(
    searchpath=v0tools_doc.TEMPLATE_DIR.resolve()
)

templateEnv = jinja2.Environment(loader=_template_loader)

GITHUB_README = templateEnv.get_template("github.md")
MAIN_README = templateEnv.get_template("site_main.md")
