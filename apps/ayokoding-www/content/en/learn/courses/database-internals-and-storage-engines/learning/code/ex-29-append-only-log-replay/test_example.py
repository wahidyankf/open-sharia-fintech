"""Example 29: pytest verification for Append-Only Log Replay."""

from example import append, log, replay


def test_replay_matches_append_order() -> None:
    log.clear()
    append("a")
    append("b")
    append("c")
    assert replay() == ["a", "b", "c"]


def test_sequence_numbers_are_gap_free() -> None:
    log.clear()
    append("x")
    append("y")
    assert [r.seq for r in log] == [0, 1]  # => no gaps, no reordering, ever


# => Run: pytest -- Output: 2 passed
