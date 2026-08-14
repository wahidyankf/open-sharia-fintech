from hashlib import sha256


def shard(identifier: int, count: int = 4) -> int:
    # A stable hash removes the sequential pattern from the partition choice.
    return int(sha256(str(identifier).encode()).hexdigest(), 16) % count


counts = [
    sum(shard(identifier) == index for identifier in range(1_000)) for index in range(4)
]
# Every shard gets keys; exact equality is neither expected nor required.
assert all(count > 150 for count in counts)
print(counts)
