"""Example 29: a toy CLI with a real argparse flag whose semantics an injected filename can trigger (co-04)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the argument-injection itself

import argparse  # => co-04: stdlib CLI parser -- argv[1] can be read as EITHER a flag or a positional
import sys  # => co-04: sys.argv is what a naive caller mistakenly treats as "just a filename"

SECRET_CONFIG = "DB_PASSWORD=hunter2-internal-only"  # => co-07: sensitive data --dump-config was never meant to expose


def main() -> (
    int
):  # => co-04: mirrors a real CLI's entry point -- exit code, not an exception, signals failure
    parser = argparse.ArgumentParser(
        prog="file_reader"
    )  # => co-04: a REAL argparse CLI, like tar/git/rsync have
    parser.add_argument(
        "filename", nargs="?", default=""
    )  # => co-04: intended positional -- optional so a lone flag still parses
    parser.add_argument(
        "--dump-config", action="store_true"
    )  # => co-04: a REAL existing flag -- ops/debug tooling
    args = (
        parser.parse_args()
    )  # => co-04: argparse decides flag-vs-positional from the LEADING "-", not intent
    # => co-07: nothing here validated WHERE "--dump-config" came from -- a wrapper's
    # => naive argv-building is indistinguishable from a legitimate operator's own flag
    if (
        args.dump_config
    ):  # => co-07: this branch fires whenever argv contained "--dump-config" ANYWHERE
        print(
            f"internal config dump: {SECRET_CONFIG}"
        )  # => co-07: the unintended behavior an injected flag reaches
        return 0  # => co-04: success exit code -- the caller has no way to tell this branch ran unexpectedly
    try:  # => co-04: the INTENDED behavior -- just read the named file
        with open(
            args.filename
        ) as f:  # => co-04: args.filename is whatever positional argparse assigned
            print(
                f.read()
            )  # => co-04: prints the file's real contents, the normal/expected path
    except (
        FileNotFoundError
    ):  # => co-04: the expected failure mode for a bogus filename
        print(
            f"file not found: {args.filename}"
        )  # => co-04: a plain, generic message -- no secret involved
    return (
        0  # => co-04: still a clean exit -- "not found" is not a CLI-level error here
    )


if (
    __name__ == "__main__"
):  # => co-04: only runs when invoked as a real subprocess, e.g. `python3 file_reader.py ...`
    sys.exit(
        main()
    )  # => co-04: propagates main()'s return code as this process's real exit status
