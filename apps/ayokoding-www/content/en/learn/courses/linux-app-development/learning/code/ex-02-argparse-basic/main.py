"""Parse one required argument."""

import argparse

parser = argparse.ArgumentParser(prog="notes")
parser.add_argument("title")
print(parser.parse_args(["standup"]).title)
