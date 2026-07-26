"""Example 32: Skip Already-Applied Records via pageLSN."""

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- no custom __init__ needed
class LogRecord:  # => a WAL record that changed exactly one page
    lsn: int  # => this record's own log sequence number
    page_id: int  # => which page it changed
    new_value: str  # => the value it wrote


def redo(
    log: list[LogRecord], page_lsns: dict[int, int]
) -> dict[int, str]:  # => returns applied values
    applied: dict[
        int, str
    ] = {}  # => page_id -> value, only for records actually re-applied
    for (
        record
    ) in log:  # => walk the log in LSN order -- ARIES calls this "repeating history"
        current_page_lsn = page_lsns.get(
            record.page_id, 0
        )  # => 0 means "page never touched before crash"
        if (
            record.lsn > current_page_lsn
        ):  # => the redo rule: only re-apply what is NEWER than the page
            applied[record.page_id] = record.new_value  # => genuinely re-applied
            page_lsns[record.page_id] = (
                record.lsn
            )  # => the page's pageLSN now reflects this record too
        # => record.lsn <= current_page_lsn means this change was ALREADY on the page before the crash
    return (
        applied  # => the caller can see exactly which pages were genuinely re-applied
    )


log = [  # => three records against the same page, only one of which still needs redo
    LogRecord(
        lsn=1, page_id=10, new_value="v1"
    ),  # => already reflected on page 10 before the crash
    LogRecord(
        lsn=2, page_id=10, new_value="v2"
    ),  # => also already reflected (page_lsns[10] starts at 2)
    LogRecord(
        lsn=3, page_id=10, new_value="v3"
    ),  # => NOT yet reflected -- this one needs redo
]  # => end of the log fixture
page_lsns = {
    10: 2
}  # => page 10's pageLSN says "everything up to LSN 2 is already applied"
applied = redo(log, page_lsns)  # => run redo over the whole log
print(applied)  # => Output: {10: 'v3'}

assert applied == {
    10: "v3"
}  # => only the record whose LSN exceeded the page's pageLSN was re-applied
assert (
    page_lsns[10] == 3
)  # => the page's pageLSN now reflects the redo that actually happened
print("ex-32 OK")  # => Output: ex-32 OK
