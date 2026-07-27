"""Worked Example 43: DAG Schedule and Catchup."""  # => co-18: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from datetime import date, timedelta  # => co-18: a daily schedule, checked over a range of calendar dates

DAG_START_DATE = date(2026, 7, 1)  # => co-18: the DAG's own declared start -- Airflow 3 renamed schedule_interval to `schedule`
CURRENT_DATE = date(2026, 7, 5)  # => co-18: "now" -- the DAG was only just enabled today, four days after it was meant to start


def missed_intervals(start_date: date, current_date: date) -> list[date]:  # => co-18: catchup -- every daily interval between start and now
    """Return one date per missed daily interval, from start_date up to (but excluding) current_date."""  # => co-18: documents missed_intervals's contract -- no runtime output, just sets its __doc__
    intervals: list[date] = []  # => co-18: accumulates one entry per missed daily run
    day = start_date  # => co-18: begin at the DAG's own declared start date
    while day < current_date:  # => co-18: every day strictly before "now" was, by definition, MISSED
        intervals.append(day)  # => co-18: this day's run is owed, per Airflow's catchup semantics
        day += timedelta(days=1)  # => co-18: advance to the next daily interval
    return intervals  # => co-18: returns this computed value to the caller


if __name__ == "__main__":  # => co-18: entry point -- runs only when this file executes directly, not on import
    catchup_runs = missed_intervals(DAG_START_DATE, CURRENT_DATE)  # => co-18: compute every run catchup owes this DAG
    print(f"DAG start: {DAG_START_DATE} | Current date: {CURRENT_DATE}")  # => co-18: frames the schedule window
    print(f"Missed daily intervals needing a catchup run: {[d.isoformat() for d in catchup_runs]}")  # => co-18: isoformat -- readable dates, not repr

    one_run_per_missed_interval = len(catchup_runs) == (CURRENT_DATE - DAG_START_DATE).days  # => co-18: the claim -- ONE run per missed day, no more, no fewer
    print(f"Exactly one run created per missed interval: {one_run_per_missed_interval}")  # => co-18: prints the count check
    assert one_run_per_missed_interval, "catchup must create exactly one run per missed interval, no double-runs or skips"  # => co-18
    assert catchup_runs == [date(2026, 7, 1), date(2026, 7, 2), date(2026, 7, 3), date(2026, 7, 4)], "the exact four missed dates"  # => co-18
    print(f"MATCH: {len(catchup_runs)} missed daily intervals, {len(catchup_runs)} catchup runs created -- a 1:1 correspondence")  # => co-18
    # => co-18: catchup=True (Airflow 3's own default is now False) is what makes a late-enabled DAG backfill its own history automatically
