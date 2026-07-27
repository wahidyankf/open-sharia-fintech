"""Example 73: pytest verification for the Non-Repeatable-Read Anomaly."""

import example


def test_read_committed_sees_a_concurrent_commit_mid_transaction() -> None:
    example.committed_value = "v1"
    first = example.read_committed_fetch()
    example.committed_value = "v2"
    second = example.read_committed_fetch()
    assert first != second


def test_repeatable_read_stays_stable_across_the_same_concurrent_commit() -> None:
    example.committed_value = "v1"
    snapshot = example.read_committed_fetch()
    example.committed_value = "v2"
    second = example.repeatable_read_fetch(snapshot)
    assert second == snapshot


# => Run: pytest -- Output: 2 passed
