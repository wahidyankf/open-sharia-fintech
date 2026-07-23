"""Example 69: pytest verification for Declarative Mini DSL."""

from example import even, gt


def test_composed_and_rule_runs_correctly() -> None:
    rule = gt(5) & even()  # => "n > 5 AND n is even"
    assert rule.evaluate(6) is True  # => 6 > 5 and even
    assert rule.evaluate(3) is False  # => 3 is not > 5
    assert rule.evaluate(7) is False  # => 7 > 5 but odd


def test_composed_or_rule_and_its_self_describing_label() -> None:
    rule = gt(100) | even()  # => "n > 100 OR n is even"
    assert rule.evaluate(4) is True  # => not > 100, but even
    assert rule.evaluate(3) is False  # => neither condition holds
    assert rule.label == "(n > 100 OR n is even)"  # => the DSL composes a readable label automatically


# => Run: pytest -- Output: 2 passed
