"""Example 26: pytest verification for the Accounting Method."""

from example import AccountedArray


def test_credit_balance_never_goes_negative_across_many_resizes() -> None:
    arr = AccountedArray()
    for i in range(2000):  # => several doublings happen along the way
        arr.append(i)
        assert arr.credit_balance >= 0  # => re-checked after every single append


def test_final_size_matches_number_of_appends() -> None:
    arr = AccountedArray()
    for i in range(37):  # => a deliberately non-power-of-two count
        arr.append(i)
    assert arr.size == 37


# => Run: pytest -- Output: 2 passed
