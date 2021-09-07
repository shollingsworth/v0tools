#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hugo helpers."""
import yaml
from datetime import datetime
import hashlib

r"""
# Set type to 'posts' if you want to render page as blogpost
type = "posts"

# Set page weight to re-arrange items in file-tree menu.
weight = 10

# Set how many table of contents levels to be showed on page.
geekdocToC = 3

# Set a description for the current page. This will be shown in toc-trees objects.
geekdocDescription =

# Set false to hide the whole left navigation sidebar. Beware that it will make
# navigation pretty hard without adding some kind of on-page navigation.
geekdocNav = true

# Show a breadcrumb navigation bar at the top of each docs page.
geekdocBreadcrumb = false

# Set source repository location.
geekdocRepo = "https://github.com/thegeeklab/hugo-geekdoc"

# Enable "Edit this page" links. Requires 'GeekdocRepo' param and path must point
# to 'content' directory of repo.
geekdocEditPath = "edit/main/exampleSite/content"

# Used for 'Edit this page' link, set to '.File.Path' by default.
# Can be overwritten by a path relative to 'geekdocEditPath'
geekdocFilePath =

# Set to mark page as flat section (file-tree menu only).
geekdocFlatSection = true

# Set true to hide page or section from side menu (file-tree menu only).
geekdocHidden = true

# Set false to show this page as a file-tree menu entry when you want it to be hidden in the sidebar.
# NOTE: Only applies when 'geekdocHidden = true'.
geekdocHiddenTocTree = true

# Set to true to make a section foldable in side menu.
geekdocCollapseSection = true

# Add an anchor link to headlines.
geekdocAnchor = true

# If you have protected some pages with e.g. basic authentication you may want to exclude these pages
# from data file, otherwise information may be leaked. Setting this parameter to 'true' will exclude the
# page from search data, feeds, etc.
# WARNING: Consider hosting a standalone, fully auth-protected static page for secret information instead!
geekdocProtected = false

# Set 'left' (default), 'center' or 'right' to configure the text align of a page.
geekdocAlign = "left"

"""


class Page(object):
    def __init__(self, title, description):
        self.weight = 99
        self.type = None  # type: str
        self.geekdocFlatSection = None  # type: bool
        self.geekdocCollapseSection = None  # type: bool
        self.geekdocAnchor = None  # type: bool
        self.geekdocProtected = None  # type: bool
        self.geekdocEditPath = None  # type: str
        self.geekdocRepo = None  # type: str
        self.geekdocToC = None  # type: int
        self.geekdocBreadcrumb = None  # type: bool
        self.geekdocNav = None  # type: bool
        self.geekdocHidden = None  # type: bool
        self.geekdocHiddenTocTree = None  # type: bool
        self.geekdocFilePath = None  # type: bool

        self.geekdocAlign = "left"
        self.title = title
        self.description = description
        self.geekdocDescription = description
        self.body = ""

    #  @property
    #  def date(self):
    #      return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    @property
    def content(self):
        hdict = {}
        for i in dir(self):
            if i.startswith("_"):
                continue
            if i in ["content", "body"]:
                continue
            aval = getattr(self, i)
            if callable(aval):
                continue
            if isinstance(aval, str):
                val = aval
                if not val:
                    val = None
            elif isinstance(aval, dict):
                val = aval
                if not val:
                    val = None
            else:
                try:
                    val = list(iter(aval))
                    if not val:
                        val = None
                except TypeError:
                    val = aval
            if val is None:
                continue
            hdict[i] = val
        dump_fmt = yaml.safe_dump(hdict)
        return f"""
---
{dump_fmt}
---

{self.body}
""".lstrip()


class Tab(object):
    def __init__(self):
        self.tabs = []

    def add_tab(self, tab_name: str, content: str):
        self.tabs.append(
            "\n".join(
                [
                    '{{< tab "__name__" >}}'.replace("__name__", tab_name),
                    content,
                    "{{< /tab >}}",
                ]
            )
        )

    @property
    def id(self):
        return hashlib.md5("".join(self.tabs).encode()).hexdigest()

    @property
    def content(self):
        ret = []
        ret.append('{{< tabs "__" >}}'.replace("__", self.id))
        ret.append("\n".join(self.tabs))
        ret.append("{{< /tabs >}}")
        return "\n".join(ret)


class ShortCode(object):
    @classmethod
    def _hint(cls, txt, hint_type: str):
        return "\n".join(
            [
                f"{{{{< hint {hint_type} >}}}}",
                txt,
                "{{< /hint >}}",
            ]
        )

    @classmethod
    def hint_ok(cls, txt):
        return cls._hint(txt, "ok")

    @classmethod
    def hint_info(cls, txt):
        return cls._hint(txt, "info")

    @classmethod
    def hint_warning(cls, txt):
        return cls._hint(txt, "warning")

    @classmethod
    def hint_danger(cls, txt):
        return cls._hint(txt, "danger")

    @classmethod
    def icon(cls, icon_name):
        return f"{{{{< icon {icon_name} >}}}}"

    @classmethod
    def button_relative(cls, txt, link):
        out = []
        out.append(f'{{{{< button relref="{link}" >}}}}')
        out.append(txt)
        out.append("{{< /button >}}")
        return "\n".join(out)

    @classmethod
    def button_external(cls, txt, link):
        out = []
        out.append(f'{{{{< button href="{link}" >}}}}')
        out.append(txt)
        out.append("{{< /button >}}")
        return "\n".join(out)

    @classmethod
    def expand(cls, content, label=None):
        out = []
        if label:
            out.append('{{< expand "__" "..." >}}'.replace("__", label))
        else:
            out.append("{{< expand >}}")
        out.append(content)
        out.append("{{< /expand >}}")
        return "\n".join(out)

    @classmethod
    def _video(cls, url: str, vid_type: str):
        txt = []
        standalone = " ".join(["controls"])
        attribs = " ".join(
            [
                f'{k}="{v}"'
                for k, v in {
                    "autoplay": "true",
                    "loop": "true",
                }.items()
            ]
        )
        txt.append('<div class="video-container">')
        txt.append(f"<video {standalone} {attribs}>")
        txt.append(f'<source src="{url}" type="video/{vid_type}">')
        txt.append("</video>")
        txt.append("</div>")
        return "\n".join(txt)

    @classmethod
    def webm(cls, url):
        return cls._video(url, "webm")

    @classmethod
    def mp4(cls, url):
        return cls._video(url, "mp4")

    @classmethod
    def code(cls, body, lang=""):
        txt = []
        txt.append("")
        txt.append(f"```{lang}")
        txt.append(body)
        txt.append("```")
        txt.append("")
        return "\n".join(txt)

    @classmethod
    def quote_bold(cls, txt: str):
        return "\n".join([f"> **{i}**" if i else "> " for i in txt.splitlines()])

    @classmethod
    def quote(cls, txt: str):
        return "\n".join([f"> {i}" if i else "> " for i in txt.splitlines()])
