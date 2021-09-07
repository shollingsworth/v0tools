#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import v0tools_doc
import v0tools_doc.template as template
from v0tools.syspkgs import get_install_instructions
from v0tools_doc import cli, EnvGroup
from v0tools_doc.hugo import ShortCode
from v0tools_doc import hugo
from pathlib import Path
import shutil


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

    config_dir = v0tools_doc.CONTENT_DIR.joinpath("configuration")
    config_dir.exists() or config_dir.mkdir()
    config_file = config_dir.joinpath("_index.md")

    inst_dir = v0tools_doc.CONTENT_DIR.joinpath("sys_prerequisites")
    inst_dir.exists() or inst_dir.mkdir()
    inst_file = inst_dir.joinpath("_index.md")

    with inst_file.open("w") as fileh:
        output = []
        output.append("## System Install Prerequisites")
        output.append("{{< toc-tree >}}")
        page = hugo.Page("System Install Prerequisites", "System Install Prerequisites")
        page.weight = 5
        page.body = "\n".join(output)
        fileh.write(page.content)

    for dist, instructions in get_install_instructions().items():
        fpath = inst_dir.joinpath(f"{dist}.md")
        txt = []
        # txt.append(f"# {dist.capitalize()}")
        txt.append(ShortCode.code(instructions, "bash"))
        with fpath.open("w") as fileh:
            fileh.write("\n".join(txt))

    with config_file.open("w") as fileh:
        eobj = EnvGroup()
        output = []
        output.append("## Environment Variable Configuration Values")
        for i in eobj.vals:
            header_val = ShortCode.hint_info(i["name"])
            output.append(f"{header_val}")
            output.append(i["doc"])
        page = hugo.Page("Configuration", "Configuration Options")
        page.weight = 2
        page.body = "\n".join(output)
        fileh.write(page.content)

    with v0tools_doc.GITHUB_README.open("w") as fileh:
        output = template.GITHUB_README.render(coll=dval)
        fileh.write(output)

    with v0tools_doc.SITE_MAIN.open("w") as fileh:
        output = template.MAIN_README.render(coll=dval)
        page = hugo.Page("Home", "Welcome to v0tools!")
        body = "\n".join(
            [
                "{{< toc >}}",
                output,
                "",
                "## Toc",
                "{{< toc-tree >}}",
            ]
        )
        page.body = body
        fileh.write(page.content)

    obj.write_content()
