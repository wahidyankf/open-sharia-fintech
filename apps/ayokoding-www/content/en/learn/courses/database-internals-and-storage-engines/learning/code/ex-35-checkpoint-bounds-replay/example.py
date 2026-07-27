"""Example 35: A Checkpoint Bounds Redo Replay."""
# A checkpoint (co-20) is the only thing that bounds how far back redo must scan.

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- no custom __init__ needed
class LogRecord:  # => either a normal write or a checkpoint marker
    lsn: int  # => this record's own log sequence number
    kind: str  # => "write" or "checkpoint"


log: list[LogRecord] = [  # => two old records, a checkpoint, then two fresh records
    LogRecord(
        lsn=1, kind="write"
    ),  # => old history -- already durable before the checkpoint
    LogRecord(
        lsn=2, kind="write"
    ),  # => old history -- already durable before the checkpoint
    LogRecord(lsn=3, kind="checkpoint"),  # => the most recent checkpoint marker
    LogRecord(lsn=4, kind="write"),  # => needs redo -- happened AFTER the checkpoint
    LogRecord(lsn=5, kind="write"),  # => needs redo -- happened AFTER the checkpoint
]  # => end of the log fixture


def last_checkpoint_lsn(
    log: list[LogRecord],
) -> int:  # => finds the MOST RECENT checkpoint's LSN
    checkpoints = [
        r.lsn for r in log if r.kind == "checkpoint"
    ]  # => every checkpoint marker's LSN
    return (
        checkpoints[-1] if checkpoints else 0
    )  # => 0 means "no checkpoint yet -- scan from the start"


def redo_scan_range(
    log: list[LogRecord],
) -> list[int]:  # => the LSNs redo actually has to look at
    start = last_checkpoint_lsn(
        log
    )  # => everything up to and including this LSN is already durable
    return [
        r.lsn for r in log if r.lsn > start
    ]  # => only records strictly AFTER the checkpoint


scanned = redo_scan_range(log)  # => the bounded set of LSNs redo must actually replay
print(scanned)  # => Output: [4, 5]

assert scanned == [
    4,
    5,
]  # => redo skips records 1, 2, and the checkpoint itself -- only 4 and 5 remain
print("ex-35 OK")  # => Output: ex-35 OK
