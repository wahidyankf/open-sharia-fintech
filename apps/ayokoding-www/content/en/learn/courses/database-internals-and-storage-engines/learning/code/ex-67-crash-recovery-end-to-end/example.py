"""Example 67: Crash Recovery End-to-End -- Analysis, Redo, Undo."""
# The full three-phase pass (co-19): analysis finds losers, redo repeats history, undo removes losers.

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- fields carry their own defaults
class LogRecord:  # => a simplified log record with everything undo needs
    lsn: int  # => this record's own log sequence number
    txn_id: int  # => which transaction issued it
    kind: str  # => "begin", "update", or "commit"
    key: str | None = None  # => the key an "update" touched, if any
    before: str | None = None  # => the value to restore if this update must be undone
    after: str | None = None  # => the value this update set, which redo would apply


log: list[LogRecord] = [  # => one committer, one loser, sharing the same small log
    LogRecord(lsn=1, txn_id=1, kind="begin"),  # => txn 1: will commit
    LogRecord(
        lsn=2, txn_id=1, kind="update", key="a", before="orig-a", after="committed-a"
    ),  # => txn 1 writes key a
    LogRecord(lsn=3, txn_id=1, kind="commit"),  # => txn 1 is a WINNER
    LogRecord(lsn=4, txn_id=2, kind="begin"),  # => txn 2: never commits
    LogRecord(
        lsn=5, txn_id=2, kind="update", key="b", before="orig-b", after="uncommitted-b"
    ),  # => txn 2 writes key b
]  # => txn 2 has no commit record -- it is a LOSER, caught mid-flight by the crash


def recover(
    log: list[LogRecord],
) -> dict[str, str]:  # => co-19: the full analysis + redo + undo pass
    committed = {
        r.txn_id for r in log if r.kind == "commit"
    }  # => analysis: who actually committed
    state: dict[str, str] = {}  # => the reconstructed page state, starting from nothing
    for (
        record
    ) in log:  # => redo: replay EVERY update, committed or not (repeats history)
        if (
            record.kind == "update"
            and record.key is not None
            and record.after is not None
        ):  # => a real write
            state[record.key] = (
                record.after
            )  # => applied unconditionally, exactly as ex-65 does
    for record in reversed(
        log
    ):  # => undo: roll back only the LOSERS, most recent change first
        is_loser_update = (
            record.kind == "update" and record.txn_id not in committed
        )  # => a loser's write
        if (
            is_loser_update and record.key is not None and record.before is not None
        ):  # => safe to restore
            state[record.key] = (
                record.before
            )  # => restore the pre-write value for this loser's change
    return state  # => committed data survives; uncommitted data is gone


final_state = recover(log)  # => run the full three-phase recovery pass
print(final_state)  # => Output: {'a': 'committed-a', 'b': 'orig-b'}

assert (
    final_state["a"] == "committed-a"
)  # => txn 1's committed write survived the crash
assert (
    final_state["b"] == "orig-b"
)  # => txn 2's uncommitted write was undone -- gone, as required
print("ex-67 OK")  # => Output: ex-67 OK
