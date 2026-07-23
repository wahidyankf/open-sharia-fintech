"""capstone-solid-core: Step 3's concurrency benchmark (topic 24 Concurrency & Parallelism).
Seeds a real SQLite database with many habits, each with a long check-in history, then times
`sequential_digest` against `concurrent_digest` (app/digest.py) over the SAME database with
`time.perf_counter()`. Both are asserted to return the identical set of results BEFORE the
timing numbers are printed -- a benchmark that skipped the correctness check could silently
compare a slow-but-right implementation to a fast-but-wrong one.

Run (large, realistic scale -- the default): python3 -m bench.benchmark_concurrency
Run (small scale, to reproduce ADR-0003's small-workload finding):
    python3 -m bench.benchmark_concurrency --num-habits 16 --checkins-per-habit 8000
(from capstone-solid-core/code/, inside the venv)
"""

from __future__ import annotations

import argparse
import os
import random
import sys
import time
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.digest import concurrent_digest, sequential_digest
from app.models import HabitCreate
from app.repository_sqlite import SqliteHabitRepository, get_connection, init_db


def _seed_database(
    db_path: str, num_habits: int, checkins_per_habit: int, seed: int
) -> list[int]:
    """Creates one user with `num_habits` habits, each with `checkins_per_habit` scattered,
    non-consecutive check-ins -- large enough per-habit histories that
    `longest_streak_ever`'s O(n) scan is genuinely non-trivial work per habit.

    Uses `executemany` + ONE commit at the end -- not `SqliteHabitRepository.record_checkin`
    (which commits per call, correct for a live request but far too slow for seeding hundreds
    of thousands of synthetic rows). This is seed-data generation, not the code path under
    benchmark; correctness of the PRODUCTION per-request path is already covered by
    tests/test_app.py's integration tests."""
    rng = random.Random(seed)
    init_db(db_path)
    conn = get_connection(db_path)
    from app.repository_sqlite import create_user

    user = create_user(conn, "bench_user", "unused-hash-for-benchmark-only")
    repo = SqliteHabitRepository(conn)
    habit_ids: list[int] = []
    base = date(1990, 1, 1)
    for i in range(num_habits):
        habit = repo.create_habit(user.id, HabitCreate(name=f"Habit {i}"))
        habit_ids.append(habit.id)
        window = checkins_per_habit * 3
        offsets = rng.sample(range(window), checkins_per_habit)
        rows = [
            (habit.id, user.id, (base + timedelta(days=offset)).isoformat())
            for offset in offsets
        ]
        conn.executemany(
            "INSERT INTO checkins (habit_id, user_id, checkin_date) VALUES (?, ?, ?)",
            rows,
        )
    conn.commit()
    conn.close()
    return habit_ids


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--num-habits",
        type=int,
        default=40,
        help="Number of habits to seed (default: 40, the large-scale scenario).",
    )
    parser.add_argument(
        "--checkins-per-habit",
        type=int,
        default=25_000,
        help="Check-ins per habit to seed (default: 25000, the large-scale scenario).",
    )
    args = parser.parse_args()

    db_path = "/tmp/capstone-solid-core-concurrency-bench.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    num_habits = args.num_habits
    checkins_per_habit = args.checkins_per_habit
    print(
        f"Seeding {num_habits} habits x {checkins_per_habit} check-ins each "
        f"({num_habits * checkins_per_habit} total rows)..."
    )
    habit_ids = _seed_database(db_path, num_habits, checkins_per_habit, seed=7)
    today = date(1990, 1, 1) + timedelta(days=checkins_per_habit * 3)

    start = time.perf_counter()
    sequential_result = sequential_digest(
        db_path, user_id=1, habit_ids=habit_ids, today=today
    )
    sequential_elapsed = time.perf_counter() - start

    start = time.perf_counter()
    concurrent_result = concurrent_digest(
        db_path, user_id=1, habit_ids=habit_ids, today=today, max_workers=4
    )
    concurrent_elapsed = time.perf_counter() - start

    assert sorted(sequential_result, key=lambda d: d.habit_id) == sorted(
        concurrent_result, key=lambda d: d.habit_id
    ), "MISMATCH -- sequential and concurrent digests must return identical results"

    speedup = (
        sequential_elapsed / concurrent_elapsed
        if concurrent_elapsed > 0
        else float("inf")
    )
    print(f"sequential_digest:  {sequential_elapsed:.4f}s")
    print(f"concurrent_digest:  {concurrent_elapsed:.4f}s  (max_workers=4)")
    print(f"speedup:            {speedup:.2f}x")
    print("results match:      True (asserted above before these numbers were printed)")


if __name__ == "__main__":
    main()
