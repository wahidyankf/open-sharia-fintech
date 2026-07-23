"""Capstone -- Imperative Shell: reads a transaction CSV file and prints the report.

Exercises co-28's OTHER half: main() is the ONLY function in this whole capstone that performs
I/O (reading a file, writing to stdout/stderr). Every actual computation -- parsing, validating,
aggregating, formatting -- is delegated straight to core.py's pure functions; this file holds no
transformation logic of its own at all.
"""

from __future__ import annotations

import sys  # => sys.argv (read) and sys.exit (write the process exit code) -- both I/O boundaries
from pathlib import (
    Path,
)  # => Path.read_text() is this shell's ONE file-reading I/O boundary

from core import (
    Err,
    analyze,
    format_report,
)  # => everything computational comes from the pure core


def main(
    argv: list[str],
) -> int:  # => the IMPERATIVE SHELL entry point -- the ONLY place with I/O
    if (
        len(argv) != 1
    ):  # => a tiny bit of shell-level argument handling, still not "business logic"
        print(
            "usage: shell.py <transactions.csv>", file=sys.stderr
        )  # => I/O boundary: stderr
        return 2  # => a non-zero exit code signals misuse to the calling shell/CI
    path = Path(
        argv[0]
    )  # => resolves the CLI argument into a filesystem path -- no read yet
    csv_text = (
        path.read_text()
    )  # => I/O boundary: the ONE file read in this entire capstone
    result = analyze(
        csv_text
    )  # => delegates EVERYTHING else to the pure core -- zero logic here
    if isinstance(
        result, Err
    ):  # => malformed input: report every collected error, do NOT crash
        print(f"{len(result.error)} error(s) found:")  # => I/O boundary: stdout
        for (
            message
        ) in result.error:  # => walks EVERY accumulated error, not just the first
            print(f"  {message}")  # => one printed line per malformed input row
        return 1  # => a non-zero exit code signals "input had errors" to the calling shell/CI
    print(
        format_report(result.value)
    )  # => I/O boundary: prints the pure core's own report string
    return 0  # => success


if (
    __name__ == "__main__"
):  # => only runs when invoked directly, e.g. `python3 shell.py sample.csv`
    sys.exit(
        main(sys.argv[1:])
    )  # => argv[0] is the script name itself -- argv[1:] is the real arguments
