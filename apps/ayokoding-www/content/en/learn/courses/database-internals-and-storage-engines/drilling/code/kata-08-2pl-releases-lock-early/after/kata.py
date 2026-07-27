"""Kata 8 (after): the write lock is held until an explicit commit() -- strict 2PL's defining rule."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LockManager:
    held_by: dict[str, int] = field(default_factory=dict[str, int])

    def acquire(self, key: str, txn_id: int) -> bool:
        if key in self.held_by and self.held_by[key] != txn_id:
            return False
        self.held_by[key] = txn_id
        return True

    def release(self, key: str) -> None:
        self.held_by.pop(key, None)


class StrictTwoPhaseTxn:
    def __init__(self, locks: LockManager, txn_id: int) -> None:
        self.locks = locks
        self.txn_id = txn_id
        self.held_keys: list[str] = []

    def write(self, key: str) -> bool:
        if not self.locks.acquire(key, self.txn_id):
            return False
        self.held_keys.append(
            key
        )  # => the lock is tracked, NOT released, until commit()
        return True

    def commit(self) -> None:
        for key in (
            self.held_keys
        ):  # => co-25: strict 2PL releases every lock only AT commit, all at once
            self.locks.release(key)
        self.held_keys.clear()


locks = LockManager()
txn1 = StrictTwoPhaseTxn(locks, txn_id=1)
txn1.write("row-1")
txn2_acquired_before_txn1_committed = locks.acquire(
    "row-1", txn_id=2
)  # txn1 has NOT committed yet
print(txn2_acquired_before_txn1_committed)
print(txn2_acquired_before_txn1_committed is False)
