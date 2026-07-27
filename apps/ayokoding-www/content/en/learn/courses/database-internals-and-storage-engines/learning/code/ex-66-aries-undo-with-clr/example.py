"""Example 66: ARIES Undo Writes Compensation Log Records (CLRs)."""
# Undo (co-18) writes a CLR for every rollback step -- so a re-crash during undo can safely resume.

from dataclasses import dataclass  # => a plain, typed record for one log entry


@dataclass  # => a plain, typed record -- fields carry their own defaults
class LogRecord:  # => either a normal update or a CLR marking an already-undone step
    lsn: int  # => this record's own log sequence number
    txn_id: int  # => which transaction this record belongs to
    page_id: int  # => which page it touched
    before: str  # => the value to restore if this update is ever undone
    is_clr: bool = (
        False  # => True once this specific undo step has been logged as compensated
    )
    compensates_lsn: int | None = (
        None  # => for a CLR: which ORIGINAL record's LSN this undoes
    )


def undo_with_clr(
    log: list[LogRecord], loser_txn: int
) -> list[LogRecord]:  # => co-18: undo, logging CLRs
    already_compensated = {
        r.compensates_lsn for r in log if r.is_clr
    }  # => LSNs a PRIOR undo pass already fixed
    clrs: list[LogRecord] = []  # => the compensation records this undo pass produces
    next_lsn = (
        max(r.lsn for r in log) + 1
    )  # => CLRs get fresh, monotonically increasing LSNs of their own
    for record in reversed(log):  # => undo walks BACKWARD, most recent change first
        needs_undo = (  # => true only for a genuinely un-compensated step of THIS loser
            record.txn_id == loser_txn
            and not record.is_clr
            and record.lsn not in already_compensated  # => all three checks
        )  # => end of the needs_undo condition
        if needs_undo:  # => a genuinely un-compensated step for this loser
            clr = LogRecord(  # => a CLR records that THIS specific undo step has now happened
                lsn=next_lsn,
                txn_id=loser_txn,
                page_id=record.page_id,
                before=record.before,  # => the restore value
                is_clr=True,
                compensates_lsn=record.lsn,  # => marks which original step this compensates
            )  # => end of the CLR construction
            clrs.append(
                clr
            )  # => if a crash happens again mid-undo, this CLR prevents re-undoing this step
            next_lsn += 1  # => the next CLR (if any) gets the following LSN
    return clrs  # => every compensation record this undo pass produced


log: list[
    LogRecord
] = [  # => one loser transaction with two updates, no CLRs written yet
    LogRecord(
        lsn=1, txn_id=9, page_id=100, before="orig-a"
    ),  # => loser txn 9's first update
    LogRecord(
        lsn=2, txn_id=9, page_id=101, before="orig-b"
    ),  # => loser txn 9's second update
]  # => end of the log fixture -- no CLRs exist yet
first_pass_clrs = undo_with_clr(
    log, loser_txn=9
)  # => the FIRST (uninterrupted) undo pass
print(len(first_pass_clrs))  # => Output: 2

log_after_first_pass = (
    log + first_pass_clrs
)  # => what the log looks like once those CLRs are written
resumed_clrs = undo_with_clr(
    log_after_first_pass, loser_txn=9
)  # => a "re-crash" -- undo runs AGAIN
print(len(resumed_clrs))  # => Output: 0

assert (
    len(first_pass_clrs) == 2
)  # => one CLR per undone update step, the first time through
assert (
    len(resumed_clrs) == 0
)  # => the re-run correctly does NOT redo already-compensated steps
print("ex-66 OK")  # => Output: ex-66 OK
