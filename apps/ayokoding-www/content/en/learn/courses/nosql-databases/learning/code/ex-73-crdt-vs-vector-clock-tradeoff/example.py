"""Example 73: CRDT vs. Vector-Clock Tradeoff."""  # => co-15,co-16: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-16: a typed G-Counter, reused from Example 43's own model


@dataclass  # => intentionally MUTABLE -- a replica's own counter grows as it counts local increments
class GCounter:  # => co-16: the SAME grow-only counter CRDT from Example 43
    replica_id: str  # => this counter's own identity
    counts: dict[str, int] = field(default_factory=dict)  # => replica_id -> that replica's own local count

    def increment(self) -> None:  # => co-16: a replica may only increment its own slot
        self.counts[self.replica_id] = self.counts.get(self.replica_id, 0) + 1  # => bumps this replica's own counter by 1

    def value(self) -> int:  # => the counter's current total
        return sum(self.counts.values())  # => sum of every replica's independent contribution

    def merge(self, other: GCounter) -> GCounter:  # => co-16: the CRDT merge -- requires ZERO application-level conflict code
        merged_counts = dict(self.counts)  # => starts from this counter's own state
        for replica_id, count in other.counts.items():  # => merges in every slot from the other replica's state
            merged_counts[replica_id] = max(merged_counts.get(replica_id, 0), count)  # => MAX per slot
        result = GCounter(self.replica_id)  # => a fresh counter object to hold the merged result
        result.counts = merged_counts  # => assigns the merged per-replica slots
        return result  # => hand back the merged counter -- automatically, with no app code deciding anything


@dataclass(frozen=True)  # => frozen -- a vector clock snapshot is a stated fact about causal history
class VectorClock:  # => co-15: the SAME vector clock model from Example 42
    counters: dict[str, int]  # => replica name -> how many writes that replica has causally seen


def clocks_are_concurrent(a: VectorClock, b: VectorClock) -> bool:  # => co-15: True means a genuine, unresolved conflict
    """Return True if neither vector clock causally dominates the other."""  # => documents the contract, no runtime output
    replicas = set(a.counters) | set(b.counters)  # => every replica either clock has ever counted
    a_le_b = all(a.counters.get(r, 0) <= b.counters.get(r, 0) for r in replicas)  # => a dominates b on NO dimension
    b_le_a = all(b.counters.get(r, 0) <= a.counters.get(r, 0) for r in replicas)  # => b dominates a on NO dimension
    return not a_le_b and not b_le_a  # => co-15: neither dominates -- CONCURRENT, a genuine conflict


def merge_carts_after_vector_clock_conflict(cart_a: list[str], cart_b: list[str]) -> list[str]:  # => co-15: the APP-LEVEL merge code required
    """An application-level merge function -- REQUIRED because vector clocks only DETECT, never resolve."""  # => documents contract
    merged = list(cart_a)  # => co-15: starts from cart A's own items
    for item in cart_b:  # => co-15: this loop is the "app must write merge code" cost co-15 imposes
        if item not in merged:  # => avoids duplicating an item both carts already agree on
            merged.append(item)  # => co-15: a UNION strategy -- one of several possible app-chosen merge policies
    return merged  # => co-15: this merge POLICY (union) was a DECISION the application had to make


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    # --- The SAME concurrent-edit scenario, modeled two ways: a CRDT counter, and a vector-clocked cart ---

    # CRDT path: two replicas independently increment a shared "likes" counter -- NO app merge code needed.
    replica_a_counter = GCounter("replica-A")  # => co-16: replica A's own counter
    replica_b_counter = GCounter("replica-B")  # => co-16: replica B's own INDEPENDENT counter
    replica_a_counter.increment()  # => co-16: A counts one "like", independently
    replica_b_counter.increment()  # => co-16: B counts one "like", independently, concurrently
    merged_counter = replica_a_counter.merge(replica_b_counter)  # => co-16: the merge() METHOD does ALL the work -- zero app-level decision-making
    print(f"CRDT G-Counter merge: {merged_counter.value()} likes total (merge() required ZERO app-level merge code)")  # => Output: CRDT G-Counter merge: 2 likes total (merge() required ZERO app-level merge code)
    assert merged_counter.value() == 2  # => co-16: both increments counted, automatically, correctly

    # Vector-clock path: two replicas independently add an item to a shopping cart -- APP merge code IS needed.
    clock_from_a = VectorClock({"replica-A": 1, "replica-B": 0})  # => co-15: replica-A's own write
    clock_from_b = VectorClock({"replica-A": 0, "replica-B": 1})  # => co-15: replica-B's own INDEPENDENT write
    conflict = clocks_are_concurrent(clock_from_a, clock_from_b)  # => co-15: the vector clock DETECTS this is a genuine conflict
    assert conflict is True  # => co-15: correctly flagged -- but detection is ALL the vector clock does
    cart_a = ["book"]  # => replica A's cart, as it independently saw it
    cart_b = ["pen"]  # => replica B's cart, as it independently saw it, CONCURRENTLY
    merged_cart = merge_carts_after_vector_clock_conflict(cart_a, cart_b)  # => co-15: the APP had to WRITE this merge function itself
    print(f"Vector-clock-detected conflict resolved by APP-LEVEL merge code: {merged_cart}")  # => Output: Vector-clock-detected conflict resolved by APP-LEVEL merge code: ['book', 'pen']
    assert merged_cart == ["book", "pen"]  # => co-15: the union-merge POLICY the application code above chose to implement

    print("Contrast: CRDT converged automatically via merge(); vector clock only DETECTED the conflict, requiring separate app merge logic")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
