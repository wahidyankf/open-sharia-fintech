"""Example 20: Simulate Eventual Consistency."""  # => co-06: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-06: a typed replica -- its own value plus a queue of pending updates


@dataclass  # => intentionally MUTABLE -- a replica's value genuinely changes over time as writes replicate in
class Replica:  # => co-06: one node's own view of a single key's value
    name: str  # => a human-readable label, e.g. "replica-A"
    value: str  # => this replica's CURRENT view -- may lag behind the true latest write
    inbox: list[str] = field(default_factory=list)  # => co-06: writes that have not yet been applied to this replica


def write_to_leader(replicas: list[Replica], new_value: str) -> None:  # => co-06: the write lands on replica[0] immediately
    """Apply a write to the first replica immediately; queue it for the rest."""  # => documents the contract
    replicas[0].value = new_value  # => co-06: the write's OWN replica sees it instantly -- no delay for the writer itself
    for replica in replicas[1:]:  # => co-06: every OTHER replica has not seen this write yet
        replica.inbox.append(new_value)  # => co-06: queued, simulating asynchronous replication lag


def replicate_pending(replicas: list[Replica]) -> None:  # => co-06: simulates the delayed propagation actually landing
    """Drain each replica's inbox, applying its queued writes in order."""  # => documents the contract
    for replica in replicas[1:]:  # => the leader (replica[0]) has no inbox to drain -- it wrote directly
        for pending_value in replica.inbox:  # => co-06: applies EVERY queued write, in the order it was queued
            replica.value = pending_value  # => co-06: catches this replica up to the leader's latest state
        replica.inbox.clear()  # => the queue is now empty -- this replica has converged


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    replicas = [Replica("leader", "v0"), Replica("follower-A", "v0"), Replica("follower-B", "v0")]  # => 3 replicas, all agreeing at v0
    write_to_leader(replicas, "v1")  # => co-06: a single write -- the leader updates instantly, followers do not yet

    stale_read = replicas[1].value  # => co-06: reading follower-A RIGHT AFTER the write, before replication lands
    assert stale_read == "v0"  # => co-06: a genuinely STALE read -- the follower has not caught up yet
    print(f"Immediately after write: leader={replicas[0].value} follower-A={stale_read} (stale)")  # => Output: Immediately after write: leader=v1 follower-A=v0 (stale)

    replicate_pending(replicas)  # => co-06: simulates the replication delay finally elapsing
    converged_read = replicas[1].value  # => reading follower-A again, now that replication has landed
    assert converged_read == "v1"  # => co-06: eventual consistency's promise kept -- the follower converged to the leader's value
    print(f"After replication settles: leader={replicas[0].value} follower-A={converged_read} (converged)")  # => Output: After replication settles: leader=v1 follower-A=v1 (converged)


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
