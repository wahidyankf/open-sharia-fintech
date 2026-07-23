"""Kata 10 (after): fix -- the core stays pure; only the shell performs I/O, and only around the core."""

import io
from contextlib import redirect_stdout


def parse_and_total(
    rows: list[str],
) -> int:  # => the pure core -- no print, no I/O of any kind
    return sum(int(row) for row in rows)


def run_shell(
    rows: list[str],
) -> None:  # => the imperative shell -- the ONLY place logging happens
    print(f"parsing {len(rows)} rows")
    total = parse_and_total(rows)
    print(total)


rows = ["10", "20", "30"]
captured = io.StringIO()
with redirect_stdout(captured):
    total = parse_and_total(
        rows
    )  # calling the core directly needs NO stdout redirection to test
print(total)
print(
    repr(captured.getvalue())
)  # empty -- the core performed no I/O, confirming it stayed pure
run_shell(
    rows
)  # the shell is where logging + the final print belong -- the core stays silent
