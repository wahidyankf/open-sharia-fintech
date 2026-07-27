"""Worked Example 52: The Log as Source of Truth -- Replay Reconstructs State."""  # => co-12: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from dataclasses import dataclass  # => co-12: reuses ex-49's change-log entry shape -- the log itself is the source of truth


@dataclass  # => co-12: the SAME entry shape ex-49 built -- Jay Kreps' "The Log" idea, applied to table reconstruction
class ChangeLogEntry:  # => co-12: one append-only log entry -- insert, update, or delete
    operation: str  # => co-12: "insert", "update", or "delete"
    row_id: int  # => co-12: which row this change applies to
    value: str | None  # => co-12: the row's new value -- None for a delete


CHANGE_LOG = [  # => co-12: the append-only log this table's ENTIRE current state is reconstructed FROM, and only from
    ChangeLogEntry("insert", 1, "widget"),  # => co-12: row 1 created
    ChangeLogEntry("insert", 2, "gadget"),  # => co-12: row 2 created
    ChangeLogEntry("update", 2, "gadget-v2"),  # => co-12: row 2 updated in place
    ChangeLogEntry("insert", 3, "gizmo"),  # => co-12: row 3 created
    ChangeLogEntry("delete", 1, None),  # => co-12: row 1 deleted
]  # => co-12: closes CHANGE_LOG -- five entries, the ONLY source this worked example reads from


def replay(log: list[ChangeLogEntry]) -> dict[int, str]:  # => co-12: rebuilds current table state PURELY by folding over the log
    """Fold the change log into current table state -- a pure function of the log, called idempotent by co-05."""  # => co-12: documents replay's contract -- no runtime output, just sets its __doc__
    state: dict[int, str] = {}  # => co-12: the reconstructed table -- starts empty, EVERY time replay runs
    for entry in log:  # => co-12: fold one log entry at a time, in order
        if entry.operation in ("insert", "update"):  # => co-12: both operations converge to the SAME action -- set the current value
            state[entry.row_id] = entry.value  # type: ignore[assignment]  # => co-12: value is never None on insert/update, only on delete
        elif entry.operation == "delete":  # => co-12: a delete removes the row from current state entirely
            state.pop(entry.row_id, None)  # => co-12: safe to call even if somehow already absent
    return state  # => co-12: returns this computed value to the caller


if __name__ == "__main__":  # => co-12: entry point -- runs only when this file executes directly, not on import
    state_after_first_replay = replay(CHANGE_LOG)  # => co-12: REPLAY 1 -- fold the whole log once
    print(f"State after replay 1: {state_after_first_replay}")  # => co-12: prints the reconstructed table

    state_after_second_replay = replay(CHANGE_LOG)  # => co-05: REPLAY 2 -- the SAME log, folded again from an empty state
    print(f"State after replay 2 (same log, replayed again): {state_after_second_replay}")  # => co-05: prints the second reconstruction

    replays_agree = state_after_first_replay == state_after_second_replay  # => co-05: idempotent -- replaying the SAME log twice must agree
    print(f"Two independent replays of the identical log agree: {replays_agree}")  # => co-05: prints the reproducibility check
    assert replays_agree, "replaying the same log twice must reconstruct IDENTICAL current state, every time"  # => co-05: the claim
    assert state_after_first_replay == {2: "gadget-v2", 3: "gizmo"}, "row 1 deleted, row 2 updated, row 3 inserted -- the exact expected state"  # => co-12
    print(f"MATCH: {state_after_first_replay} -- the log alone, replayed idempotently, is sufficient to reconstruct current state")  # => co-12
    # => co-12: this is Jay Kreps' "The Log" idea end to end -- the log IS the source of truth; any derived table is just one replay of it
