from hashlib import sha256


def point(value: str) -> int:
    # A stable digest gives names and keys the same coordinate space.
    return int(sha256(value.encode()).hexdigest(), 16)


def owner(nodes: list[str], key: str) -> str:
    # Sort nodes by their ring position before finding the clockwise successor.
    ring = sorted((point(node), node) for node in nodes)
    # Wrap to the first node when a key lies beyond the last coordinate.
    return next((node for location, node in ring if point(key) <= location), ring[0][1])


before = [owner(["a", "b", "c"], f"key-{i}") for i in range(100)]
after = [owner(["a", "b", "c", "d"], f"key-{i}") for i in range(100)]
# Adding one node changes only a subset; real rings use many virtual nodes for balance.
assert 0 < sum(left != right for left, right in zip(before, after)) < 100
print("moved", sum(left != right for left, right in zip(before, after)))
