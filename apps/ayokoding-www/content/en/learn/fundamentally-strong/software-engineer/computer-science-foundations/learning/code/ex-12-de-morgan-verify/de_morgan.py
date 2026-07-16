# learning/code/ex-12-de-morgan-verify/de_morgan.py
"""Example 12: Verifying De Morgan's Law -- not(a and b) == (not a or not b)."""  # => co-06: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import itertools  # => co-06: enumerates all 4 (a, b) input pairs -- an exhaustive proof, not a spot check


def de_morgan_holds(a: bool, b: bool) -> bool:  # => co-06: one side of De Morgan's law, checked against the other
    """Check De Morgan's law for one (a, b) pair: not(a and b) == (not a or not b)."""  # => co-06: documents de_morgan_holds's contract -- no runtime output, just sets its __doc__
    left = not (a and b)  # => co-06: negation OUTSIDE the conjunction
    right = (not a) or (not b)  # => co-06: negation INSIDE, conjunction rewritten as disjunction
    return left == right  # => co-06: De Morgan's law claims these are ALWAYS equal


if __name__ == "__main__":  # => co-06: entry point -- this block runs only when the file executes directly, not on import
    rows: list[tuple[bool, bool, bool]] = []  # => co-06: (a, b, holds) for every input combination
    for a, b in itertools.product([False, True], repeat=2):  # => co-06: all 4 combinations -- exhaustive
        holds = de_morgan_holds(a, b)  # => co-06: True/False row for this specific (a, b) pair
        rows.append((a, b, holds))  # => co-06: recorded for the final summary print
        print(f"a={int(a)} b={int(b)} -> not(a and b) == (not a or not b): {holds}")  # => co-06: per-row result
    all_true = all(holds for _, _, holds in rows)  # => co-06: the law must hold on EVERY row to be a law
    assert all_true, "De Morgan's law must hold for all four input combinations"  # => co-06: the actual proof
    assert len(rows) == 4, "must have checked exactly all 4 boolean combinations"  # => co-06: exhaustiveness check
    print(f"All four rows True: {all_true}")  # => co-06: reached only if the law held everywhere
    # => co-06: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
