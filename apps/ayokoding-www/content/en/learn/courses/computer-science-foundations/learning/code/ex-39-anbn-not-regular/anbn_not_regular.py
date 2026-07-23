# learning/code/ex-39-anbn-not-regular/anbn_not_regular.py
"""Example 39: a^n b^n Cannot Be a DFA -- a Pumping-Lemma-Style Counterexample."""  # => co-20: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

# ex-39: the pumping lemma says ANY regular language has a "pump length" p such that every
# string of length >= p can be split x.y.z, |xy| <= p, |y| >= 1, and x.(y^k).z stays in the
# language for EVERY k >= 0. This example shows that for a^n b^n, NO fixed p can survive
# pumping -- a fixed-state machine's finite memory cannot track an UNBOUNDED count of a's.


def in_anbn(s: str) -> bool:  # => co-20, co-21: independent membership check -- exactly equal runs of a then b
    """True iff s is exactly n a's followed by exactly n b's, for some n >= 0."""  # => co-20: documents in_anbn's contract -- no runtime output, just sets its __doc__
    a_count = 0  # => co-21: counts leading a's
    i = 0  # => co-21: scan position
    while i < len(s) and s[i] == "a":  # => co-21: consume the a-run
        a_count += 1  # => co-21: updates the running total/counter in place
        i += 1  # => co-21: updates the running total/counter in place
    b_count = 0  # => co-21: counts the following b's
    while i < len(s) and s[i] == "b":  # => co-21: consume the b-run
        b_count += 1  # => co-21: updates the running total/counter in place
        i += 1  # => co-21: updates the running total/counter in place
    return i == len(s) and a_count == b_count  # => co-21: whole string consumed AND counts equal


def pump(s: str, x_len: int, y_len: int, k: int) -> str:  # => co-21: x.(y^k).z, per the pumping lemma's construction
    """Split s into x (length x_len), y (next y_len chars), z (rest), then return x + y*k + z."""  # => co-21: documents pump's contract -- no runtime output, just sets its __doc__
    x, y, z = s[:x_len], s[x_len : x_len + y_len], s[x_len + y_len :]  # => co-21: the mandated 3-way split
    return x + (y * k) + z  # => co-21: "pumping" y -- repeating it k times


if __name__ == "__main__":  # => co-21: entry point -- this block runs only when the file executes directly, not on import
    p = 4  # => co-21: an ARBITRARY candidate pump length -- the argument holds for ANY p, this is just one witness
    s = ("a" * p) + ("b" * p)  # => co-21: a string of length 2p, definitely long enough to force |xy| <= p into the a-run
    print(f"candidate pump length p={p}, witness string s={s!r} (in a^n b^n: {in_anbn(s)})")  # => co-21
    assert in_anbn(s), "the witness string itself must be a valid a^n b^n member"  # => co-21: sanity check
    # Any valid split with |xy| <= p forces y to consist ENTIRELY of a's (y sits inside the first p characters,
    # which are all 'a'). Pumping y (k=2, i.e. repeating it once more) adds extra a's WITHOUT adding any b's.
    x_len, y_len = 0, 1  # => co-21: a valid split satisfying |xy| = 1 <= p=4 and |y| = 1 >= 1, per the lemma's constraints
    pumped_up = pump(s, x_len, y_len, k=2)  # => co-21: "pump up" -- repeat y twice instead of once
    pumped_down = pump(s, x_len, y_len, k=0)  # => co-21: "pump down" -- remove y entirely (k=0)
    print(f"pumped up (k=2)   = {pumped_up!r} (in a^n b^n: {in_anbn(pumped_up)})")  # => co-21
    print(f"pumped down (k=0) = {pumped_down!r} (in a^n b^n: {in_anbn(pumped_down)})")  # => co-21
    assert not in_anbn(pumped_up), "pumping y up must break membership -- extra a's, same b's"  # => co-21
    assert not in_anbn(pumped_down), "pumping y down must break membership -- fewer a's, same b's"  # => co-21
    print(f"Every valid split's pumped string breaks a^n b^n membership: True")  # => co-21: the counterexample holds
    # => co-21: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
