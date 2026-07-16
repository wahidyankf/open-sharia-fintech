# learning/code/ex-02-base-roundtrip/base_roundtrip.py
"""Example 2: Base Round-Trip -- bin/hex/int(s, base) Agree."""  # => co-01: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from typing import NamedTuple  # => co-01: a typed record beats a bare tuple for the per-base report


class BaseView(NamedTuple):  # => co-01: one row per base this value is rendered in
    base_name: str  # => human-readable base label ("binary", "hex", "octal")
    literal: str  # => co-01: the string Python's own builtin produced for this base
    round_tripped: int  # => co-01: literal parsed BACK to int via int(s, base) -- must equal the original


def round_trip(value: int) -> list[BaseView]:  # => co-01: builds one BaseView per base, in a fixed order
    """Render `value` in binary/octal/hex and parse each back with int(s, base)."""  # => co-01: documents round_trip's contract -- no runtime output, just sets its __doc__
    views: list[BaseView] = []  # => co-01: accumulates the three rows this function returns
    for name, literal in (  # => co-01: (label, Python's own builtin literal, prefix included)
        ("binary", bin(value)),  # => co-01: e.g. "0b10011100"
        ("octal", oct(value)),  # => co-01: e.g. "0o234"
        ("hex", hex(value)),  # => co-01: e.g. "0x9c"
    ):  # => co-01: closes the multi-line construct opened above
        base = {"binary": 2, "octal": 8, "hex": 16}[name]  # => co-01: numeric base matching this literal
        round_tripped = int(literal, base)  # => co-01: int() parses the FULL literal, prefix included
        views.append(BaseView(name, literal, round_tripped))  # => co-01: one completed row
    return views  # => co-01: returns this computed value to the caller


if __name__ == "__main__":  # => co-01: entry point -- this block runs only when the file executes directly, not on import
    value = 156  # => co-01: same test value as Example 1, for continuity
    for view in round_trip(value):  # => co-01: one printed line per base
        print(f"{view.base_name:<7} {view.literal:<12} -> int(..) = {view.round_tripped}")  # => co-01
        assert view.round_tripped == value, f"{view.base_name} round-trip must equal {value}"  # => co-01
    print(f"All three bases round-trip to {value}: True")  # => co-01: reached only if every assert passed
    # => co-01: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
