"""Example 54: DynamoDB ConsistentRead Toggle, Simulated."""  # => co-06,co-07: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-06: a typed replica set standing in for DynamoDB's own multi-AZ replicas

# NOTE (honesty, per this topic's own no-fabrication rule): amazon/dynamodb-local runs as a SINGLE
# local process with no real inter-replica lag, so ConsistentRead=False and ConsistentRead=True return
# the IDENTICAL result on it every time -- there is no staleness window to observe locally. This
# example instead simulates real DynamoDB's DOCUMENTED behavior (an eventually-consistent read MAY hit
# a replica that has not yet applied the latest write; a strongly consistent read always reads the
# leader/up-to-date copy) with a toy multi-replica model, the same honest-simulation technique
# Example 20 already used for eventual consistency in general.


@dataclass  # => intentionally MUTABLE -- a replica's own value changes as writes replicate in
class Replica:  # => co-06: one of DynamoDB's internal replicas for a partition (not user-visible directly)
    name: str  # => a human-readable label, e.g. "replica-1"
    value: str  # => this replica's CURRENT view of the item -- may lag the true latest write


class SimulatedDynamoTable:  # => co-07: models GetItem's two ConsistentRead modes over a lagging replica set
    def __init__(self) -> None:  # => builds a 3-replica table, all starting in agreement
        self.replicas = [Replica("replica-1", "v0"), Replica("replica-2", "v0"), Replica("replica-3", "v0")]  # => co-06: 3 replicas, DynamoDB's real internal default

    def put_item(self, value: str) -> None:  # => co-07: the leader replica updates instantly; the others lag
        self.replicas[0].value = value  # => co-06: the write's OWN leader replica applies it immediately
        # => replicas[1] and replicas[2] are deliberately left UN-replicated here, simulating the real
        # => propagation delay a strongly consistent read is specifically designed to bypass

    def get_item(self, consistent_read: bool) -> str:  # => co-07: the SAME item, read two different ways
        if consistent_read:  # => co-07: ConsistentRead=True -- DynamoDB always routes to the up-to-date leader replica
            return self.replicas[0].value  # => co-07: strongly consistent -- CANNOT observe a stale value
        return self.replicas[1].value  # => co-07: ConsistentRead=False (the default) -- MAY hit a replica that has not caught up yet

    def replicate(self) -> None:  # => co-06: simulates replication lag finally elapsing
        for replica in self.replicas[1:]:  # => catches every follower replica up to the leader's value
            replica.value = self.replicas[0].value  # => co-06: convergence, exactly as Example 20 modeled


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    table = SimulatedDynamoTable()  # => co-06: a fresh, fully-converged 3-replica table
    table.put_item("v1")  # => co-07: a write lands on the leader replica; the eventually-consistent replica has NOT caught up yet

    eventual_read = table.get_item(consistent_read=False)  # => co-07: ConsistentRead=False -- reads the LAGGING replica
    assert eventual_read == "v0"  # => co-07: a genuinely STALE read -- the eventually-consistent path can observe the OLD value
    print(f"ConsistentRead=False right after the write: {eventual_read} (may be stale)")  # => Output: ConsistentRead=False right after the write: v0 (may be stale)

    strong_read = table.get_item(consistent_read=True)  # => co-07: ConsistentRead=True -- ALWAYS reads the up-to-date leader
    assert strong_read == "v1"  # => co-07: strongly consistent -- CANNOT observe a stale value, by construction
    print(f"ConsistentRead=True right after the write:  {strong_read} (never stale)")  # => Output: ConsistentRead=True right after the write:  v1 (never stale)

    table.replicate()  # => co-06: simulates the replication delay finally elapsing
    converged_read = table.get_item(consistent_read=False)  # => reads the ONCE-lagging replica again, now caught up
    assert converged_read == "v1"  # => co-06: eventual consistency's promise kept -- the lagging replica converged
    print(f"ConsistentRead=False after replication settles: {converged_read} (converged)")  # => Output: ConsistentRead=False after replication settles: v1 (converged)


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
