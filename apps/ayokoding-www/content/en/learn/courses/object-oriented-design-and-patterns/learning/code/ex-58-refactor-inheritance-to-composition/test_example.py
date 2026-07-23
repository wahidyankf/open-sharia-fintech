"""Example 58: pytest verification that behavior is unchanged after the composition refactor."""

from example import (
    ComposedNotifier,
    LoggingBehavior,
    RetryBehavior,
    ThrottledRetryingLoggingNotifier,
    ThrottleBehavior,
    send_with_capabilities,
)


def test_inheritance_and_composition_versions_agree_on_successful_sends() -> None:
    old = ThrottledRetryingLoggingNotifier(attempts=2, max_calls=5)  # => 4-level inheritance version
    old_result = old.send("hello")  # => exercises the full inherited chain
    logging = LoggingBehavior()  # => the composed logging unit
    new = ComposedNotifier(logging=logging)  # => depth-1 composed version
    new_result = send_with_capabilities(new, "hello", RetryBehavior(attempts=2), ThrottleBehavior(max_calls=5))
    assert old_result == new_result == "SEND:hello"  # => both versions produce identical output
    assert old.log == logging.log == ["hello", "hello"]  # => both log every retry attempt identically


def test_throttling_behavior_is_identical_once_budget_is_exhausted() -> None:
    old = ThrottledRetryingLoggingNotifier(attempts=1, max_calls=1)  # => budget of exactly one call
    old.send("first")  # => consumes the single-call budget
    old_second = old.send("second")  # => budget exhausted -- should be throttled
    logging = LoggingBehavior()
    new = ComposedNotifier(logging=logging)
    retry = RetryBehavior(attempts=1)
    throttle = ThrottleBehavior(max_calls=1)
    send_with_capabilities(new, "first", retry, throttle)  # => consumes the composed version's budget too
    new_second = send_with_capabilities(new, "second", retry, throttle)  # => should also be throttled
    assert old_second == new_second == "THROTTLED"  # => both versions refuse identically once budget is spent


def test_composed_version_has_inheritance_depth_of_exactly_one() -> None:
    assert ComposedNotifier.__mro__ == (ComposedNotifier, object)  # => depth 1: no intermediate base classes
    assert len(ThrottledRetryingLoggingNotifier.__mro__) == 5  # => old version: 4 custom levels + object


# => Run: pytest -q -- Output: 3 passed
