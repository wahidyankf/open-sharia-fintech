"""Example 8: pytest verification for Method Call As Message."""

from example import Dog, Duck, announce


def test_each_receiver_dispatches_its_own_reply() -> None:
    assert announce(Duck()) == "Quack"  # => Duck answers the message its own way
    assert announce(Dog()) == "Woof"  # => Dog answers the SAME message its own, different way


def test_dispatch_depends_only_on_the_runtime_receiver() -> None:
    speakers = [Duck(), Dog(), Duck()]  # => order matters: proves dispatch is per-object, not fixed
    replies = [announce(s) for s in speakers]  # => the same announce() call site, three receivers
    assert replies == ["Quack", "Woof", "Quack"]  # => each call picked its OWN receiver's reply


# => Run: pytest -- Output: 2 passed
