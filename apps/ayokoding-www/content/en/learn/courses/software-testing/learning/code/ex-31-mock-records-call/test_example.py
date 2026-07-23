# learning/code/ex-31-mock-records-call/test_example.py
"""Example 31: A Mock Records a Call."""

from unittest.mock import MagicMock  # => stdlib's mock object -- records every call made to it (co-13)  # fmt: skip


def notify(observer) -> None:  # => the unit under test -- calls ONE method on its collaborator  # fmt: skip
    observer.on_event("started")  # => the interaction this example wants to VERIFY happened  # fmt: skip


def test_mock_records_that_it_was_called() -> None:
    mock_observer = MagicMock()  # => arrange: MagicMock auto-creates on_event as another MagicMock  # fmt: skip
    notify(mock_observer)  # => act: notify() calls mock_observer.on_event("started") internally  # fmt: skip
    assert mock_observer.on_event.called  # => assert on the INTERACTION, not a return value (co-13)  # fmt: skip
    # => unlike ex-29's stub, this test does not care what on_event RETURNS -- it cares
    # => THAT on_event was called at all, which is a fundamentally different kind of check
    assert mock_observer.on_event.call_count == 1  # => confirms it was called EXACTLY once, not zero or twice  # fmt: skip
