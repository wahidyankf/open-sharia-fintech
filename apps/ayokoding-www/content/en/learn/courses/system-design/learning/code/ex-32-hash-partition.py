# => Use the standard-library helper required by this runnable model.
from hashlib import sha256


# => Isolate the operation so its observable behavior can be checked.
def shard(identifier: int, count: int = 4) -> int:
    # A stable hash removes the sequential pattern from the partition choice.
    # => Return the observable result of this modeled operation.
    return int(sha256(str(identifier).encode()).hexdigest(), 16) % count


# => Initialize or update deterministic state used by this demonstration.
counts = [
    # => Initialize or update deterministic state used by this demonstration.
    sum(shard(identifier) == index for identifier in range(1_000))
    for index in range(4)
    # => Initialize or update deterministic state used by this demonstration.
]
# Every shard gets keys; exact equality is neither expected nor required.
# => Check the promised observable behavior of the demonstration.
assert all(count > 150 for count in counts)
# => Emit the final observable state for a direct run.
print(counts)
