#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Welcome to the v0tools python module."""
import os
import pathlib
import inspect


class Error(Exception):
    """Base exception class for v0tools."""


class BadEnvConfig(Error):
    """BadEnvConfig Class."""

    MSG = "Environment Variable is not set or has an error"
    """Default Message for BadEnvConfig"""

    def __init__(self, env_var: str, msg=""):
        """Return BadEnvConfig Object."""
        self.env_var = env_var
        """Missing / Invalid environment variable."""

        self.msg = msg
        """Additional message."""

    def __str__(self):
        """Returns exception message."""
        return f"{BadEnvConfig.MSG} {self.msg}"


class Config(object):
    """Config Environment Variables."""

    @staticmethod
    def get_val_throw_if_not_exist(name, msg, override):
        """Return env value if override is not default
        and throw BadEnvConfig if it's invalid or doesn't exist
        """
        if override == "__DEFAULT__":
            val = os.environ.get(name)
        else:
            val = override
        if not val:
            raise BadEnvConfig(msg)
        return val

    @staticmethod
    def V0_USER():
        """Default identifier on the victim machines Default: V0_Rando."""
        return os.environ.get("V0_USER", "V0_Rando")

    @staticmethod
    def V0_POWERSHELL_CONPTY(override="__DEFAULT__"):
        """Location of Invoke-ConPtyShell.ps1

        see: ::
            https://github.com/antonioCoco/ConPtyShell
        """
        name = Config.V0_POWERSHELL_CONPTY.__name__

        throw_msg = inspect.cleandoc(
            f"""
        Please set the environment Variable: {name} to point to file downloaded
        from url:

        https://github.com/antonioCoco/ConPtyShell
        """
        )
        return Config.get_val_throw_if_not_exist(name, throw_msg, override)

    @staticmethod
    def V0_VENOM_CACHE():
        """
        MSF Venom cache for autocomplete and functions
        Default ~/.msfvenom_cache.json
        """
        defpath = pathlib.Path("~/.msfvenom_cache.json").expanduser().resolve()
        return os.environ.get("V0_VENOM_CACHE", defpath)
