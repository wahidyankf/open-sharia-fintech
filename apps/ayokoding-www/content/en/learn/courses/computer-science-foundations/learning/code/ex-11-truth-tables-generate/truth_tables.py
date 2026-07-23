# learning/code/ex-11-truth-tables-generate/truth_tables.py
"""Example 11: Generating AND/OR/XOR Truth Tables Programmatically."""  # => co-07: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-07: itertools.product enumerates every input combination -- the definition of a truth table
from collections.abc import Callable  # => co-06: typing the gate functions passed into the generator below

Gate = Callable[[bool, bool], bool]  # => co-06: every gate below has this exact two-input, one-output shape

GATES: dict[str, Gate] = {  # => co-06: the three boolean-algebra operators this example tables
    "AND": lambda a, b: a and b,  # => co-06: True only when BOTH inputs are True
    "OR": lambda a, b: a or b,  # => co-06: True when AT LEAST ONE input is True
    "XOR": lambda a, b: a != b,  # => co-06: True when the inputs DIFFER -- the "derived" gate the concept names
}  # => co-06: closes the multi-line construct opened above


def truth_table(gate: Gate) -> list[tuple[bool, bool, bool]]:  # => co-07: one row per input combination
    """Enumerate every (a, b, gate(a, b)) row -- a truth table, mechanically generated."""  # => co-07: documents truth_table's contract -- no runtime output, just sets its __doc__
    return [(a, b, gate(a, b)) for a, b in itertools.product([False, True], repeat=2)]  # => co-07: all 4 rows


if __name__ == "__main__":  # => co-07: entry point -- this block runs only when the file executes directly, not on import
    for name, gate in GATES.items():  # => co-06: one full table per gate, in AND/OR/XOR order
        print(f"{name} truth table:")  # => co-06: labels which gate the following rows belong to
        rows = truth_table(gate)  # => co-07: 4 rows: (F,F), (F,T), (T,F), (T,T) with each gate's output
        for a, b, result in rows:  # => co-07: prints and cross-checks EVERY row against the gate function
            print(f"  {int(a)} {int(b)} -> {int(result)}")  # => co-07: printed as 0/1, the conventional notation
            assert result == gate(a, b), "each printed row must match the gate it was generated from"  # => co-07
    and_rows = truth_table(GATES["AND"])  # => co-06: spot-check AND's defining row directly
    assert and_rows[-1] == (True, True, True), "AND(True, True) must be True"  # => co-06: the only True row
    xor_rows = truth_table(GATES["XOR"])  # => co-06: spot-check XOR's defining property
    assert xor_rows[0] == (False, False, False) and xor_rows[-1] == (True, True, False)  # => co-06: same->False
    print("All rows verified against their generating gate: True")  # => co-06: every assert above passed
    # => co-06: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
