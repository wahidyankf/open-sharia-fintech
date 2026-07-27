"""Worked Example 26: At-Least-Once Redelivery."""  # => co-13: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass, field  # => co-13: models a consumer's committed-offset bookkeeping


@dataclass  # => co-13: a minimal consumer -- processes records, but only ADVANCES its committed offset on success
class Consumer:  # => co-13: models the at-least-once default: process, THEN commit -- a crash in between causes redelivery
    committed_offset: int = -1  # => co-13: -1 means "nothing committed yet" -- the consumer resumes from committed_offset + 1
    processed_log: list[int] = field(default_factory=list)  # => co-13: EVERY offset actually processed, including duplicates

    def process(self, offset: int, *, crash_before_commit: bool) -> None:  # => co-13: process one record, optionally simulating a crash
        """Process one record; only commit its offset if crash_before_commit is False."""  # => co-13: documents process's contract -- no runtime output, just sets its __doc__
        self.processed_log.append(offset)  # => co-13: processing happens FIRST, regardless of whether the commit will succeed
        if not crash_before_commit:  # => co-13: the happy path -- commit succeeds, offset advances
            self.committed_offset = offset  # => co-13: only NOW does the consumer's resume point move forward


if __name__ == "__main__":  # => co-13: entry point -- runs only when this file executes directly, not on import
    consumer = Consumer()  # => co-13: a fresh consumer, nothing committed yet
    consumer.process(offset=0, crash_before_commit=False)  # => co-13: record 0 -- processed AND committed normally
    consumer.process(offset=1, crash_before_commit=True)  # => co-13: record 1 -- processed, but CRASHES before the commit lands
    print(f"After the crash: committed_offset={consumer.committed_offset}, processed_log={consumer.processed_log}")  # => co-13

    resume_from = consumer.committed_offset + 1  # => co-13: the consumer restarts, resuming from committed_offset + 1
    print(f"Consumer restarts, resuming from offset {resume_from}")  # => co-13: prints the resume point -- offset 1, NOT offset 2
    consumer.process(offset=resume_from, crash_before_commit=False)  # => co-13: record 1 is REDELIVERED and processed AGAIN
    print(f"After redelivery: committed_offset={consumer.committed_offset}, processed_log={consumer.processed_log}")  # => co-13

    offset_1_count = consumer.processed_log.count(1)  # => co-13: how many times was offset 1 actually processed?
    print(f"Offset 1 processed {offset_1_count} times (a duplicate)")  # => co-13: prints the duplicate count
    assert offset_1_count == 2, "a crash before commit must cause the SAME record to be redelivered and reprocessed"  # => co-13: the claim
    assert consumer.committed_offset == 1, "the consumer must successfully commit past the record on the retry"  # => co-13
    print("MATCH: at-least-once means a crash before commit produces a genuine duplicate, not a lost record")  # => co-13
    # => co-13: at-least-once trades "never lose a record" for "sometimes process one twice" -- co-21 covers making that safe
