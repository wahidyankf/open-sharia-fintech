"""Example 50: pytest verification for Load-Time Snapshotting."""

from example import Session, User


def test_snapshot_matches_object_state_at_load_time() -> None:
    session = Session()  # => a fresh session
    user = User(id=7, name="Grace")  # => a freshly-mapped object
    session.load(user)  # => snapshots it immediately
    assert session.snapshot_of(user) == {"id": 7, "name": "Grace"}  # => exact match at load time


def test_each_object_gets_its_own_independent_snapshot() -> None:
    session = Session()
    alice = User(id=1, name="Alice")  # => object one
    bob = User(id=2, name="Bob")  # => object two, distinct identity
    session.load(alice)
    session.load(bob)
    assert session.snapshot_of(alice) != session.snapshot_of(bob)  # => two DIFFERENT snapshots
    assert session.snapshot_of(alice)["name"] == "Alice"  # => alice's own snapshot, untouched by bob's


# => Run: pytest -- Output: 2 passed
