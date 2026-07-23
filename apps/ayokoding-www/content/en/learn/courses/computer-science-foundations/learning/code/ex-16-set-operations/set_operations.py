# learning/code/ex-16-set-operations/set_operations.py
"""Example 16: Union/Intersection/Difference on Python Sets."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


if __name__ == "__main__":  # => co-09: entry point -- this block runs only when the file executes directly, not on import
    a: set[int] = {1, 2, 3, 4, 5}  # => co-09: set A -- a finite, unordered, duplicate-free collection
    b: set[int] = {4, 5, 6, 7}  # => co-09: set B -- overlaps A at exactly {4, 5}
    union = a | b  # => co-09: A ∪ B -- every element in EITHER set, with no duplicates
    intersection = a & b  # => co-09: A ∩ B -- only elements in BOTH sets
    difference = a - b  # => co-09: A \ B -- elements in A but explicitly NOT in B
    print(f"A = {sorted(a)}")  # => co-09: sorted() only for stable, readable printing -- sets are unordered
    print(f"B = {sorted(b)}")  # => co-09: same printing convention for B
    print(f"A | B (union) = {sorted(union)}")  # => co-09: prints the computed union
    print(f"A & B (intersection) = {sorted(intersection)}")  # => co-09: prints the computed intersection
    print(f"A - B (difference) = {sorted(difference)}")  # => co-09: prints the computed difference
    assert union == {1, 2, 3, 4, 5, 6, 7}, "union must contain every element from either set"  # => co-09
    assert intersection == {4, 5}, "intersection must contain only the shared elements"  # => co-09
    assert difference == {1, 2, 3}, "difference must contain only A's elements not also in B"  # => co-09
    print("All three operations match hand-computed results: True")  # => co-09: all three asserts passed
    # => co-09: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
