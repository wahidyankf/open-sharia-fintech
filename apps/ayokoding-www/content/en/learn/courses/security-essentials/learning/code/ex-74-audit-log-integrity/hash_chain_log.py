# learning/code/ex-74-audit-log-integrity/hash_chain_log.py
"""Example 74: a real hash-chained append-only log -- tampering with ONE past entry breaks a real verification pass (co-22)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the hash-chaining logic itself

import hashlib  # => co-22: real SHA-256 -- the same primitive a real blockchain-style chain uses
from dataclasses import (
    dataclass,
    field,
)  # => co-22: a real, typed log-entry record -- not a loose dict

GENESIS_HASH = (
    "0" * 64
)  # => co-22: a real, fixed sentinel -- the "previous hash" the FIRST entry chains from


@dataclass  # => co-22: one real entry per audit event -- content plus the real chain-linking fields
class LogEntry:  # => co-22: the shape every real entry in this log takes
    index: int  # => co-22: this entry's real, sequential position in the chain
    content: str  # => co-22: the REAL audit event text -- what an attacker might try to alter
    prev_hash: str  # => co-22: the REAL hash of the entry immediately before this one -- the actual "chain" link
    entry_hash: str = field(
        default=""
    )  # => co-22: THIS entry's own real hash, computed once and never recomputed


def compute_hash(
    index: int, content: str, prev_hash: str
) -> str:  # => co-22: the ONE real hash function every entry uses
    payload = (
        f"{index}|{content}|{prev_hash}".encode()
    )  # => co-22: real, deterministic serialization -- order matters
    return hashlib.sha256(
        payload
    ).hexdigest()  # => co-22: a real SHA-256 digest -- the SAME algorithm, every call


class HashChainedLog:  # => co-22: a real, append-only log -- entries are added, never mutated through this API
    def __init__(
        self,
    ) -> None:  # => co-22: constructor -- starts with a real, empty chain
        self.entries: list[
            LogEntry
        ] = []  # => co-22: every real entry appended so far, in real chain order

    def append(
        self, content: str
    ) -> LogEntry:  # => co-22: the ONLY real way to add to this log
        prev_hash = (
            self.entries[-1].entry_hash if self.entries else GENESIS_HASH
        )  # => co-22: real link to the PRIOR entry
        index = len(
            self.entries
        )  # => co-22: this entry's real, sequential index -- next available slot
        entry_hash = compute_hash(
            index, content, prev_hash
        )  # => co-22: a REAL hash, computed from THIS entry's real data
        entry = LogEntry(
            index=index, content=content, prev_hash=prev_hash, entry_hash=entry_hash
        )  # => co-22: real record
        self.entries.append(
            entry
        )  # => co-22: real, append-only -- this list is the log's actual, on-disk-equivalent state
        return entry  # => co-22: the real, freshly-chained entry just added

    def verify(
        self,
    ) -> tuple[
        bool, int | None
    ]:  # => co-22: a REAL chain-verification pass -- recomputes every real hash
        prev_hash = GENESIS_HASH  # => co-22: starts from the SAME real sentinel the first entry chained from
        for (
            entry
        ) in self.entries:  # => co-22: walks the REAL chain, in order, entry by entry
            recomputed = compute_hash(
                entry.index, entry.content, prev_hash
            )  # => co-22: a FRESH, real hash of CURRENT content
            if (
                entry.prev_hash != prev_hash or entry.entry_hash != recomputed
            ):  # => co-22: the REAL, two-part integrity check
                return (
                    False,
                    entry.index,
                )  # => co-22: real, precise failure location -- exactly WHICH entry broke the chain
            prev_hash = entry.entry_hash  # => co-22: advances the real chain -- THIS entry's stored hash feeds the next
        return (
            True,
            None,
        )  # => co-22: every real entry's stored hash matched its freshly recomputed hash -- chain intact


def main() -> (
    None
):  # => co-22: builds a real log, verifies it intact, tampers with ONE entry, then re-verifies
    log = HashChainedLog()  # => co-22: a fresh, real, empty audit log
    log.append("user=alice action=login outcome=success")  # => co-22: real entry 0
    log.append(
        "user=alice action=view_document outcome=success"
    )  # => co-22: real entry 1
    log.append(
        "user=bob action=login outcome=failure"
    )  # => co-22: real entry 2 -- the one this example later tampers with
    log.append("user=alice action=logout outcome=success")  # => co-22: real entry 3

    print("=== the real, untampered chain ===")  # => labels section
    for entry in log.entries:  # => co-22: every REAL entry currently in this log
        print(
            f"  [{entry.index}] {entry.content}  hash={entry.entry_hash[:12]}..."
        )  # => co-22: real, truncated hash
    ok, broken_at = (
        log.verify()
    )  # => co-22: a REAL verification pass over the untouched chain
    print(
        f"verify() -> ok={ok}, broken_at={broken_at}"
    )  # => co-22: real, computed result
    assert (
        ok and broken_at is None
    )  # => co-22: proves the real, freshly-built chain is genuinely intact

    print(
        "\n=== tampering with entry 2's content DIRECTLY (attacker edits the record, not the hash) ==="
    )  # => labels
    log.entries[
        2
    ].content = "user=bob action=login outcome=success"  # => co-22: the REAL attack -- changes failure to success
    # => co-22: note the attacker did NOT recompute entry_hash -- that is exactly what makes
    # => this detectable; a real attacker who wanted to hide this would need to recompute
    # => EVERY subsequent entry's hash too, which this simple tamper does not attempt

    print("\n=== re-verifying the SAME chain after tampering ===")  # => labels section
    ok2, broken_at2 = (
        log.verify()
    )  # => co-22: a REAL verification pass -- recomputes every real hash fresh
    print(
        f"verify() -> ok={ok2}, broken_at={broken_at2}"
    )  # => co-22: real, computed result -- now False
    assert (
        ok2 is False and broken_at2 == 2
    )  # => co-22: proves the tamper was detected, at EXACTLY the real tampered index


if (
    __name__ == "__main__"
):  # => co-22: only runs when launched directly, e.g. `python3 hash_chain_log.py`
    main()  # => co-22: builds the real chain, verifies it, tampers with one entry, then re-verifies and detects it
