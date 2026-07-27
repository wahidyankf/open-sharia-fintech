"""Example 79: pytest verification for the Workload-Based Engine Chooser."""

from example import choose_engine


def test_a_write_heavy_workload_selects_lsm() -> None:
    assert choose_engine(write_fraction=0.8) == "LSM"


def test_a_read_heavy_workload_selects_btree() -> None:
    assert choose_engine(write_fraction=0.2) == "B-tree"


# => Run: pytest -- Output: 2 passed
