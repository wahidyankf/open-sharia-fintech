# learning/code/ex-18-implication-truth-table/implication_truth_table.py
"""Example 18: The Implication Truth Table -- p -> q."""  # => co-10: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-10: enumerates all 4 (p, q) pairs -- the full implication truth table


def implies(p: bool, q: bool) -> bool:  # => co-10: material implication -- False ONLY when p is True, q is False
    """p -> q, using the standard logical-implication definition: (not p) or q."""  # => co-10: documents implies's contract -- no runtime output, just sets its __doc__
    return (not p) or q  # => co-10: "if p then q" is FALSE only in the one case p holds but q doesn't


if __name__ == "__main__":  # => co-10: entry point -- this block runs only when the file executes directly, not on import
    rows: list[tuple[bool, bool, bool]] = []  # => co-10: (p, q, p->q) for every combination
    for p, q in itertools.product([False, True], repeat=2):  # => co-10: all 4 combinations, exhaustive
        result = implies(p, q)  # => co-10: this pair's implication value
        rows.append((p, q, result))  # => co-10: recorded for the final False-count check
        print(f"p={int(p)} q={int(q)} -> p->q = {int(result)}")  # => co-10: per-row printed result
    false_rows = [(p, q) for p, q, result in rows if not result]  # => co-10: which rows evaluated to False
    print(f"False rows: {false_rows}")  # => co-10: expect exactly [(True, False)]
    assert false_rows == [(True, False)], "only (p=True, q=False) may make p->q False"  # => co-10: the one case
    assert len(false_rows) == 1, "exactly one of the four rows must be False"  # => co-10: exhaustiveness check
    print("Only (True, False) is False: True")  # => co-10: reached only if both asserts above passed
    # => co-10: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
