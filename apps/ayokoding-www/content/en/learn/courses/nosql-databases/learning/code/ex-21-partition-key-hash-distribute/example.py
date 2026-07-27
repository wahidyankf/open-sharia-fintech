"""Example 21: Partition Key Hash Distribution."""  # => co-10: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import hashlib  # => co-10: a stable, deterministic hash -- Python's built-in hash() varies process to process


def bucket_for_key(key: str, bucket_count: int) -> int:  # => co-10: the simplest possible partitioning function
    """Return which of bucket_count buckets a key hashes into, via mod-hash."""  # => documents the contract
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()  # => co-10: a stable 256-bit digest, same input always yields the same output
    numeric = int(digest, 16)  # => converts the hex digest to a plain integer for the modulo below
    return numeric % bucket_count  # => co-10: the classic mod-hash partitioning scheme -- key -> bucket_count buckets


KEYS = ["user:1", "user:2", "user:3", "user:4", "user:5"]  # => co-10: 5 partition keys to distribute
BUCKET_COUNT = 4  # => co-10: simulates 4 nodes/shards sharing the load


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    distribution: dict[int, list[str]] = {b: [] for b in range(BUCKET_COUNT)}  # => co-10: one list per bucket, starts empty
    for key in KEYS:  # => co-10: assigns EVERY key to exactly one bucket
        bucket = bucket_for_key(key, BUCKET_COUNT)  # => runs the mod-hash for this one key
        distribution[bucket].append(key)  # => records which bucket this key landed in

    for bucket, keys_here in distribution.items():  # => co-10: prints the resulting spread, bucket by bucket
        print(f"bucket {bucket}: {keys_here}")  # => Output (4 lines, one per bucket, e.g. bucket 0: ['user:3'] / bucket 1: ['user:1', 'user:5'] / ...)
    max_bucket_size = max(len(keys_here) for keys_here in distribution.values())  # => co-10: the single most-loaded bucket
    assert max_bucket_size <= 2  # => co-10: roughly even -- no bucket gets more than 2 of the 5 keys
    print(f"Max bucket load: {max_bucket_size} of {len(KEYS)} keys -- roughly even distribution")  # => Output: Max bucket load: 2 of 5 keys -- roughly even distribution


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
