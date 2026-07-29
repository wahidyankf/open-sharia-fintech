# pyright: strict
"""Kata 5 (after): the outbox message is written IN the same transaction."""

from dataclasses import dataclass, field


@dataclass
class Service:
    db: list[str] = field(default_factory=list[str])
    outbox: list[str] = field(default_factory=list[str])
    committed: bool = False

    def place_order(self, order: str, fail_before_commit: bool = False) -> None:
        # THE FIX: stage BOTH writes, then commit them together -- atomic.
        staged_db = order
        staged_outbox = f"event:{order}"
        if fail_before_commit:  # a failure before commit rolls back BOTH -> nothing lost, nothing sent
            self.committed = False
            return
        self.db.append(staged_db)  # commit business + outbox TOGETHER
        self.outbox.append(staged_outbox)  # sent iff the transaction commits
        self.committed = True


committed = Service()
committed.place_order("order-X")  # both commit together
rolled_back = Service()
rolled_back.place_order("order-Y", fail_before_commit=True)  # rollback -> neither survives
print(f"committed: db={committed.db}, outbox={committed.outbox}")  # both present
print(f"rolled back: db={rolled_back.db}, outbox={rolled_back.outbox}")  # both empty
assert committed.db == ["order-X"] and committed.outbox == ["event:order-X"]
assert rolled_back.db == [] and rolled_back.outbox == []
