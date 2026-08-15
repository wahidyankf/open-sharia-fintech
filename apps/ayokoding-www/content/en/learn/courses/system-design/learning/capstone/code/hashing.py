from hashlib import sha256


def locate(nodes: list[str], key: str) -> str:
    # A stable digest keeps the placement answer deterministic across processes.
    key_point = int(sha256(key.encode()).hexdigest(), 16)
    ring = sorted((int(sha256(node.encode()).hexdigest(), 16), node) for node in nodes)
    # The first clockwise node owns the key, with wraparound at the end of the ring.
    return next((node for point, node in ring if key_point <= point), ring[0][1])


before = [locate(["a", "b", "c"], f"key-{index}") for index in range(100)]
after = [locate(["a", "b", "c", "d"], f"key-{index}") for index in range(100)]
# A new node moves some, but not all, keys; virtual nodes improve real-world balance.
assert 0 < sum(left != right for left, right in zip(before, after)) < 100
print("capstone ring passed")
