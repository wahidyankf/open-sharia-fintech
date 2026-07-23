"""Example 18: pytest verification for Dataflow Two Cells."""

from example import Cell


def test_b_recomputes_from_as_new_value() -> None:
    a = Cell(lambda: 5)  # => fresh cell A, isolated from the module-level demo
    b = Cell(lambda: a.value + 1)  # => B depends on A via a formula
    assert b.value == 6  # => 5 + 1 at construction time

    a.value = 100  # => change A directly
    assert b.value == 6  # => B is still stale -- recompute() has not run yet
    b.recompute()  # => fire the dataflow edge explicitly
    assert b.value == 101  # => B now reflects A's new value: 100 + 1


def test_a_cell_with_no_dependency_never_changes_on_its_own() -> None:
    a = Cell(lambda: 42)  # => a plain-value cell
    a.recompute()  # => recomputing a constant rule is a no-op
    assert a.value == 42  # => still the same constant


# => Run: pytest -- Output: 2 passed
