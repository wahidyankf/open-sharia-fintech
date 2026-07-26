"""Example 80: pytest verification for the Mini Storage Engine Integration."""

from example import MiniEngine


def test_a_committed_write_is_readable_immediately() -> None:
    engine = MiniEngine()
    engine.write("k", "v")
    engine.commit("k")
    assert engine.snapshot_read("k") == "v"


def test_a_committed_write_survives_a_simulated_crash() -> None:
    engine = MiniEngine()
    engine.write("k", "v")
    engine.commit("k")
    engine.crash_and_recover()
    assert engine.snapshot_read("k") == "v"


def test_an_uncommitted_write_is_never_readable_even_before_a_crash() -> None:
    engine = MiniEngine()
    engine.write("k", "v")  # => never committed
    assert engine.snapshot_read("k") is None


# => Run: pytest -- Output: 3 passed
