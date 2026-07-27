"""Worked Example 37: Data Quality -- Timeliness (Freshness Check)."""  # => co-16: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from datetime import datetime, timedelta, timezone  # => co-16: timeliness is checked against the CURRENT moment, not a fixed constant

FRESHNESS_THRESHOLD_HOURS = 24  # => co-16: a batch is "fresh" only if its newest row is within this many hours of now


def is_fresh(max_event_timestamp: datetime, *, now: datetime) -> bool:  # => co-16: the timeliness check itself -- a pure, testable function
    """Return True iff max_event_timestamp is within FRESHNESS_THRESHOLD_HOURS of `now`."""  # => co-16: documents is_fresh's contract -- no runtime output, just sets its __doc__
    age = now - max_event_timestamp  # => co-16: how STALE is the newest row in this batch?
    return age <= timedelta(hours=FRESHNESS_THRESHOLD_HOURS)  # => co-16: fresh iff the newest row is within the threshold


if __name__ == "__main__":  # => co-16: entry point -- runs only when this file executes directly, not on import
    fixed_now = datetime(2026, 7, 27, 12, 0, 0, tzinfo=timezone.utc)  # => co-16: a FIXED "now" -- keeps this worked example's output reproducible
    fresh_batch_max_ts = fixed_now - timedelta(hours=3)  # => co-16: this batch's newest row is only 3h old -- well within the 24h threshold
    stale_batch_max_ts = fixed_now - timedelta(hours=48)  # => co-16: this batch's newest row is 48h old -- TWICE the threshold

    fresh_result = is_fresh(fresh_batch_max_ts, now=fixed_now)  # => co-16: check the fresh batch
    stale_result = is_fresh(stale_batch_max_ts, now=fixed_now)  # => co-16: check the stale batch
    print(f"Fresh batch (max ts 3h old): timeliness check passed = {fresh_result}")  # => co-16: prints the fresh batch's verdict
    print(f"Stale batch (max ts 48h old): timeliness check passed = {stale_result}")  # => co-16: prints the stale batch's verdict

    assert fresh_result is True, "a batch whose newest row is within the freshness threshold must pass"  # => co-16: the claim
    assert stale_result is False, "a batch whose newest row exceeds the freshness threshold must fail"  # => co-16: the claim ex-37 makes
    print(f"MATCH: a {FRESHNESS_THRESHOLD_HOURS}h freshness threshold correctly separates the fresh batch from the stale one")  # => co-16
    # => co-16: timeliness is the one data-quality dimension that can only be checked relative to the CURRENT moment
