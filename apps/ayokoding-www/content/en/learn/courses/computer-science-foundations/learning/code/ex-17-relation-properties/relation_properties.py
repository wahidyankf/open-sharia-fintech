# learning/code/ex-17-relation-properties/relation_properties.py
"""Example 17: Classifying a Relation -- Reflexive, Symmetric, Transitive."""  # => co-09: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def is_reflexive(domain: set[int], relation: set[tuple[int, int]]) -> bool:  # => co-09: every x relates to itself
    """True iff (x, x) is in the relation for every x in the domain."""  # => co-09: documents is_reflexive's contract -- no runtime output, just sets its __doc__
    return all((x, x) in relation for x in domain)  # => co-09: checked for EVERY domain element, not a sample


def is_symmetric(relation: set[tuple[int, int]]) -> bool:  # => co-09: (x,y) in R implies (y,x) in R
    """True iff (a, b) in the relation implies (b, a) is too, for every pair."""  # => co-09: documents is_symmetric's contract -- no runtime output, just sets its __doc__
    return all((b, a) in relation for a, b in relation)  # => co-09: checked for every existing pair


def is_transitive(relation: set[tuple[int, int]]) -> bool:  # => co-09: (x,y) and (y,z) in R implies (x,z) in R
    """True iff (a, b) and (b, c) in the relation implies (a, c) is too."""  # => co-09: documents is_transitive's contract -- no runtime output, just sets its __doc__
    for a, b in relation:  # => co-09: for every pair sharing a "middle" element...
        for c, d in relation:  # => co-09: ...paired against every other relation entry
            if b == c and (a, d) not in relation:  # => co-09: chain a->b->d found, but a->d missing
                return False  # => co-09: the SINGLE counterexample that disproves transitivity
    return True  # => co-09: no counterexample found across the full double loop


if __name__ == "__main__":  # => co-09: entry point -- this block runs only when the file executes directly, not on import
    domain: set[int] = {1, 2, 3}  # => co-09: the small finite domain this relation is defined over
    # "divides" restricted to {1,2,3}: 1|1, 1|2, 1|3, 2|2, 3|3 -- a KNOWN reflexive, transitive, non-symmetric case
    divides: set[tuple[int, int]] = {(1, 1), (1, 2), (1, 3), (2, 2), (3, 3)}  # => co-09: "a divides b" pairs
    reflexive = is_reflexive(domain, divides)  # => co-09: expect True -- (1,1),(2,2),(3,3) all present
    symmetric = is_symmetric(divides)  # => co-09: expect False -- (1,2) present but (2,1) is not
    transitive = is_transitive(divides)  # => co-09: expect True -- "divides" is always transitive
    print(f"relation = {sorted(divides)}")  # => co-09: prints the relation under test
    print(f"reflexive={reflexive} symmetric={symmetric} transitive={transitive}")  # => co-09: the three flags
    assert reflexive is True, "'divides' on {1,2,3} must be reflexive"  # => co-09
    assert symmetric is False, "'divides' on {1,2,3} must NOT be symmetric (1|2 but not 2|1)"  # => co-09
    assert transitive is True, "'divides' on {1,2,3} must be transitive"  # => co-09
    print("All three property flags match the known classification: True")  # => co-09: all three asserts passed
    # => co-09: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
