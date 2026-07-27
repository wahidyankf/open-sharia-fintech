"""Kata 8 (before): a transaction releases its write lock as soon as it finishes writing, not at commit."""

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


locks = LockManager()
locks.acquire("row-1", txn_id=1)  # txn 1 acquires the write lock and writes row-1
locks.release(
    "row-1"
)  # BUG: released immediately after the write, NOT held until commit (violates strict 2PL)

# txn 2 can now acquire the SAME row before txn 1 has committed -- a dirty read/write becomes possible
txn2_acquired_before_txn1_committed = locks.acquire("row-1", txn_id=2)
print(txn2_acquired_before_txn1_committed)
print(
    txn2_acquired_before_txn1_committed is False
)  # expected True (i.e. txn2 should NOT acquire it) under strict 2PL
