# learning/code/ex-21-birthday-collision/birthday_collision.py
"""Example 21: The Birthday-Paradox Collision Probability."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

DAYS_IN_YEAR = 365  # => co-12: the "buckets" every person's birthday lands in, ignoring leap years


def probability_of_shared_birthday(people: int, days: int = DAYS_IN_YEAR) -> float:  # => co-12: 1 - P(all distinct)
    """Probability at least two people (of `people`) share a birthday out of `days` possible days."""  # => co-12: documents probability_of_shared_birthday's contract -- no runtime output, just sets its __doc__
    probability_all_distinct = 1.0  # => co-12: starts at certainty, multiplied down as each person is added
    for i in range(people):  # => co-12: person i+1 must avoid all i already-claimed days
        probability_all_distinct *= (days - i) / days  # => co-12: the counting-principle term for this person
    return 1.0 - probability_all_distinct  # => co-12: complement -- "at least one collision" = 1 - "all distinct"


if __name__ == "__main__":  # => co-12: entry point -- this block runs only when the file executes directly, not on import
    for n in (10, 20, 22, 23, 30, 50):  # => co-12: a spread of group sizes around the famous n=23 threshold
        p = probability_of_shared_birthday(n)  # => co-12: this group size's collision probability
        print(f"people={n:>3}  P(shared birthday) = {p:.4f}")  # => co-12: printed to 4 decimal places
    p22 = probability_of_shared_birthday(22)  # => co-12: just below the famous threshold
    p23 = probability_of_shared_birthday(23)  # => co-12: the famous "50%" threshold group size
    print(f"P(22) = {p22:.4f}, P(23) = {p23:.4f}")  # => co-12: shown side by side for direct comparison
    assert p22 < 0.5, "22 people must NOT yet exceed 50% collision probability"  # => co-12
    assert p23 > 0.5, "23 people must exceed 50% collision probability"  # => co-12: the textbook claim
    print(f"P(23) exceeds 0.5: {p23 > 0.5}")  # => co-12: reached only if both asserts above passed
    # => co-12: every assert above is this script's own regression check -- a clean exit means the claim held for these inputs
