#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exception classes for v0tools."""
import os
from v0tools import ansi
from typing import List
from v0tools import syspkgs
from v0tools import Error, BadEnvConfig


class BinaryNotFound(Error):
    """BinaryNotFound Class.

    raises when a required binary is not found in the system PATH
    """

    MESSAGE = "command not found in PATH, adjust path or follow install instructions"
    """Default Message for BinaryNotFound."""

    def __init__(self, binary_path: str):
        """Return BinaryNotFound Object."""
        self.binary_path = binary_path
        """Binary that was not found."""

    @property
    def system_paths(self):
        """known paths separated by newlines."""
        return "\n".join(os.environ["PATH"].split(":"))

    def __str__(self):
        """String representation of BinaryNotFound."""
        pkg = syspkgs.COMMANDS[self.binary_path]
        return f"'{self.binary_path}' {BinaryNotFound.MESSAGE}\n{pkg.instruction}"


class MultiBinaryNotFound(Error):
    """Multiple Binaries not found.

    This exception throws on group check of binaries
    """

    def __init__(self, missing_bins: List):
        """Return BinaryNotFound Object."""
        self.bins = missing_bins
        """List of missing binaries."""

    def __str__(self):
        """String representation of MultiBinaryNotFound."""
        msg = [
            f'The following packages are not installed: {ansi.magenta(",".join(i.name for i in self.bins))}'
        ]
        msg.append(ansi.section("Install instructions"))
        for i in self.bins:
            msg.append(f"# {i.name}")
            msg.append(i.instruction)
        return "\n".join(msg)


class InvalidCliArgument(Error):
    """InvalidCliArgument Class."""

    MSG = "Invalid argument"
    """Default message for InvalidCliArgument."""

    def __init__(self, argument: str, msg=""):
        """Return InvalidCliArgument Object."""
        self.argument = argument
        """Argument having issues."""
        self.msg = msg
        """Passed message."""

    def __str__(self):
        """Returns exception message."""
        return f"{InvalidCliArgument.MSG} for {self.argument} {self.msg}"


class DirectoryNotExist(Error):
    """DirectoryNotExist Class."""

    def __init__(self, directory: str):
        """Return DirectoryNotExist Object."""
        self.directory = directory
        """Directory that doesn't exist."""

    def __str__(self):
        """Returns exception message."""
        return "Directory {self.directory} does not exist, or is not a directory"


class FileExists(Error):
    """FileExists Class."""

    MSG = "File exists"
    """Default message for FileExists."""

    def __init__(self, file: str, msg=""):
        """Return FileExists Object."""
        self.file = file
        """File in question."""

        self.msg = msg
        """Passed message."""

    def __str__(self):
        """Returns exception message."""
        return f"{FileExists.MSG} {self.file} {self.msg}"


class NoAction(Error):
    """NoAction Class."""

    MSG = ""
    """Default Message for NoAction"""

    def __init__(self, message):
        """Return NoAction Object."""

        self.message = message
        """Passed message."""

    def __str__(self):
        """Returns exception message."""
        return f"{NoAction.MSG} {self.message}"


class InvalidFileExtention(Error):
    """File has an invalid extension."""

    MSG = "has an invalid file extension"
    """Default message for InvalidFileExtention."""

    def __init__(self, passed_fn: str, valid_ext: List):
        """Return InvalidFileExtention Object."""
        self.passed_fn = passed_fn
        """Filename."""

        self.valid_ext = valid_ext
        """List of valid extensions."""

    def __str__(self):
        """String representation of InvalidFileExtention."""
        exts = ",".join(self.valid_ext)
        return (
            f"{self.passed_fn} {InvalidFileExtention.MSG}, valid extensions are {exts}"
        )


class InvalidIp(Error):
    """InvalidIp Class."""

    MSG = "Invalid IP Address"
    """Default message for InvalidIp."""

    def __init__(self, ip: str):
        """Return InvalidIp Object."""
        self.ip = ip
        """The Invalid IP Address."""

    def __str__(self):
        """Returns exception message."""
        return f"{InvalidIp.MSG} {self.ip}"
