"""Example 23: pytest verification for Match-Case Dispatch."""

from example import handle_command


def test_every_literal_branch_fires() -> None:
    assert handle_command("start") == "engine started"  # => case #1
    assert handle_command("stop") == "engine stopped"  # => case #2


def test_or_pattern_and_wildcard_branch_fire() -> None:
    assert handle_command("status") == "engine idle"  # => the OR-pattern's first alternative
    assert handle_command("ping") == "engine idle"  # => the OR-pattern's second alternative
    assert handle_command("nope") == "unknown command: nope"  # => the wildcard catches everything else


# => Run: pytest -- Output: 2 passed
