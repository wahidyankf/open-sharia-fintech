"""Example 40: Leaderless Replication, Simulated."""  # => co-13: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-13: a typed replica -- no single one is designated "the leader"


@dataclass  # => intentionally MUTABLE -- a replica's own stored value changes as writes arrive
class Replica:  # => co-13: any replica can accept a write directly -- there is no leader to route through
    name: str  # => a human-readable label, e.g. "replica-1"
    value: str | None = None  # => co-13: this replica's OWN local value, may be None if it never saw a write


def write_to_w_replicas(replicas: list[Replica], value: str, w: int) -> None:  # => co-13: ANY w of the replicas accept directly
    """Write value to the first w replicas directly -- no leader coordinates this."""  # => documents the contract
    for replica in replicas[:w]:  # => co-13: the write fans out to w replicas AT ONCE, none of them is "the" leader
        replica.value = value  # => co-13: each targeted replica accepts the write independently


def read_from_r_replicas(replicas: list[Replica], r: int) -> str | None:  # => co-13: a quorum READ reconciles what it sees
    """Read from r replicas and reconcile via simple majority-of-non-null values."""  # => documents the contract
    observed = [replica.value for replica in replicas[:r] if replica.value is not None]  # => co-13: collects whatever THESE r replicas currently hold
    if not observed:  # => none of the r replicas queried have seen a write yet
        return None  # => a genuinely empty read -- no replica in the queried set has data
    return max(observed, key=observed.count)  # => co-13: the value appearing most often among the r replicas queried wins


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    replicas = [Replica("replica-1"), Replica("replica-2"), Replica("replica-3")]  # => co-13: N=3, no replica is special

    write_to_w_replicas(replicas, "v1", w=2)  # => co-13: writes "v1" DIRECTLY to replica-1 and replica-2, W=2
    for replica in replicas:  # => prints each replica's own local state right after the write
        print(f"{replica.name}: {replica.value}")  # => Output line, one per replica -- replica-3 still None
    assert replicas[2].value is None  # => co-13: replica-3 was NOT part of the write quorum -- it has nothing yet

    read_result = read_from_r_replicas(replicas, r=2)  # => co-13: R=2 -- reads from replica-1 and replica-2, the SAME two that got the write
    # => co-13: W (2) + R (2) > N (3) -- the read quorum overlaps the write quorum, so it MUST observe v1
    assert read_result == "v1"  # => co-13: the client observes the latest write once R and W quorums overlap
    print(f"Read from {2} replicas (overlapping the write quorum): {read_result}")  # => Output: Read from 2 replicas (overlapping the write quorum): v1


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
