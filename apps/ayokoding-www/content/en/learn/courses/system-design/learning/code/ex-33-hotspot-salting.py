from hashlib import sha256


def bucket(event_id: int, shards: int = 8) -> int:
    # An event-specific suffix spreads one celebrity's independent increments.
    digest = sha256(f"celebrity:{event_id}".encode()).hexdigest()
    return int(digest, 16) % shards


used = {bucket(event_id) for event_id in range(100)}
# Several sub-partitions replace the one-key write hotspot.
assert len(used) > 1
print(sorted(used))
