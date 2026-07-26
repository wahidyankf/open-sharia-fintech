"""Kata 5 (before): commit() flips the committed flag but never materializes the write into storage."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WalRecord:
    txn_id: int
    key: str
    value: str
    committed: bool = False


@dataclass
class Engine:
    log: list[WalRecord] = field(default_factory=list[WalRecord])
    table: dict[str, str] = field(default_factory=dict[str, str])

    def append(self, txn_id: int, key: str, value: str) -> None:
        self.log.append(WalRecord(txn_id=txn_id, key=key, value=value))

    def commit(self, txn_id: int) -> None:
        for record in self.log:
            if record.txn_id == txn_id:
                record.committed = (
                    True  # BUG: marks committed but never writes into self.table
                )

    def read(self, key: str) -> str | None:
        return self.table.get(key)


engine = Engine()
engine.append(txn_id=1, key="a", value="v1")
engine.commit(txn_id=1)
print(
    engine.read("a")
)  # expected "v1" -- a committed write should be immediately readable
