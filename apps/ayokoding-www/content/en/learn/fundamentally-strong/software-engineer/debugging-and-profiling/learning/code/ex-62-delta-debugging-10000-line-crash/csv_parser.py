"""Example 62: a CSV-like parser that crashes on one specific malformed row,
buried among 10,000 lines of otherwise-valid input.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the crash itself


def parse_lines(
    lines: list[str],
) -> list[list[str]]:  # => co-11: the ONE function ddmin_lines.py will minimize against
    rows: list[
        list[str]
    ] = []  # => co-11: accumulates every SUCCESSFULLY parsed row before the crash
    for line in lines:  # => co-11: iterates every input line -- the crashing row can be ANYWHERE in here
        fields = line.split(
            ","
        )  # => co-11: a naive split -- no quoting/escaping, deliberately simple
        # co-11: the real bug -- a row with an EMPTY third field crashes when
        # something downstream tries int(fields[2]) on it.
        rows.append(
            [fields[0], fields[1], str(int(fields[2]))]
        )  # => co-11: int('') raises ValueError -- the crash site
    return rows  # => co-11: never reached on the crashing input -- the exception propagates up first
