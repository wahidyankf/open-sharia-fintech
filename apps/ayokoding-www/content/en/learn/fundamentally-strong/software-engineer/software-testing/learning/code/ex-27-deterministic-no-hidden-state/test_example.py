# learning/code/ex-27-deterministic-no-hidden-state/test_example.py
"""Example 27: Deterministic, Order-Independent Tests."""

# ex-27: two tests that could, in principle, run in EITHER order -- neither depends on the other (co-26)  # fmt: skip
_counter_state = {"value": 0}  # => module-level state that COULD leak between tests if misused  # fmt: skip


def increment_and_reset(state: dict[str, int]) -> int:  # => the unit under test
    state["value"] += 1  # => mutates the PASSED-IN dict, not the module-level one directly  # fmt: skip
    result = state["value"]  # => capture before resetting
    state["value"] = 0  # => reset immediately -- the function itself leaves no lasting trace  # fmt: skip
    return result  # => returns exactly 1, every single time, regardless of call order


def test_increment_and_reset_called_first() -> None:
    fresh_state = {"value": 0}  # => arrange: a FRESH dict, not the shared module-level one  # fmt: skip
    assert increment_and_reset(fresh_state) == 1  # => always 1 -- no hidden dependency on prior calls  # fmt: skip
    assert fresh_state["value"] == 0  # => confirms the function reset its OWN input, leaking nothing  # fmt: skip


def test_increment_and_reset_called_second() -> None:
    fresh_state = {"value": 0}  # => a SEPARATE fresh dict -- identical starting point to the test above  # fmt: skip
    assert increment_and_reset(fresh_state) == 1  # => IDENTICAL result -- order-independent (co-26)  # fmt: skip
    # => if this test depended on test_increment_and_reset_called_first running earlier
    # => and mutating shared state, running these two tests in reverse order (pytest
    # => supports random ordering via plugins) would produce a DIFFERENT result here
