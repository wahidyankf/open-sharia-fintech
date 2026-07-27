"""Worked Example 45: DAG Backfill an Explicit Date Range."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from datetime import date  # => co-18: a backfill targets an explicit, bounded range of past partitions

ALL_PARTITIONS = [date(2026, 7, d) for d in range(1, 11)]  # => co-18: ten daily partitions already exist, 2026-07-01 through 2026-07-10
BACKFILL_START = date(2026, 7, 3)  # => co-18: the explicit past range this run targets -- STARTS here
BACKFILL_END = date(2026, 7, 5)  # => co-18: ...and ENDS here, inclusive -- exactly co-06's "reprocess an explicit past range" idea


def partitions_to_reprocess(all_partitions: list[date], *, start: date, end: date) -> list[date]:  # => co-18: the backfill's own selection logic
    """Return exactly the partitions within [start, end], inclusive -- and no others."""  # => co-18: documents partitions_to_reprocess's contract -- no runtime output, just sets its __doc__
    return [p for p in all_partitions if start <= p <= end]  # => co-18: an explicit, bounded range -- co-06's backfill idea, applied via the DAG


if __name__ == "__main__":  # => co-18: entry point -- runs only when this file executes directly, not on import
    targeted = partitions_to_reprocess(ALL_PARTITIONS, start=BACKFILL_START, end=BACKFILL_END)  # => co-18: compute the exact backfill scope
    untouched = [p for p in ALL_PARTITIONS if p not in targeted]  # => co-18: every partition OUTSIDE the backfill's declared range
    print(f"Backfill range: {BACKFILL_START} to {BACKFILL_END}")  # => co-18: frames the declared range
    print(f"Partitions reprocessed: {[p.isoformat() for p in targeted]}")  # => co-18: isoformat -- readable dates, not repr
    print(f"Partitions left untouched: {[p.isoformat() for p in untouched]}")  # => co-18: isoformat -- readable dates, not repr

    only_targeted_range = len(targeted) == 3 and all(BACKFILL_START <= p <= BACKFILL_END for p in targeted)  # => co-18: exactly the declared range
    untouched_count_correct = len(untouched) == len(ALL_PARTITIONS) - len(targeted)  # => co-18: everything else stays untouched
    print(f"Only the declared range reprocessed: {only_targeted_range} | Untouched count correct: {untouched_count_correct}")  # => co-18
    assert only_targeted_range, "a backfill must reprocess EXACTLY the explicit date range requested, no more"  # => co-18: the claim
    assert untouched_count_correct, "partitions outside the backfill range must remain entirely untouched"  # => co-18
    print(f"MATCH: {len(targeted)} of {len(ALL_PARTITIONS)} partitions reprocessed -- exactly the declared backfill range")  # => co-18
    # => co-18: because the underlying transform is idempotent (co-05), reprocessing this range is safe, not destructive
