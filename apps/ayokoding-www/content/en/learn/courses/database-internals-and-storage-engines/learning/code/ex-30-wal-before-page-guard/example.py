"""Example 30: WAL-Before-Page Ordering Guard."""

# The WAL rule: a log record must be DURABLE before the page it describes is
# flushed (co-16) -- reversing that order is exactly what makes a crash
# unrecoverable, since the page's change would exist with no log record to
# redo it from.


class WalOrderingError(Exception):  # => raised when a flush is attempted out of order
    """Raised when a page flush is attempted before its log record is durable."""  # => documents intent


durable_lsns: set[int] = set()  # => LSNs that have actually reached stable storage


def make_durable(
    lsn: int,
) -> None:  # => simulates fsync-ing the log up through this LSN
    durable_lsns.add(lsn)


def flush_page(page_lsn: int) -> None:  # => the guarded page-write path
    if page_lsn not in durable_lsns:  # => the guard: check BEFORE writing the page
        raise WalOrderingError(
            f"log record {page_lsn} is not yet durable -- refusing to flush the page"
        )
    print(
        f"page flushed (log record {page_lsn} was already durable)"
    )  # => Output: page flushed line


raised = False  # => flips to True only if the guard actually fires below
try:
    flush_page(page_lsn=5)  # => LSN 5's log record was never made durable
except WalOrderingError:  # => the exact exception the guard raises
    raised = True  # => confirms the guard fired instead of flushing out of order
assert raised  # => the page write was refused

make_durable(5)  # => NOW the log record is durable
flush_page(
    page_lsn=5
)  # => this time the guard passes -- Output: page flushed (log record 5 was already durable)

assert (
    5 in durable_lsns
)  # => the log record really was made durable before this second flush
print("ex-30 OK")  # => Output: ex-30 OK
