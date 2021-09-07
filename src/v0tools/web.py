#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTB."""
from urllib import parse
import requests
from requests.auth import HTTPBasicAuth
from html2text import html2text
from base64 import b64decode, b64encode
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

HEADER_URL_ENCODED = {
    "Content-Type": "application/x-www-form-urlencoded",
}
"""URL Encoded Header."""


class Webber(object):
    """Helper class for making http reqests to a remote."""

    def __init__(self, debug=False):
        """Return Webber Object."""
        self.session = requests.Session()
        """requests.Session object."""
        self.debug = debug
        """Debug Flag (be verbose)."""

    def set_cookie(self, key, value):
        """Set cookie."""
        self.session.cookies.set(key, value)

    def get(self, url):
        """Simple http get request."""
        return self.session.get(url)

    def get_json(self, url: str, json_param: dict):
        """simple get request with json input send as encoded params."""
        send = parse.urlencode(json_param)
        url = f"{url}?{send}"
        return self.session.get(url)

    def post_form_urlencoded_json(self, url: str, json_param: dict):
        """Post with HEADER_URL_ENCODED header and dict passed as argument."""
        send = parse.urlencode(json_param)
        return self.session.post(url, headers=HEADER_URL_ENCODED, data=send)

    def post_json(self, url: str, json_param: dict):
        """Post with default JSON content encoding."""
        return self.session.post(url, json=json_param)
