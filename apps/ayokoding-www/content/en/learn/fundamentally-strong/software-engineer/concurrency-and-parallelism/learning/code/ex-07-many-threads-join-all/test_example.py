"""Example 7: pytest verification for Starting Many Threads and Joining Them All."""

from example import run_all


def test_every_thread_completes_exactly_once() -> None:
    ids = run_all(8)
    assert len(ids) == 8  # => the two-loop start-then-join pattern collected every worker
    assert sorted(ids) == list(range(8))  # => no id missing, none duplicated


def test_different_count_still_completes() -> None:
    ids = run_all(20)
    assert sorted(ids) == list(range(20))  # => the pattern scales to more threads unchanged


# => Run: pytest -- Output: 2 passed
