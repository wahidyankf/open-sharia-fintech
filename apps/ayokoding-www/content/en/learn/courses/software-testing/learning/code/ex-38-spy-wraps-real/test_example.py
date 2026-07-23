# learning/code/ex-38-spy-wraps-real/test_example.py
"""Example 38: A Spy Wraps the Real Object."""

from unittest.mock import MagicMock  # => wraps= turns a MagicMock into a SPY around a real object (co-15)  # fmt: skip


class Calculator:  # => a REAL implementation -- the spy will delegate to THIS, not fake it  # fmt: skip
    def add(self, a: int, b: int) -> int:  # => genuine computation, no canned answer involved  # fmt: skip
        return a + b  # => the actual, real logic being spied on


def test_spy_delegates_to_the_real_object_while_recording_calls() -> None:
    real_calculator = Calculator()  # => arrange: a genuine instance, real behavior intact  # fmt: skip
    spy = MagicMock(wraps=real_calculator)  # => co-15: EVERY call is forwarded to real_calculator  # fmt: skip
    # => wraps= is what distinguishes a spy from a plain mock (ex-31/32): calling spy.add(...)
    # => both RECORDS the call (like a mock) AND actually runs real_calculator.add(...) (unlike a mock)
    result = spy.add(2, 3)  # => act: genuinely computed via the real Calculator, not a canned value  # fmt: skip
    assert result == 5  # => proves the REAL computation ran -- a plain mock would return a MagicMock here  # fmt: skip
    spy.add.assert_called_once_with(2, 3)  # => proves the call was ALSO recorded, exactly like ex-32  # fmt: skip
