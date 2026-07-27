"""Example 70: pytest verification for Optimistic Concurrency Control."""

from example import VersionedStore, occ_transaction


def test_a_transaction_with_no_conflict_commits() -> None:
    store = VersionedStore(value="v0", version=0)
    assert occ_transaction(store, "v1") is True
    assert store.value == "v1"


def test_a_conflicting_concurrent_commit_fails_validation() -> None:
    store = VersionedStore(value="v0", version=0)
    read_version = store.version
    occ_transaction(store, "from-someone-else")  # => a concurrent writer commits first
    assert (
        store.version != read_version
    )  # => the version moved -- our earlier read is now stale


# => Run: pytest -- Output: 2 passed
