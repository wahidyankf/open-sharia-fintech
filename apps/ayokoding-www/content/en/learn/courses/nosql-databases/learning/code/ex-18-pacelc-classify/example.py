"""Example 18: Classify by PACELC."""  # => co-04: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-04: a typed record pairing the CAP lean with the ELSE-branch lean
from enum import Enum, auto  # => co-04: PA/PC and EL/EC as checkable types, not bare strings


class DuringPartition(Enum):  # => co-03: the SAME P-branch classification Example 17 already computed
    PA = auto()  # => Partitioned -> Available: answers anyway, possibly stale
    PC = auto()  # => Partitioned -> Consistent: refuses rather than risk stale data


class ElseBranch(Enum):  # => co-04: PACELC's own addition -- the tradeoff when there is NO partition at all
    EL = auto()  # => Else -> Latency: favors a fast answer even without a partition
    EC = auto()  # => Else -> Consistency: favors waiting for full replica agreement even without a partition


@dataclass(frozen=True)  # => frozen -- a PACELC classification is a stated fact, not something later code edits
class PacelcClassification:  # => co-04: the full four-letter label PACELC gives a distributed store
    store_config: str  # => which SPECIFICALLY configured store this classification describes
    partition_lean: DuringPartition  # => co-03: reused directly from Example 17's own CAP classification
    else_lean: ElseBranch  # => co-04: the new axis -- latency vs. consistency absent any partition


CLASSIFICATIONS = [  # => co-04: extends Example 17's three configs with the ELSE-branch axis
    PacelcClassification("MongoDB (majority write concern)", DuringPartition.PC, ElseBranch.EC),  # => waits for majority ack even with no partition
    PacelcClassification("Cassandra (QUORUM/QUORUM)", DuringPartition.PC, ElseBranch.EC),  # => quorum coordination costs latency even absent a partition
    PacelcClassification("DynamoDB (eventually-consistent reads)", DuringPartition.PA, ElseBranch.EL),  # => favors fast reads over waiting for full replica sync
]  # => 3 configs, each carrying BOTH a partition-branch lean AND an else-branch lean -- 2 axes, not 1


def label(classification: PacelcClassification) -> str:  # => builds the canonical 4-letter PACELC label
    """Return the 4-letter PACELC label, e.g. PC/EC or PA/EL."""  # => documents the contract, no runtime output
    return f"{classification.partition_lean.name}/{classification.else_lean.name}"  # => co-04: e.g. "PC/EC" or "PA/EL"


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    for c in CLASSIFICATIONS:  # => co-04: labels every configured store from the table above
        print(f"{c.store_config}: {label(c)}")  # => Output: MongoDB (...): PC/EC / Cassandra (...): PC/EC / DynamoDB (...): PA/EL
    assert label(CLASSIFICATIONS[0]) == "PC/EC"  # => co-04: MongoDB's majority write concern costs latency even with no partition
    assert label(CLASSIFICATIONS[2]) == "PA/EL"  # => co-04: DynamoDB's default favors speed on BOTH axes


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
