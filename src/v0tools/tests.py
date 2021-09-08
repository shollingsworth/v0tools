#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit test helpers."""
from types import ModuleType
import contextlib
import sys
from io import StringIO
from pathlib import Path
from v0tools.cli import Cli
import subprocess
import unittest

BASE = Path(__file__).parent.parent.parent.resolve()
"""Base Path."""
sys.path.append(str(BASE.joinpath("bin")))

# Stolen from https://raw.githubusercontent.com/lacostej/unity3d-bash-completion/master/lib/completion.py
# inspired from http://stackoverflow.com/questions/9137245/unit-test-for-bash-completion-script
# Modified / Fixed some behaviour Steven Hollingsworth

COMP_WORDBREAKS = [
    " ",
    "\t",
    "\n",
    '"',
    "'",
    ">",
    "<",
    "=",
    ";",
    "|",
    "&",
    "(",
    ":",
    "\n",
]
"""Bash Autocomplete COMP_WORDBREAKS content."""


def split_wordbreak(command):
    """Split Bash Autcomplete by wordbreak."""
    vals = []
    for letter in command:
        if letter in COMP_WORDBREAKS:
            vals.append(" ")
            vals.append(letter)
            vals.append(" ")
        else:
            vals.append(letter)
    comp_line = "".join(vals).split()
    return " ".join(comp_line), len(comp_line) - 1


class Completion:
    """Bash Completion test class."""

    def prepare(self, program, command):
        """Prepare the command."""
        self.program = program
        """Base Completer program."""

        self.COMP_LINE = "%s %s" % (program, command)
        """Raw Complete Line."""

        self.COMP_POINT = len(self.COMP_LINE)
        """Word complete Length."""

        _ = split_wordbreak(self.COMP_LINE)
        self.COMP_WORDS = _[0]
        """WORD Split."""
        self.COMP_CWORD = _[1]
        """Split Word Count."""

        if self.COMP_LINE[-1] == " ":
            self.COMP_WORDS += " "
            self.COMP_CWORD += 1

    def run(self, completion_file, program, command):
        """Run the test."""
        self.prepare(program, command)
        # Leave these in for debuggin
        #  print("COMP_LINE", self.COMP_LINE)
        #  print("COMP_WORDS", self.COMP_WORDS)
        #  print("COMP_POINT", self.COMP_POINT)
        #  print("COMP_CWORD", self.COMP_CWORD)
        full_cmdline = r'source {compfile}; COMP_LINE="{COMP_LINE}" COMP_WORDS=({COMP_WORDS}) COMP_CWORD={COMP_CWORD} COMP_POINT={COMP_POINT}; $(complete -p {program} | sed "s/.*-F \\([^ ]*\\) .*/\\1/") && echo ${{COMPREPLY[*]}}'.format(
            compfile=completion_file,
            COMP_LINE=self.COMP_LINE,
            COMP_WORDS=self.COMP_WORDS,
            COMP_POINT=self.COMP_POINT,
            program=self.program,
            COMP_CWORD=self.COMP_CWORD,
        )
        out = subprocess.Popen(
            ["bash", "-i", "-c", full_cmdline], stdout=subprocess.PIPE
        )
        return out.communicate()


class BashCompletionTest(unittest.TestCase):
    """Bash Completion Test class."""

    def run_complete(self, completion_file, program, command, expected):
        """Run the complete command."""
        stdout, _ = Completion().run(completion_file, program, command)
        should = expected + "\n"
        self.assertEqual(stdout, should.encode())


class CliRun(object):
    """Run the program and capture the output."""

    def __init__(self, script_name: str):
        """Initialize CliRun object."""
        name = script_name.rstrip(".py")
        self.mod = __import__(name)
        """cli module."""
        self.cli = self.mod.cli  # type: Cli
        """cli object."""

    def run(self, inp_args: str):
        """Run with no testing."""
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = self.cli.get_parse(inp_args)
            self.cli.run_nocatch(args)
            output = buf.getvalue()
        return output


class CliTest(unittest.TestCase):
    """Cli Test Class."""

    SCRIPT_NAME = ""
    """Base script name."""

    def init(self):
        """Setup module and variables."""
        if not self.SCRIPT_NAME:
            raise RuntimeError("Class SCRIPT_NAME not set")
        name = self.SCRIPT_NAME.rstrip(".py")
        self.mod = __import__(name)
        """cli module."""
        self.cli = self.mod.cli  # type: Cli
        """cli object."""

    def run_cli(self, inp_args: str):
        """Run with no testing."""
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = self.cli.get_parse(inp_args)
            self.cli.run_nocatch(args)
            output = buf.getvalue()
        return output

    def match_txt_in_output(self, inp_args: str, match_str: str):
        """Match string in output."""
        output = self.run_cli(inp_args)
        self.assertIn(match_str, output)

    def match_lines_in_output(self, inp_args: str, match_lines: list):
        """Match string in output."""
        output = self.run_cli(inp_args)
        lines = output.splitlines()
        matches = [i for i in match_lines if i in lines]
        self.assertEqual(len(matches), len(match_lines))

    def match_zero_exit_code(self, inp_args: str, match_str: str):
        """Match string in zero exit coded program."""
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            with self.assertRaises(SystemExit) as err:
                args = self.cli.get_parse(inp_args)
                print(args)
            self.assertEqual(err.exception.code, 0)  # exits ok
            output = buf.getvalue()
        self.assertIn(match_str, output)

    def exception_raises(self, inp_args: str, exception):
        """Test if certain exception raised."""
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            args = self.cli.get_parse(inp_args)
            self.assertRaises(exception, self.cli.run_nocatch, args)

    def exception_raises_with_regex(self, inp_args: str, exception, regex: str):
        """Checked raised exception and regex match."""
        args = self.cli.get_parse(inp_args)
        with StringIO() as buf, contextlib.redirect_stdout(buf):
            self.assertRaisesRegex(exception, regex, self.cli.run_nocatch, args)
