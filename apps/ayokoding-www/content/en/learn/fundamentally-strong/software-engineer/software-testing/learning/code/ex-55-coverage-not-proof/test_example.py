# learning/code/ex-55-coverage-not-proof/test_example.py
"""Example 55: Coverage Is Not Proof."""

from hypothesis import given  # => the property test that WILL catch what coverage alone missed (co-18)  # fmt: skip
from hypothesis import strategies as st  # => generates lists, INCLUDING the empty list eventually (co-20)  # fmt: skip


def average(numbers: list[int]) -> float:  # => the unit under test -- ONE line, a latent bug (co-21)  # fmt: skip
    return sum(numbers) / len(numbers)  # => crashes with ZeroDivisionError if numbers is EMPTY  # fmt: skip


def test_average_basic() -> None:  # => a single, ordinary unit test -- passes, AND covers 100% of the one line  # fmt: skip
    assert average([1, 2, 3]) == 2  # => 6/3 == 2 -- this ALONE achieves 100% line coverage of average()  # fmt: skip
    # => coverage.py would report average() as fully covered after just this ONE call --
    # => there is only one line in the function body, and this call executes it (co-21)


@given(st.lists(st.integers()))  # => co-18: NO min_size -- Hypothesis WILL eventually generate []  # fmt: skip
def test_average_property_finds_what_coverage_missed(numbers: list[int]) -> None:
    # => this property test is EXPECTED to fail -- it generates the empty list eventually,
    # => which crashes average() with ZeroDivisionError, a bug 100% line coverage NEVER caught
    result = average(
        numbers
    )  # => genuinely raises ZeroDivisionError when numbers == []
    assert isinstance(result, float)  # => never reached for the empty-list case -- the crash happens first  # fmt: skip
