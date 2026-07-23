"""Example 68: pytest verification for Constructor-Injected Dependencies Enable Fakes in Tests."""

from example import Event, FakeClock


def test_fake_collaborator_substitutes_cleanly_in_a_test() -> None:
    event: Event = Event(FakeClock())  # type: ignore  # => duck typing accepts the structural match
    assert (
        event.timestamp() == "1999-01-01T00:00:00"
    )  # => no real clock or real time involved


# => Run: pytest -- Output: 1 passed
