"""Example 56: pytest verification for Dependency Inversion with abc.ABC."""

import pytest

from example import EmailSender, IncompleteSender, Notifier, SmsSender


def test_notifier_depends_only_on_the_abstraction() -> None:
    notifier: Notifier = Notifier(EmailSender())
    assert notifier.notify("build failed") == "email: build failed"
    notifier.sender = SmsSender()  # => swapped detail, no Notifier class edit
    assert notifier.notify("build failed") == "sms: build failed"


def test_incomplete_subclass_cannot_be_instantiated() -> None:
    with pytest.raises(TypeError):  # => missing send() -- ABC blocks construction
        IncompleteSender()  # type: ignore


# => Run: pytest -- Output: 2 passed
