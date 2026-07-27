"""Example 33: WAL Redo Replays Committed Writes."""
# ARIES-style redo replays EVERY logged write (co-19) -- undo removes the losers next.

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- no custom __init__ needed
class LogRecord:  # => a WAL record for one key's write, tagged with its owning transaction
    txn_id: int  # => which transaction wrote this
    key: str  # => the key that was written
    value: str  # => the value it was set to


log: list[LogRecord] = [  # => one committed write, one that never committed
    LogRecord(txn_id=1, key="a", value="committed-a"),  # => txn 1 later commits
    LogRecord(
        txn_id=2, key="b", value="uncommitted-b"
    ),  # => txn 2 never commits (crashes mid-flight)
]  # => end of the log fixture
committed_txns: set[int] = {
    1
}  # => only txn 1 reached COMMIT before the simulated crash


def redo_all(
    log: list[LogRecord],
) -> dict[str, str]:  # => replays EVERY record, commit status ignored
    state: dict[
        str, str
    ] = {}  # => simulates the page state, wiped clean by the "crash"
    for record in (
        log
    ):  # => redo does not check committed_txns at all -- that is undo's job (ex-34)
        state[record.key] = (
            record.value
        )  # => re-apply, regardless of whether the writer ever committed
    return state  # => the fully redone state, including transactions that never actually committed


state = redo_all(
    log
)  # => in-memory state was discarded ("crash") -- this rebuilds it from the log
print(state)  # => Output: {'a': 'committed-a', 'b': 'uncommitted-b'}

assert (
    state["a"] == "committed-a"
)  # => the committed write survived the crash, via redo
assert 1 in committed_txns  # => confirms txn 1 really did commit before the crash
print("ex-33 OK")  # => Output: ex-33 OK
