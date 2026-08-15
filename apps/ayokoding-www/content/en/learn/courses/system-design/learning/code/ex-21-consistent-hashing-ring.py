# => Use the standard-library helper required by this runnable model.
from hashlib import sha256


# => Isolate the operation so its observable behavior can be checked.
def point(value: str) -> int:
    # A stable digest gives names and keys the same coordinate space.
    # => Return the observable result of this modeled operation.
    return int(sha256(value.encode()).hexdigest(), 16)


# => Isolate the operation so its observable behavior can be checked.
def owner(nodes: list[str], key: str) -> str:
    # Sort nodes by their ring position before finding the clockwise successor.
    # => Initialize or update deterministic state used by this demonstration.
    ring = sorted((point(node), node) for node in nodes)
    # Wrap to the first node when a key lies beyond the last coordinate.
    # => Return the observable result of this modeled operation.
    return next((node for location, node in ring if point(key) <= location), ring[0][1])


# => Initialize or update deterministic state used by this demonstration.
before = [owner(["a", "b", "c"], f"key-{i}") for i in range(100)]
# => Initialize or update deterministic state used by this demonstration.
after = [owner(["a", "b", "c", "d"], f"key-{i}") for i in range(100)]
# Adding one node changes only a subset; real rings use many virtual nodes for balance.
# => Check the promised observable behavior of the demonstration.
assert 0 < sum(left != right for left, right in zip(before, after)) < 100
# => Emit the final observable state for a direct run.
print("moved", sum(left != right for left, right in zip(before, after)))
