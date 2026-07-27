"""Example 41: Last-Write-Wins Conflict Resolution."""  # => co-14: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-14: a typed write -- pairs a value with the timestamp LWW resolves by


@dataclass(frozen=True)  # => frozen -- a write, once issued, is an immutable historical fact
class TimestampedWrite:  # => co-14: exactly what LWW needs to pick a winner -- a value and when it happened
    value: str  # => the data this write attempted to set
    timestamp: float  # => co-14: the deciding factor -- a later timestamp always wins, regardless of arrival order


def resolve_lww(writes: list[TimestampedWrite]) -> TimestampedWrite:  # => co-14: picks the single winner among concurrent writes
    """Resolve concurrent writes to the same key by last-write-wins, on timestamp alone."""  # => documents the contract
    return max(writes, key=lambda w: w.timestamp)  # => co-14: the LATEST timestamp wins -- every other write is SILENTLY dropped


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    # Two clients write to the SAME key concurrently -- neither saw the other's write before sending.
    write_from_client_a = TimestampedWrite(value="blue", timestamp=1000.5)  # => co-14: client A's write, timestamped first
    write_from_client_b = TimestampedWrite(value="green", timestamp=1000.9)  # => co-14: client B's write, timestamped LATER

    winner = resolve_lww([write_from_client_a, write_from_client_b])  # => co-14: LWW resolves the two concurrent writes to ONE value
    assert winner.value == "green"  # => co-14: the later timestamp (1000.9 > 1000.5) wins -- "blue" is silently dropped
    print(f"LWW winner: {winner.value} (timestamp={winner.timestamp})")  # => Output: LWW winner: green (timestamp=1000.9)
    print(f"Dropped silently: {write_from_client_a.value} (timestamp={write_from_client_a.timestamp}) -- NO merge, NO error raised")  # => Output line
    # => co-14: this is LWW's real cost -- client A's "blue" write is GONE, with no record it ever
    # => existed and no error surfaced to client A that its write lost -- the tradeoff for a
    # => cheap, deterministic, coordination-free conflict resolution rule


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
