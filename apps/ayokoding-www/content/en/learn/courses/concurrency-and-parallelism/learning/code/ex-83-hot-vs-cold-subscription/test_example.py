"""Example 83: pytest verification for Hot vs Cold Observable Subscription Semantics."""

from example import cold_observable_demo, hot_subject_demo


def test_cold_observable_replays_the_full_sequence_to_every_subscriber() -> None:
    first, second = cold_observable_demo()
    assert first == list(range(5))  # => first subscriber gets the full sequence
    assert second == first  # => late subscriber gets an IDENTICAL full replay


def test_hot_subject_drops_emissions_that_happened_before_subscribing() -> None:
    early, late = hot_subject_demo()
    assert early == [1, 2, 3, 4]  # => early subscriber saw every emission
    assert late == [3, 4]  # => late subscriber missed what already fired


# => Run: pytest -- Output: 2 passed
