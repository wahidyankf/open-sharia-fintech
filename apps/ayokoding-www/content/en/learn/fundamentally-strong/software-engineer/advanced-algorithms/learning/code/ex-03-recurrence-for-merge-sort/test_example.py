"""Example 3: pytest verification for the Merge Sort Recurrence."""

from example import closed_form, recurrence_t


def test_recurrence_matches_closed_form_for_powers_of_two() -> None:
    for n in (2, 4, 8, 16, 32, 64):  # => every power of two up to 64
        assert recurrence_t(n) == closed_form(
            n
        )  # => T(n) via recursion equals n*log2(n)+n


def test_base_case_is_one() -> None:
    assert recurrence_t(1) == 1  # => T(1) = 1, the smallest subproblem


# => Run: pytest -- Output: 2 passed
