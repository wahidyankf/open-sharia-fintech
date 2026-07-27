"""Example 29: Append-Only Log Replay."""

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass
class LogRecord:  # => the smallest unit a WAL ever stores -- just enough to replay one change
    seq: int  # => this record's position in append order
    action: str  # => a human-readable description of what happened


# A write-ahead log is APPEND-ONLY (co-16) -- records are never edited or
# reordered once written, so replaying them in the SAME order they were
# appended in is always well-defined, with no ambiguity about what happened
# first.
log: list[LogRecord] = []  # => models a WAL file as an in-memory list, in append order


def append(action: str) -> LogRecord:  # => the only way a record enters the log
    record = LogRecord(
        seq=len(log), action=action
    )  # => seq is just "how many records came before"
    log.append(
        record
    )  # => append-only: always added at the END, never inserted elsewhere
    return record


def replay() -> list[str]:  # => walks the log front-to-back, in append order
    return [
        record.action for record in log
    ]  # => list order == log order, by construction


append("insert row-1")  # => record 0
append("insert row-2")  # => record 1
append("delete row-1")  # => record 2
actions = replay()
print(actions)  # => Output: ['insert row-1', 'insert row-2', 'delete row-1']

assert actions == [
    "insert row-1",
    "insert row-2",
    "delete row-1",
]  # => replay order == append order
assert [r.seq for r in log] == [
    0,
    1,
    2,
]  # => sequence numbers are strictly increasing, gap-free
print("ex-29 OK")  # => Output: ex-29 OK
