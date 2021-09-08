#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import v0tools_doc
import v0tools_doc.template as template
from v0tools.syspkgs import get_install_instructions
from v0tools_doc import cli, EnvGroup
from v0tools_doc.hugo import ShortCode
from v0tools_doc import hugo, changelog, badges
from pathlib import Path
import shutil

ABOUT = """
{{< toc >}}

# Theme
Hugo Theme: https://geekdocs.de

# About Me
SRE by day, security wonk by night Feel free to reach out on the Hack
the box [discord](https://discord.com/invite/hackthebox) , DM:`stev0`

""".lstrip()


def _root_path(dirname):
    _dir = v0tools_doc.CONTENT_DIR.joinpath(dirname)
    _dir.exists() or _dir.mkdir()
    file = _dir.joinpath("_index.md")
    return _dir, file


def clean(fpath: Path):
    for i in fpath.iterdir():
        if i.is_dir():
            print(f"removing dir {i}")
            shutil.rmtree(str(i))
            continue
        if i.exists():
            print(f"removing file {i}")
            i.unlink()


if __name__ == "__main__":
    clean(v0tools_doc.CONTENT_DIR)
    obj = cli.DocGroup()
    dval = dict(obj)

    config_dir, config_file = _root_path("configuration")
    inst_dir, inst_file = _root_path("sys_prerequisites")
    change_dir, change_file = _root_path("changelog")
    about_dir, about_file = _root_path("about")

    with about_file.open("w") as fileh:
        page = hugo.Page("About", "About Page")
        page.weight = 100
        page.body = ABOUT
        fileh.write(page.content)

    with change_file.open("w") as fileh:
        output = []
        page = hugo.Page("Changlog", "Version Control Changelog")
        page.weight = 150
        output.append(ShortCode.expand("{{< toc >}}", "TOC"))
        output.append(changelog.get_changlog())
        page.body = "\n".join(output)
        fileh.write(page.content)

    with inst_file.open("w") as fileh:
        output = []
        output.append("{{< toc-tree >}}")
        page = hugo.Page(
            "System Install",
            "OS Specific Install Procedures",
        )
        page.weight = 5
        page.body = "\n".join(output)
        fileh.write(page.content)

    expand_vals = {}

    for dist, (prereq, desc, instructions) in get_install_instructions().items():
        fpath = inst_dir.joinpath(f"{dist}.md")
        txt = []
        prereq_line = "\n".join(
            [
                "# Python / Package Pre-reqs",
                prereq,
            ]
        )

        exval = []
        exval.append(ShortCode.code(prereq_line, "bash"))
        exval.append(ShortCode.code(instructions, "bash"))
        exval.append(
            ShortCode.code("# install pip package\npip3 install v0tools", "bash")
        )

        expand_vals[desc] = "\n".join(exval)
        txt.append("\n".join(exval))

        page = hugo.Page(desc, "")
        page.body = "\n".join(txt)
        with fpath.open("w") as fileh:
            fileh.write(page.content)

    with config_file.open("w") as fileh:
        eobj = EnvGroup()
        output = []
        output.append("## Environment Variable Config Keys")
        for i in eobj.vals:
            header_val = ShortCode.hint_info(i["name"])
            output.append(f"{header_val}")
            output.append(i["doc"])
        page = hugo.Page("Configuration", "Configuration Options")
        page.weight = 2
        page.body = "\n".join(output)
        fileh.write(page.content)

    with v0tools_doc.GITHUB_README.open("w") as fileh:
        output = []
        output.append(badges.get_badges())
        output.append("")
        output.append(template.GITHUB_README.render(coll=dval))
        fileh.write("\n".join(output))

    with v0tools_doc.SITE_MAIN.open("w") as fileh:
        output = template.MAIN_README.render(coll=dval)
        page = hugo.Page("Home", "Welcome to v0tools!")
        exvals = "\n".join(
            [ShortCode.expand(txt, desc) for desc, txt in expand_vals.items()]
        )
        body = "\n".join(
            [
                badges.get_badges(),
                "{{< toc >}}",
                output,
                "",
                "## Quickstart / Install",
                exvals,
                "## Api",
                "> **API Documentation can be found [here](https://v0tools.stev0.me/api)**",
                "## Toc",
                "{{< toc-tree >}}",
            ]
        )
        page.body = body
        fileh.write(page.content)

    obj.write_content()
