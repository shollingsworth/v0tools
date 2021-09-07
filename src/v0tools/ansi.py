#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ansi colors."""


class Ansi:
    """Ansi color class."""

    MAGENTA = "\033[95m"
    """Light Magenta."""

    OKBLUE = "\033[94m"
    """Light Blue."""

    OKCYAN = "\033[96m"
    """Light Cyan."""

    OKGREEN = "\033[92m"
    """Light Green."""

    WARNING = "\033[93m"
    """Light Yellow."""

    FAIL = "\033[91m"
    """Light Red."""

    ENDC = "\033[0m"
    """End Ansi block."""

    BOLD = "\033[1m"
    """Make value Bold."""

    UNDERLINE = "\033[4m"
    """Make Value Underline."""


def green(txt):
    """Return Green Ansi string."""
    return "".join([Ansi.OKGREEN, txt, Ansi.ENDC])


def blue(txt):
    """Return Blue Ansi string."""
    return "".join([Ansi.OKBLUE, txt, Ansi.ENDC])


def red(txt):
    """Return Red Ansi String."""
    return "".join([Ansi.FAIL, txt, Ansi.ENDC])


def magenta(txt):
    """Return Header / Light Magenta."""
    return "".join([Ansi.MAGENTA, txt, Ansi.ENDC])


def banner(txt):
    """Ansi Banner in Magenta."""
    return "\n".join(
        [
            magenta("-" * 50),
            magenta(txt),
            magenta("-" * 50),
        ]
    )


def section(txt):
    """Ansi Section in Green."""
    return "\n".join(
        [
            green("=" * 40),
            green(txt),
            green("=" * 40),
        ]
    )
