"""Example 65: ARIES Redo Repeats History Regardless of Commit Status."""
# ARIES "repeats history" (co-18) -- redo replays EVERY logged change, committed or not.

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- no custom __init__ needed
class LogRecord:  # => one logged page write
    lsn: int  # => this record's own log sequence number
    page_id: int  # => which page it changed
    value: str  # => the value it wrote


log: list[
    LogRecord
] = [  # => three writes across two pages, one from an uncommitted writer
    LogRecord(lsn=1, page_id=1, value="v1"),  # => from a transaction that later commits
    LogRecord(
        lsn=2, page_id=2, value="v1"
    ),  # => from a transaction that never commits (a "loser")
    LogRecord(
        lsn=3, page_id=1, value="v2"
    ),  # => a second write to page 1, also from a committer
]  # => end of the log fixture


def redo_repeat_history(
    log: list[LogRecord],
) -> dict[int, str]:  # => co-18: replay EVERYTHING, no filtering
    pages: dict[
        int, str
    ] = {}  # => reconstructed page state, starting from a blank slate ("crashed")
    for record in (
        log
    ):  # => walk the whole log in LSN order -- commit status is NEVER checked here
        pages[record.page_id] = (
            record.value
        )  # => apply the change exactly as it was originally applied
    return pages  # => the pre-crash state, fully reconstructed -- including the loser's changes


pages = redo_repeat_history(log)  # => run redo over the entire fixture log
print(pages)  # => Output: {1: 'v2', 2: 'v1'}

assert (
    pages[1] == "v2"
)  # => page 1 reaches its exact pre-crash state (the second write won)
assert (
    pages[2] == "v1"
)  # => page 2 ALSO reaches its pre-crash state, even though its writer never committed
print("ex-65 OK")  # => Output: ex-65 OK
