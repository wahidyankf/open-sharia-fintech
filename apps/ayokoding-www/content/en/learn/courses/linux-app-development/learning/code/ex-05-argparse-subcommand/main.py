"""Dispatch an argparse subcommand."""

import argparse

parser = argparse.ArgumentParser(prog="notes")
commands = parser.add_subparsers(dest="command", required=True)
commands.add_parser("status")
print(parser.parse_args(["status"]).command)
