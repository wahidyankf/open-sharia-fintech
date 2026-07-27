"""Example 74: Replication Leader-Follower Failover, Simulated."""  # => co-12: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-12: a typed follower, extended from Example 23's own model


@dataclass  # => intentionally MUTABLE -- a follower's log genuinely grows as it replicates
class Node:  # => co-12: any node can be EITHER a leader or a follower, depending on cluster state
    name: str  # => a human-readable label, e.g. "node-A"
    log: list[str] = field(default_factory=list)  # => this node's own copy of the write log, in arrival order
    is_leader: bool = False  # => co-12: exactly ONE node in the cluster should be True at any given time


class ReplicatedCluster:  # => co-12: models leader-follower replication PLUS a leader failure and promotion
    def __init__(self, node_names: list[str]) -> None:  # => builds a cluster with the first node as leader
        self.nodes = [Node(name) for name in node_names]  # => co-12: every named node, none failed yet
        self.nodes[0].is_leader = True  # => co-12: the first node starts as leader -- an arbitrary but explicit initial choice

    @property  # => co-12: reads like a plain attribute, but re-scans the cluster's own live state each call
    def leader(self) -> Node | None:  # => co-12: finds whichever node currently holds is_leader=True, or None during an outage
        for node in self.nodes:  # => scans for the CURRENT leader -- there is at most one at any time
            if node.is_leader:  # => co-12: found it
                return node  # => co-12: stops scanning as soon as the current leader is found
        return None  # => co-12: NO leader currently exists -- the cluster is mid-failover, writes cannot be accepted

    def write(self, value: str) -> bool:  # => co-12: returns True if the write succeeded, False if there was no leader to accept it
        """Write a value through the current leader, if one exists; replicate to all followers."""  # => documents the contract
        leader = self.leader  # => co-12: finds the current leader, or None
        if leader is None:  # => co-12: NO leader means writes are REJECTED -- this is the availability gap during failover
            return False  # => co-12: the write genuinely failed -- there was nowhere to route it
        leader.log.append(value)  # => co-12: the leader orders this write BEFORE any follower sees it
        for node in self.nodes:  # => co-12: replication fans out to every OTHER node
            if node is not leader:  # => skips re-appending to the leader's own log
                node.log.append(value)  # => co-12: each follower replicates, in the SAME order the leader chose
        return True  # => the write succeeded

    def fail_leader(self) -> None:  # => co-12: simulates the current leader going down -- NO node is leader afterward
        """Simulate the current leader failing -- no node is leader until promote_new_leader runs."""  # => documents the contract
        leader = self.leader  # => finds the currently failing leader
        if leader is not None:  # => guards against calling this when there is already no leader
            leader.is_leader = False  # => co-12: the failed node is no longer the leader -- an availability GAP begins here

    def promote_new_leader(self, node_name: str) -> None:  # => co-12: a follower is promoted, ending the availability gap
        """Promote the named node to leader, ending the availability gap."""  # => documents the contract
        for node in self.nodes:  # => finds the node being promoted
            if node.name == node_name:  # => this is the node the caller chose to promote
                node.is_leader = True  # => co-12: the availability gap ends -- writes can resume through this new leader


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    cluster = ReplicatedCluster(["node-A", "node-B", "node-C"])  # => co-12: node-A starts as leader
    assert cluster.write("v1")  # => co-12: succeeds -- node-A is leader, accepts and replicates the write
    print(f"Write v1 via leader node-A: succeeded = True, all logs = {[n.log for n in cluster.nodes]}")  # => Output: Write v1 via leader node-A: succeeded = True, all logs = [['v1'], ['v1'], ['v1']]

    cluster.fail_leader()  # => co-12: node-A (the leader) fails -- an availability gap begins
    write_during_outage_succeeded = cluster.write("v2-during-outage")  # => co-12: attempted DURING the gap, with NO leader
    assert write_during_outage_succeeded is False  # => co-12: correctly rejected -- there is no leader to accept it, a genuine availability gap
    print(f"Write attempted during outage (no leader): succeeded = {write_during_outage_succeeded}")  # => Output: Write attempted during outage (no leader): succeeded = False

    cluster.promote_new_leader("node-B")  # => co-12: node-B is promoted -- the availability gap ends here
    assert cluster.write("v3-after-failover")  # => co-12: succeeds -- node-B is now leader, writes resume
    node_b = next(n for n in cluster.nodes if n.name == "node-B")  # => finds node-B to inspect its log directly
    assert node_b.log == ["v1", "v3-after-failover"]  # => co-12: node-B's log has v1 (replicated before the outage) PLUS the new write -- v2 never happened
    print(f"Write v3 via new leader node-B: succeeded = True, node-B log = {node_b.log}")  # => Output: Write v3 via new leader node-B: succeeded = True, node-B log = ['v1', 'v3-after-failover']
    print("Availability gap: exactly one write (v2-during-outage) was rejected during the leaderless window between failure and promotion")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
