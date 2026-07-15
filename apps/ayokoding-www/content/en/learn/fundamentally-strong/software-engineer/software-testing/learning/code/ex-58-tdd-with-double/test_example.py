# learning/code/ex-58-tdd-with-double/test_example.py
"""Example 58 (GREEN half): TDD with a Stubbed Collaborator."""


# ex-58 GREEN: the SAME tests as test_red.py, now with notify_user() implemented (co-17, co-12)  # fmt: skip
class StubNotificationSender:  # => the IDENTICAL stub from test_red.py -- unchanged  # fmt: skip
    def send(self, message: str) -> bool:  # => still a canned, always-succeeds answer  # fmt: skip
        return True


def notify_user(sender, message: str) -> bool:  # => NEW: just enough logic to satisfy both tests below  # fmt: skip
    if not message:  # => guards against an empty message -- a second case this TDD step adds  # fmt: skip
        return False  # => rejects the empty-message case WITHOUT ever calling the collaborator  # fmt: skip
    return sender.send(message)  # => delegates to whichever collaborator (stub here) it was given  # fmt: skip


def test_notify_user_sends_via_stub() -> None:  # => the EXACT test that was red in test_red.py  # fmt: skip
    stub = StubNotificationSender()  # => arrange: identical stub collaborator
    result = notify_user(stub, "hello")  # => act: now resolves -- notify_user exists in this file  # fmt: skip
    assert result is True  # => stub.send("hello") returns True, notify_user forwards it -- now genuinely green  # fmt: skip


def test_notify_user_rejects_empty_message() -> None:  # => a SECOND case, added alongside the implementation  # fmt: skip
    stub = (
        StubNotificationSender()
    )  # => arrange: same stub, even though this path never calls it
    result = notify_user(
        stub, ""
    )  # => act: empty message -- the guard clause fires FIRST
    assert (
        result is False
    )  # => the collaborator is NEVER consulted for an empty message
