"""Worked Example 27: Exactly-Once via the Idempotent Producer."""  # => co-13: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic


class IdempotentBroker:  # => co-13: models a broker's producer-id + sequence-number dedup, the mechanism behind KIP-98
    """Deduplicates appends by (producer_id, sequence) -- a retried send lands exactly once."""  # => co-13: documents IdempotentBroker's contract -- no runtime output, just sets its __doc__

    def __init__(self) -> None:  # => co-13: sets up this broker's dedup bookkeeping and append log
        self.seen_sequences: set[tuple[str, int]] = set()  # => co-13: every (producer_id, sequence) pair ALREADY accepted
        self.log: list[str] = []  # => co-13: the append-only log -- grows only on a genuinely NEW (producer_id, sequence)

    def append(self, producer_id: str, sequence: int, value: str) -> bool:  # => co-13: returns True iff this append was NEW
        """Append value iff (producer_id, sequence) has never been seen before; a retry is silently deduplicated."""  # => co-13: documents append's contract -- no runtime output, just sets its __doc__
        dedup_key = (producer_id, sequence)  # => co-13: the exact key KIP-98's idempotent producer dedups on
        if dedup_key in self.seen_sequences:  # => co-13: a RETRY of an already-accepted send -- dedup silently, no second append
            return False  # => co-13: signals "this was a duplicate, not a new record"
        self.seen_sequences.add(dedup_key)  # => co-13: mark this (producer_id, sequence) as now seen
        self.log.append(value)  # => co-13: append happens EXACTLY ONCE per unique (producer_id, sequence)
        return True  # => co-13: signals "this was genuinely new"


if __name__ == "__main__":  # => co-13: entry point -- runs only when this file executes directly, not on import
    broker = IdempotentBroker()  # => co-13: a fresh broker, nothing appended yet
    first_send = broker.append(producer_id="producer-1", sequence=42, value="order-created")  # => co-13: the ORIGINAL send
    print(f"First send accepted as new: {first_send} | Log: {broker.log}")  # => co-13: prints the first result

    retried_send = broker.append(producer_id="producer-1", sequence=42, value="order-created")  # => co-13: a NETWORK RETRY of the SAME send
    print(f"Retried send accepted as new: {retried_send} | Log: {broker.log}")  # => co-13: prints the retry's result -- log unchanged

    assert first_send is True and retried_send is False, "the retry must be recognized as a duplicate, not appended again"  # => co-13
    assert broker.log == ["order-created"], "the log must contain exactly one entry despite two send attempts"  # => co-13: the claim
    print(f"MATCH: {broker.log} -- the retried send landed exactly once, deduplicated by (producer_id, sequence)")  # => co-13
    # => co-13: idempotent producer dedup + transactions is what upgrades at-least-once's duplicates into exactly-once delivery
