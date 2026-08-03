"""Expose argparse's real --help contract."""

import argparse

parser = argparse.ArgumentParser(prog="notes-linux", description="Read a local note")
parser.add_argument("note", nargs="?")
try:
    parser.parse_args(["--help"])
except SystemExit as error:
    assert error.code == 0
