"""Example 34: WAL Undo Rolls Back Uncommitted Writes."""
# Undo removes exactly what redo just replayed for transactions that never committed (co-19).

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- no custom __init__ needed
class LogRecord:  # => carries BOTH the old and new value -- undo needs the old one
    txn_id: int  # => which transaction wrote this
    key: str  # => the key that was written
    before: (
        str  # => the value that existed BEFORE this write -- undo's restoration target
    )
    after: str  # => the value this write set -- what redo would apply


log: list[LogRecord] = [  # => one committed write, one that never committed
    LogRecord(
        txn_id=1, key="a", before="orig-a", after="committed-a"
    ),  # => txn 1 commits
    LogRecord(
        txn_id=2, key="b", before="orig-b", after="uncommitted-b"
    ),  # => txn 2 never commits
]  # => end of the log fixture
committed_txns: set[int] = {1}  # => only txn 1 reached COMMIT before the crash

state: dict[str, str] = {
    record.key: record.after for record in log
}  # => redo already ran (ex-33's step)
print(state)  # => Output: {'a': 'committed-a', 'b': 'uncommitted-b'}


def undo_losers(
    log: list[LogRecord], state: dict[str, str], committed: set[int]
) -> None:  # => rolls back losers
    for record in reversed(
        log
    ):  # => undo walks the log BACKWARD -- most recent uncommitted change first
        if (
            record.txn_id not in committed
        ):  # => a "loser" transaction: never reached COMMIT
            state[record.key] = (
                record.before
            )  # => restore the value that existed before this write


undo_losers(log, state, committed_txns)  # => run the repair pass over the redone state
print(state)  # => Output: {'a': 'committed-a', 'b': 'orig-b'}

assert state["a"] == "committed-a"  # => the committed write was untouched by undo
assert (
    state["b"] == "orig-b"
)  # => the uncommitted write was rolled back to its before-image
print("ex-34 OK")  # => Output: ex-34 OK
