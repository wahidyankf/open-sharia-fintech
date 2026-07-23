"""capstone-solid-core: the digest hot path -- SEQUENTIAL and CONCURRENT strategies that
compute the IDENTICAL result (topic 24 Concurrency & Parallelism). For every one of a user's
habits, computes its current streak, its longest-streak-ever (Step 3's O(n) algorithm, topic
25), and its total check-in count -- for a user with many habits and long histories, this is
genuinely CPU-bound per habit (rebuilding the domain object's hash-set from every stored
check-in row, then an O(n) scan over it), so it is the hot path this capstone makes concurrent.

DELIBERATELY NOT wired behind a synchronous HTTP route: spawning a fresh `ProcessPoolExecutor`
on every incoming request would pay process-spawn overhead per request, the opposite of what
Step 3's own benchmark shows (see `bench/benchmark_concurrency.py` -- overhead dominates at
small scale). This module is called directly instead, the way a real system would run it -- a
periodic batch/reporting job (a nightly digest email, an admin report) -- which is exactly
where `ProcessPoolExecutor`'s per-call spawn cost is amortized across a large, one-shot batch
rather than paid on every request. `tests/test_app.py`'s `TestDigestSequentialAndConcurrentAgree`
proves both strategies agree; `bench/benchmark_concurrency.py` measures the real speedup.

Each worker opens its OWN `sqlite3.Connection` -- a connection cannot cross a process boundary
(it holds an OS file handle and internal C state that does not survive `pickle`), so `digest.py`
passes only the `db_path` (a plain string) to each worker and lets it reconnect. `PRAGMA
journal_mode=WAL` (set in `repository_sqlite.get_connection`) is what makes many concurrent
READER connections to the same SQLite file safe (sqlite.org/wal.html): "WAL provides more
concurrency as readers do not block writers and a writer does not block readers."
"""

from __future__ import annotations

import sqlite3
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import date

from .repository_sqlite import SqliteHabitRepository


@dataclass(frozen=True, slots=True)
class HabitDigest:
    habit_id: int
    name: str
    current_streak: int
    longest_streak_ever: int
    checkin_count: int


def _digest_for_habit(
    db_path: str, user_id: int, habit_id: int, today_iso: str
) -> HabitDigest:
    """Runs INSIDE a worker (this same function is called directly by the sequential path
    below, and via `ProcessPoolExecutor` by the concurrent path -- same function, same result,
    only the CALLER differs). Opens its own connection: state that must cross a process
    boundary has to be rebuilt on the other side, never shared by reference (DD-33
    taming-state, applied to concurrency instead of just to the DB-vs-domain-object split)."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        repo = SqliteHabitRepository(conn)
        habit = repo.get_habit(habit_id, user_id)
        assert habit is not None  # => the caller only ever passes ids it just listed
        today = date.fromisoformat(today_iso)
        return HabitDigest(
            habit_id=habit.id,
            name=habit.name,
            current_streak=habit.current_streak(today),
            longest_streak_ever=habit.longest_streak_ever(),  # => Step 3's O(n) algorithm
            checkin_count=habit.checkin_count(),
        )
    finally:
        conn.close()


def sequential_digest(
    db_path: str, user_id: int, habit_ids: list[int], today: date
) -> list[HabitDigest]:
    """BEFORE: one habit at a time, entirely inside the request-handling process."""
    today_iso = today.isoformat()
    return [_digest_for_habit(db_path, user_id, hid, today_iso) for hid in habit_ids]


def concurrent_digest(
    db_path: str,
    user_id: int,
    habit_ids: list[int],
    today: date,
    max_workers: int = 4,
) -> list[HabitDigest]:
    """AFTER: each habit's load + O(n) longest-streak scan runs in its OWN OS process
    (`concurrent.futures.ProcessPoolExecutor`, Python standard library since 3.2 --
    docs.python.org/3/library/concurrent.futures.html) -- genuine parallelism across CPU
    cores for this CPU-bound per-habit work. A THREAD pool would stay serialized on the
    CPU-bound parts of this same code path (building the hash-set, walking it) because of the
    GIL; a PROCESS pool does not share a GIL at all."""
    today_iso = today.isoformat()
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        results = list(
            pool.map(
                _digest_for_habit,
                [db_path] * len(habit_ids),
                [user_id] * len(habit_ids),
                habit_ids,
                [today_iso] * len(habit_ids),
            )
        )
    return results
