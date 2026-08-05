"""Parse an optional flag with a useful default."""

import argparse

parser = argparse.ArgumentParser(prog="notes")
parser.add_argument("--format", choices=["text", "json"], default="text")
print(parser.parse_args(["--format", "json"]).format)
