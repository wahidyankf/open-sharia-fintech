from collections import Counter
from hashlib import sha256


def point(value: str) -> int:
    # The same hash function lets virtual nodes and keys share positions.
    return int(sha256(value.encode()).hexdigest(), 16)


def owner(nodes: list[str], key: str, replicas: int = 32) -> str:
    # Several positions per physical node make each node own smaller intervals.
    ring = sorted(
        (point(f"{node}:{replica}"), node)
        for node in nodes
        for replica in range(replicas)
    )
    # The first clockwise position owns the key.
    return next((node for location, node in ring if point(key) <= location), ring[0][1])


counts = Counter(owner(["a", "b", "c"], f"key-{i}") for i in range(300))
# Each physical node receives work; variance is expected but no node is absent.
assert set(counts) == {"a", "b", "c"}
print(dict(counts))
