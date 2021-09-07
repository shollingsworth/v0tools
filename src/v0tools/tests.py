#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit test helpers."""
import subprocess
import unittest

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
