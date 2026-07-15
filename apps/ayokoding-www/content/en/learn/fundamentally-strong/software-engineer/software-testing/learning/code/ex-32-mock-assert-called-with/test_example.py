# learning/code/ex-32-mock-assert-called-with/test_example.py
"""Example 32: assert_called_once_with."""

from unittest.mock import MagicMock  # => same mock object as ex-31, checking ARGUMENTS this time (co-13)  # fmt: skip


def send_email(mailer, to: str, subject: str) -> None:  # => the unit under test  # fmt: skip
    mailer.send(to, subject)  # => delegates to a collaborator -- the EXACT args matter here  # fmt: skip


def test_mock_asserts_the_exact_call_arguments() -> None:
    mock_mailer = MagicMock()  # => arrange: a bare mock, no return value configured -- not needed here  # fmt: skip
    send_email(mock_mailer, "ada@example.com", "Welcome")  # => act: triggers mailer.send(...)  # fmt: skip
    mock_mailer.send.assert_called_once_with("ada@example.com", "Welcome")  # => co-13: checks BOTH call count AND exact arguments  # fmt: skip
    # => if send_email had called mailer.send with a DIFFERENT subject, or called it twice,
    # => or never called it at all, this one line would raise AssertionError with a diff
    # => showing exactly what was expected versus what mailer.send actually received
