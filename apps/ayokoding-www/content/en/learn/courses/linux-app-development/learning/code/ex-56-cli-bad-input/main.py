"""Make invalid CLI input a stable stderr-and-exit-code contract."""

import argparse
import sys


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="notes", add_help=False)
    parser.add_argument("command", choices=["status"])
    try:
        parser.parse_args(argv)
    except SystemExit:
        print("notes: command must be status", file=sys.stderr)
        return 2
    print("pending=2")
    return 0


assert main(["unknown"]) == 2
