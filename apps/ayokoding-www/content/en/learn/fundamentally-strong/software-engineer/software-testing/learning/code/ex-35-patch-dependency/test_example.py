# learning/code/ex-35-patch-dependency/test_example.py
"""Example 35: Patching a Dependency."""

from unittest import mock  # => brings in mock.patch, a context manager that swaps an attribute (co-14)  # fmt: skip


def get_current_time() -> str:  # => the REAL dependency -- deliberately unpredictable ("REAL_TIME" stands in)  # fmt: skip
    return "REAL_TIME"  # => in a real app this might call time.strftime(...) -- non-deterministic  # fmt: skip


def format_greeting() -> str:  # => the unit under test -- depends on get_current_time via module lookup  # fmt: skip
    return f"The time is {get_current_time()}"  # => looks up get_current_time in THIS module's namespace  # fmt: skip


def test_patch_replaces_the_dependency_for_the_duration_of_the_test() -> None:
    # mock.patch's target string names WHERE the dependency is LOOKED UP (this module,
    # via __name__), not where it happens to be defined -- "patch where it's used" (co-14)
    with mock.patch(f"{__name__}.get_current_time", return_value="12:00"):  # => replaces it temporarily  # fmt: skip
        assert format_greeting() == "The time is 12:00"  # => act+assert: sees the PATCHED value  # fmt: skip
    # => outside the "with" block, get_current_time is AUTOMATICALLY restored to the
    # => real function -- the line below proves the patch did not leak past the block
    assert format_greeting() == "The time is REAL_TIME"  # => confirms the real dependency is back  # fmt: skip
