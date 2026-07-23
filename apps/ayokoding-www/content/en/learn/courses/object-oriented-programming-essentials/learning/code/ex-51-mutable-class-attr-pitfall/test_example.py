"""Example 51: pytest verification for The Mutable Class-Attribute Pitfall."""

from example import BuggyCart, Cart


def test_buggy_cart_shares_state_across_instances() -> None:
    a, b = BuggyCart(), BuggyCart()
    a.add("apple")
    assert b.items == [
        "apple"
    ]  # => reproduces the bug: b sees a's item through the shared list


def test_fixed_cart_isolates_state_per_instance() -> None:
    a, b = Cart(), Cart()
    a.add("apple")
    assert b.items == []  # => the fix: each instance's __init__ built its own list


# => Run: pytest -- Output: 2 passed
