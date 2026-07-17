"""Example 17: pytest verification for Reactive Counter."""

from example import ObservableValue


def test_subscriber_sees_the_new_value_on_set() -> None:
    counter = ObservableValue(0)  # => fresh observable, isolated from the module-level demo
    seen: list[int] = []  # => local recorder for this test only
    counter.subscribe(lambda v: seen.append(v))  # => register a listener
    counter.set(5)  # => trigger it once
    assert seen == [5]  # => the subscriber saw exactly the new value


def test_multiple_subscribers_all_receive_every_update() -> None:
    counter = ObservableValue(0)  # => fresh observable
    first: list[int] = []  # => recorder for subscriber A
    second: list[int] = []  # => recorder for subscriber B
    counter.subscribe(lambda v: first.append(v))  # => register A
    counter.subscribe(lambda v: second.append(v))  # => register B
    counter.set(7)  # => both A and B must be pushed this update
    counter.set(9)  # => and this one too
    assert first == [7, 9]  # => A saw both updates in order
    assert second == [7, 9]  # => B saw both updates in order, independently of A


# => Run: pytest -- Output: 2 passed
