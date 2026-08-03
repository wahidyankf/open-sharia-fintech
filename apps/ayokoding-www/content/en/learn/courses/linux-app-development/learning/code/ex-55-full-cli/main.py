"""Implement a complete small CLI with an explicit success contract."""

import argparse


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="notes")
    parser.add_argument("command", choices=["status"])
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args(argv)
    print('{"pending": 2}' if args.format == "json" else "pending=2")
    return 0


raise SystemExit(main(["status"]))
