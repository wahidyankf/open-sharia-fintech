"""Example 69: pytest verification that each behavioral pattern dispatches correctly."""

from example import (
    AddTextCommand,
    EvenNumbers,
    Green,
    Publisher,
    Red,
    SalesReport,
    TierOneSupport,
    TierTwoSupport,
    by_length,
    sort_words,
)


def test_strategy_sorts_by_the_supplied_key() -> None:
    assert sort_words(["banana", "kiwi", "fig"], key=by_length) == ["fig", "kiwi", "banana"]  # => shortest first


def test_observer_notifies_a_subscriber_without_publisher_edits() -> None:
    events: list[str] = []
    publisher = Publisher()
    publisher.subscribe(lambda msg: events.append(msg.upper()))  # => registered without editing Publisher
    publisher.publish("news")
    assert events == ["NEWS"]


def test_command_undo_reverses_the_last_command() -> None:
    doc: list[str] = []
    cmd = AddTextCommand(doc, "hello")
    cmd.execute()
    assert doc == ["hello"]
    cmd.undo()
    assert doc == []  # => undo reversed exactly what execute() did


def test_template_method_shares_the_flow_and_fills_only_body() -> None:
    assert SalesReport().run() == "[REPORT] sales: 42 units [END]"  # => header/footer defaults, body overridden


def test_state_moves_red_to_green_via_next() -> None:
    light = Red()
    light = light.next()
    assert isinstance(light, Green)  # => the state pattern's transition, verified by type


def test_iterator_yields_even_numbers_lazily() -> None:
    assert list(EvenNumbers(10)) == [0, 2, 4, 6, 8]  # => a for-loop-compatible custom iterator


def test_chain_of_responsibility_falls_through_to_the_next_handler() -> None:
    tier_one = TierOneSupport()
    tier_two = TierTwoSupport()
    tier_one.set_next(tier_two)
    assert tier_one.handle(2) == "resolved by tier 2"  # => tier 1 couldn't handle it, tier 2 did


# => Run: pytest -q -- Output: 7 passed
