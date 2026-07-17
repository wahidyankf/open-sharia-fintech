"""Kata 10 (before): a debug print() leaks I/O into what is supposed to be the pure core."""

import io
from contextlib import redirect_stdout


def parse_and_total(
    rows: list[str],
) -> int:  # meant to be the PURE core -- no I/O anywhere
    print(
        f"parsing {len(rows)} rows"
    )  # SMELL: a debug print buried inside the "pure" core
    return sum(int(row) for row in rows)


rows = ["10", "20", "30"]
captured = io.StringIO()
with redirect_stdout(
    captured
):  # BUG: a "pure" function should never need its stdout redirected
    total = parse_and_total(rows)
print(total)
print(
    repr(captured.getvalue())
)  # BUG: proves the core actually performed I/O -- it isn't pure
