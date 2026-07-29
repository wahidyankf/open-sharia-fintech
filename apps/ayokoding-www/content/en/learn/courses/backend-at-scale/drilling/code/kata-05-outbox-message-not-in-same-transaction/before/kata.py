# pyright: strict
"""Kata 5 (before): the outbox message is written OUTSIDE the transaction (dual-write)."""

from dataclasses import dataclass, field


@dataclass
class Service:
    db: list[str] = field(default_factory=list[str])
    outbox: list[str] = field(default_factory=list[str])
    committed: bool = False

    def place_order(self, order: str, fail_after_db: bool = False) -> None:
        # THE BUG: the DB write and the outbox write are NOT in the same transaction.
        self.db.append(order)  # committed independently
        if fail_after_db:  # a crash here loses the message -- this is the dual-write problem
            return  # DB has the order, outbox is EMPTY -> the event is lost
        self.outbox.append(f"event:{order}")  # written separately -- NOT atomic with the DB write


crashed = Service()
crashed.place_order("order-X", fail_after_db=True)  # crash between DB and outbox
print(f"after crash: db={crashed.db}, outbox={crashed.outbox}")  # BUG: event lost
