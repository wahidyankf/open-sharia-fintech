# => Use the standard-library helper required by this runnable model.
from collections import Counter

# => Use the standard-library helper required by this runnable model.
from hashlib import sha256


# => Isolate the operation so its observable behavior can be checked.
def point(value: str) -> int:
    # The same hash function lets virtual nodes and keys share positions.
    # => Return the observable result of this modeled operation.
    return int(sha256(value.encode()).hexdigest(), 16)


# => Isolate the operation so its observable behavior can be checked.
def owner(nodes: list[str], key: str, replicas: int = 32) -> str:
    # Several positions per physical node make each node own smaller intervals.
    # => Initialize or update deterministic state used by this demonstration.
    ring = sorted(
        # => Initialize or update deterministic state used by this demonstration.
        (point(f"{node}:{replica}"), node)
        # => Repeat the deterministic step over the current input.
        for node in nodes
        # => Repeat the deterministic step over the current input.
        for replica in range(replicas)
        # => Initialize or update deterministic state used by this demonstration.
    )
    # The first clockwise position owns the key.
    # => Return the observable result of this modeled operation.
    return next((node for location, node in ring if point(key) <= location), ring[0][1])


# => Initialize or update deterministic state used by this demonstration.
counts = Counter(owner(["a", "b", "c"], f"key-{i}") for i in range(300))
# Each physical node receives work; variance is expected but no node is absent.
# => Check the promised observable behavior of the demonstration.
assert set(counts) == {"a", "b", "c"}
# => Emit the final observable state for a direct run.
print(dict(counts))
