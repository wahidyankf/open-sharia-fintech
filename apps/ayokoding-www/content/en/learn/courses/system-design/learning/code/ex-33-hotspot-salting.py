# => Use the standard-library helper required by this runnable model.
from hashlib import sha256


# => Isolate the operation so its observable behavior can be checked.
def bucket(event_id: int, shards: int = 8) -> int:
    # An event-specific suffix spreads one celebrity's independent increments.
    # => Initialize or update deterministic state used by this demonstration.
    digest = sha256(f"celebrity:{event_id}".encode()).hexdigest()
    # => Return the observable result of this modeled operation.
    return int(digest, 16) % shards


# => Initialize or update deterministic state used by this demonstration.
used = {bucket(event_id) for event_id in range(100)}
# Several sub-partitions replace the one-key write hotspot.
# => Check the promised observable behavior of the demonstration.
assert len(used) > 1
# => Emit the final observable state for a direct run.
print(sorted(used))
