"""Worked Example 24: Consumer Group Assignment."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


def assign_partitions(partition_ids: list[int], member_ids: list[str]) -> dict[int, str]:  # => co-12: round-robin partition assignment
    """Assign each partition to exactly one consumer-group member, round-robin."""  # => co-12: documents assign_partitions's contract -- no runtime output, just sets its __doc__
    assignment: dict[int, str] = {}  # => co-12: partition_id -> the ONE member consuming it
    for index, partition_id in enumerate(partition_ids):  # => co-12: one partition at a time, in order
        member = member_ids[index % len(member_ids)]  # => co-12: round-robin -- cycles through members as partitions are assigned
        assignment[partition_id] = member  # => co-12: each partition maps to EXACTLY one member -- never zero, never two
    return assignment  # => co-12: returns this computed value to the caller


if __name__ == "__main__":  # => co-12: entry point -- runs only when this file executes directly, not on import
    topic_partitions = [0, 1, 2, 3, 4]  # => co-12: a five-partition topic
    consumer_group_members = ["consumer-A", "consumer-B"]  # => co-12: a two-member consumer group reading this topic
    assignment = assign_partitions(topic_partitions, consumer_group_members)  # => co-12: compute the assignment
    for partition_id, member in assignment.items():  # => co-12: one line per partition, showing its assigned member
        print(f"  partition {partition_id} -> {member}")  # => co-12: prints the assignment

    assigned_members_per_partition = {p: [m for pp, m in assignment.items() if pp == p] for p in topic_partitions}  # => co-12: every partition's member LIST
    exactly_one_each = all(len(members) == 1 for members in assigned_members_per_partition.values())  # => co-12: exactly ONE member, never zero or two
    print(f"Every partition assigned to exactly one member: {exactly_one_each}")  # => co-12: prints the check
    assert exactly_one_each, "each partition must be consumed by exactly one member of the group"  # => co-12: the claim
    assert set(assignment.values()) == set(consumer_group_members), "every member must receive at least one partition here"  # => co-12
    print(f"MATCH: {len(topic_partitions)} partitions distributed across {len(consumer_group_members)} members, one owner each")  # => co-12
    # => co-12: this exactly-one-owner property is what lets a consumer group parallelize reads without double-processing a record
