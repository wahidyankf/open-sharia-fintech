"""Example 72: pytest verification that the SAME contract passes ListStack and fails BuggyQueueAsStack."""

import pytest

from example import BuggyQueueAsStack, ListStack, run_stack_contract


def test_conforming_implementation_satisfies_the_stack_contract() -> None:
    run_stack_contract(ListStack)  # => no exception raised -- LSP holds: ListStack substitutes cleanly


def test_violating_subtype_fails_the_same_contract() -> None:
    with pytest.raises(AssertionError, match="LSP violation"):
        run_stack_contract(BuggyQueueAsStack)  # => the SAME contract catches the violation, no new test file needed


def test_empty_stack_raises_on_pop_for_both_implementations() -> None:
    for make_stack in (ListStack, BuggyQueueAsStack):
        stack = make_stack()
        with pytest.raises(IndexError):
            stack.pop()  # => both implementations honor this part of the contract correctly


# => Run: pytest -q -- Output: 3 passed
