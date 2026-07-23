# learning/code/ex-19-quantifiers-all-any/quantifiers.py
"""Example 19: Modeling ∀/∃ with all()/any() over a Domain."""  # => co-11: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

from collections.abc import Callable  # => co-11: types the predicate ∀/∃ are quantified over

Predicate = Callable[[int], bool]  # => co-11: every predicate in this example has this exact int -> bool shape


def for_all(domain: list[int], predicate: Predicate) -> bool:  # => co-11: ∀x in domain: predicate(x)
    """∀ (universal quantifier): predicate holds for EVERY member of the domain."""  # => co-11: documents for_all's contract -- no runtime output, just sets its __doc__
    return all(predicate(x) for x in domain)  # => co-11: all() short-circuits on the first False


def there_exists(domain: list[int], predicate: Predicate) -> bool:  # => co-11: ∃x in domain: predicate(x)
    """∃ (existential quantifier): predicate holds for AT LEAST ONE member of the domain."""  # => co-11: documents there_exists's contract -- no runtime output, just sets its __doc__
    return any(predicate(x) for x in domain)  # => co-11: any() short-circuits on the first True


def is_even(x: int) -> bool:  # => co-11: the predicate ∀ is quantified over below
    return x % 2 == 0  # => co-11: returns this computed value to the caller


def is_greater_than_9(x: int) -> bool:  # => co-11: a second predicate -- true for exactly one domain member (10)
    return x > 9  # => co-11: returns this computed value to the caller


if __name__ == "__main__":  # => co-11: entry point -- this block runs only when the file executes directly, not on import
    domain = [2, 4, 6, 8, 10]  # => co-11: a domain deliberately chosen so "all even" is TRUE
    forall_even = for_all(domain, is_even)  # => co-11: ∀x in domain: even(x)
    exists_gt9 = there_exists(domain, is_greater_than_9)  # => co-11: ∃x in domain: x > 9
    hand_checked_forall = all(x % 2 == 0 for x in domain)  # => co-11: an independent hand check, same domain
    hand_checked_exists = any(x > 9 for x in domain)  # => co-11: an independent hand check, same domain
    print(f"domain = {domain}")  # => co-11: shows the domain both quantifiers range over
    print(f"∀x even(x) = {forall_even}")  # => co-11: expect True -- every element is even
    print(f"∃x x>9     = {exists_gt9}")  # => co-11: expect True -- only 10 satisfies it, but that's enough for ∃
    assert forall_even == hand_checked_forall == True, "∀ result must match the hand check"  # => co-11
    assert exists_gt9 == hand_checked_exists == True, "∃ result must match the hand check"  # => co-11
    print("Both quantifiers match their hand-checked expectations: True")  # => co-11: both asserts passed
    # => co-11: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
