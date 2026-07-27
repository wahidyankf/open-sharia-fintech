"""Example 23: Leader-Follower Replication, Simulated."""  # => co-12: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-12: a typed follower -- its own replication log


@dataclass  # => intentionally MUTABLE -- a follower's log genuinely grows as it replicates
class Follower:  # => co-12: one follower node, receiving writes from the leader in order
    name: str  # => a human-readable label, e.g. "follower-A"
    log: list[str] = field(default_factory=list[str])  # => co-12: this follower's OWN copy of the write log, in arrival order


class Leader:  # => co-12: the single node that decides the ORDER every write is applied in
    def __init__(self, followers: list[Follower]) -> None:  # => wires up the followers this leader replicates to
        self.log: list[str] = []  # => co-12: the leader's OWN authoritative, ordered write log
        self.followers = followers  # => every follower this leader must eventually replicate to

    def write(self, value: str) -> None:  # => co-12: the leader ORDERS this write before anything else happens
        self.log.append(value)  # => co-12: appended to the leader's log FIRST -- this defines the canonical order
        for follower in self.followers:  # => co-12: replication fans out to every follower, same order every time
            follower.log.append(value)  # => co-12: each follower appends in the EXACT order the leader chose


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    follower_a = Follower("follower-A")  # => a follower that will replicate every write
    follower_b = Follower("follower-B")  # => a second, independent follower
    leader = Leader([follower_a, follower_b])  # => co-12: one leader, two followers

    for value in ["v1", "v2", "v3"]:  # => co-12: three writes, issued in this exact order
        leader.write(value)  # => the leader decides this write's position BEFORE any follower sees it

    print(f"Leader log:     {leader.log}")  # => Output: Leader log:     ['v1', 'v2', 'v3']
    print(f"Follower-A log: {follower_a.log}")  # => Output: Follower-A log: ['v1', 'v2', 'v3']
    print(f"Follower-B log: {follower_b.log}")  # => Output: Follower-B log: ['v1', 'v2', 'v3']

    assert follower_a.log == leader.log  # => co-12: follower-A converged to the LEADER's exact write order
    assert follower_b.log == leader.log  # => co-12: follower-B converged to the SAME order, independently
    print("Both followers converged to the leader's exact write order")  # => Output: Both followers converged to the leader's exact write order


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
