"""Example 43: CRDT G-Counter (Grow-Only Counter)."""  # => co-16: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-16: a typed G-Counter -- one slot per replica, merged by taking the max per slot


@dataclass  # => intentionally MUTABLE -- a replica's own counter grows as it counts local increments
class GCounter:  # => co-16: a Conflict-free Replicated Data Type -- grow-only, never decrements
    replica_id: str  # => this counter's OWN identity -- the slot it is allowed to increment
    counts: dict[str, int] = field(default_factory=dict)  # => co-16: replica_id -> that replica's own local count

    def increment(self) -> None:  # => co-16: a replica may ONLY increment its OWN slot, never another's
        self.counts[self.replica_id] = self.counts.get(self.replica_id, 0) + 1  # => co-16: bumps this replica's own counter by 1

    def value(self) -> int:  # => co-16: the counter's current total is the SUM across every replica's slot
        return sum(self.counts.values())  # => co-16: total = sum of every replica's independent contribution

    def merge(self, other: GCounter) -> GCounter:  # => co-16: the CRDT merge function -- deterministic, commutative, associative
        merged_counts = dict(self.counts)  # => starts from this counter's own state
        for replica_id, count in other.counts.items():  # => co-16: merges in EVERY slot from the other replica's state
            merged_counts[replica_id] = max(merged_counts.get(replica_id, 0), count)  # => co-16: MAX per slot -- never double-counts, never loses an increment
        result = GCounter(self.replica_id)  # => a fresh counter object to hold the merged result
        result.counts = merged_counts  # => assigns the merged per-replica slots
        return result  # => hand back the merged counter -- no application-level conflict code was needed


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    replica_a = GCounter("replica-A")  # => co-16: replica A's own counter, starts empty
    replica_b = GCounter("replica-B")  # => co-16: replica B's own INDEPENDENT counter, starts empty

    replica_a.increment()  # => co-16: A counts one local event
    replica_a.increment()  # => co-16: A counts a second local event -- A's own slot is now 2
    replica_b.increment()  # => co-16: B counts one local event, INDEPENDENTLY of A -- B's own slot is now 1

    merged_a_then_b = replica_a.merge(replica_b)  # => co-16: merge in ONE order -- A first, then B's state folded in
    merged_b_then_a = replica_b.merge(replica_a)  # => co-16: merge in the OPPOSITE order -- B first, then A's state folded in

    assert merged_a_then_b.value() == 3  # => co-16: 2 (from A) + 1 (from B) = 3, regardless of merge order
    assert merged_b_then_a.value() == 3  # => co-16: the SAME total -- merge order genuinely does not matter
    print(f"merge(A, B).value() = {merged_a_then_b.value()}")  # => Output: merge(A, B).value() = 3
    print(f"merge(B, A).value() = {merged_b_then_a.value()}")  # => Output: merge(B, A).value() = 3
    print("Merge is commutative: both orders converge to the identical total, with zero app-level merge code")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
