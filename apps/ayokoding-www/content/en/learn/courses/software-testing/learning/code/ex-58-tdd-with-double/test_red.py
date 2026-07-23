# learning/code/ex-58-tdd-with-double/test_red.py
"""Example 58 (RED half): TDD with a Stubbed Collaborator."""


# ex-58 RED: the collaborator's stub already exists -- notify_user() itself does not YET (co-17, co-12)  # fmt: skip
class StubNotificationSender:  # => a stub collaborator, written FIRST, before the unit that uses it  # fmt: skip
    def send(self, message: str) -> bool:  # => a canned, ALWAYS-succeeds answer (co-12)
        return True  # => no real notification service involved -- just a fixed reply


def test_notify_user_sends_via_stub() -> None:
    stub = StubNotificationSender()  # => arrange: the stubbed collaborator is ready
    # => act: notify_user does not exist ANYWHERE in this file yet -- this call is genuinely red
    result = notify_user(stub, "hello")  # => NameError: 'notify_user' is not defined  # fmt: skip
    assert (
        result is True
    )  # => the INTENDED behavior -- not yet true, not yet even reachable
