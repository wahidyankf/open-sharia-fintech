"""Example 60: pytest verification for fsync as a Durability Barrier."""

from example import DurabilityModel


def test_writes_before_fsync_survive_a_crash() -> None:
    model = DurabilityModel()
    model.write("a")
    model.fsync()
    survivors = model.crash()
    assert "a" in survivors


def test_writes_after_the_last_fsync_do_not_survive() -> None:
    model = DurabilityModel()
    model.write("a")
    model.fsync()
    model.write("b")
    survivors = model.crash()
    assert "b" not in survivors


# => Run: pytest -- Output: 2 passed
