"""Example 44: CRDT LWW-Register."""  # => co-16: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-16: a typed register state -- a value plus the timestamp that set it


@dataclass(frozen=True)  # => frozen -- a register STATE is a snapshot, merge always produces a NEW one
class LwwRegister:  # => co-16: a CRDT wrapping LWW in a formally mergeable, deterministic type
    value: str  # => this register's current value, as this replica currently sees it
    timestamp: float  # => co-16: the deciding factor for merge, same rule Example 41 used, now wrapped as a CRDT

    def merge(self, other: LwwRegister) -> LwwRegister:  # => co-16: the CRDT merge function -- deterministic, commutative
        if self.timestamp >= other.timestamp:  # => co-16: ties break toward self -- an arbitrary but CONSISTENT rule both replicas apply identically
            return self  # => this register's value is already the (tied-or-later) winner
        return other  # => co-16: the other register's timestamp is strictly later -- it wins


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    register_on_replica_1 = LwwRegister(value="cart:3-items", timestamp=500.0)  # => co-16: replica 1's own local state
    register_on_replica_2 = LwwRegister(value="cart:5-items", timestamp=503.2)  # => co-16: replica 2's own INDEPENDENT, LATER state

    merged_on_replica_1 = register_on_replica_1.merge(register_on_replica_2)  # => co-16: replica 1 merges in replica 2's state
    merged_on_replica_2 = register_on_replica_2.merge(register_on_replica_1)  # => co-16: replica 2 merges in replica 1's state, OPPOSITE order

    assert merged_on_replica_1.value == "cart:5-items"  # => co-16: replica 2's later timestamp (503.2) wins, regardless of merge direction
    assert merged_on_replica_2.value == "cart:5-items"  # => co-16: the SAME winner on replica 2 -- deterministic convergence
    assert merged_on_replica_1 == merged_on_replica_2  # => co-16: BOTH replicas now hold the IDENTICAL register state
    print(f"Replica 1 merged value: {merged_on_replica_1.value}")  # => Output: Replica 1 merged value: cart:5-items
    print(f"Replica 2 merged value: {merged_on_replica_2.value}")  # => Output: Replica 2 merged value: cart:5-items
    print("Both replicas converged to the identical state -- no coordinator, no app-level merge decision needed")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
