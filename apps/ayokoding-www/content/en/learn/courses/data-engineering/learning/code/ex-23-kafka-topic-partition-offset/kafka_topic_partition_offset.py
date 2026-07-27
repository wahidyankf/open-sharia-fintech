"""Worked Example 23: Kafka Topic -- Partitions of an Append-Only Log."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-12: models one Kafka record and one partition's append-only log


@dataclass  # => co-12: one immutable-once-appended record, matching a real Kafka record's shape
class Record:  # => co-12: a single appended record within one partition
    offset: int  # => co-12: this record's position within ITS partition -- monotonic, assigned on append
    key: str  # => co-12: the record's key -- would drive partition assignment in a real producer
    value: str  # => co-12: the record's payload


@dataclass  # => co-12: a topic modeled as SEVERAL independent partitions, each its own append-only log
class Partition:  # => co-12: one partition -- an append-only log with its own offset counter
    partition_id: int  # => co-12: which partition this is, within the topic
    log: list[Record] = field(default_factory=list)  # => co-12: the append-only log itself -- a plain, growing list

    def append(self, key: str, value: str) -> Record:  # => co-12: the ONLY way a record enters this partition
        """Append a new record, assigning it the next monotonic offset for THIS partition."""  # => co-12: documents append's contract -- no runtime output, just sets its __doc__
        next_offset = len(self.log)  # => co-12: offsets are 0-indexed and monotonic PER PARTITION -- not shared across partitions
        record = Record(offset=next_offset, key=key, value=value)  # => co-12: assign the offset at append time, never earlier
        self.log.append(record)  # => co-12: APPEND-only -- nothing already in the log is ever modified or removed
        return record  # => co-12: returns this computed value to the caller


if __name__ == "__main__":  # => co-12: entry point -- runs only when this file executes directly, not on import
    topic_orders = [Partition(partition_id=0), Partition(partition_id=1)]  # => co-12: a topic modeled as TWO independent partitions
    appended = [  # => co-12: append five records, alternating which partition receives each one
        topic_orders[0].append("order-1", "created"),  # => co-12: partition 0, offset 0
        topic_orders[1].append("order-2", "created"),  # => co-12: partition 1, offset 0 -- ITS OWN independent counter
        topic_orders[0].append("order-1", "shipped"),  # => co-12: partition 0, offset 1
        topic_orders[1].append("order-2", "shipped"),  # => co-12: partition 1, offset 1
        topic_orders[0].append("order-3", "created"),  # => co-12: partition 0, offset 2
    ]  # => co-12: closes appended -- five records total, across two partitions

    for record in appended:  # => co-12: one line per appended record, showing which partition + offset it landed at
        print(f"  appended {record.key}:{record.value} -> offset {record.offset}")  # => co-12: prints each append's assigned offset

    partition_0_offsets = [r.offset for r in topic_orders[0].log]  # => co-12: partition 0's own offset sequence
    partition_1_offsets = [r.offset for r in topic_orders[1].log]  # => co-12: partition 1's own, INDEPENDENT offset sequence
    print(f"Partition 0 offsets: {partition_0_offsets} | Partition 1 offsets: {partition_1_offsets}")  # => co-12
    assert partition_0_offsets == [0, 1, 2], "partition 0's offsets must be monotonic and start at 0"  # => co-12: the claim
    assert partition_1_offsets == [0, 1], "partition 1's offsets must ALSO be monotonic and start at 0, independently"  # => co-12
    print("MATCH: each partition assigns its own monotonic, per-partition offset -- offsets are NOT shared across partitions")  # => co-12
    # => co-12: a Kafka topic is a set of independent append-only logs, each with its own offset sequence -- never one global counter
