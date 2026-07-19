"""capstone-solid-core: Step 3's SQL-tuning wall-clock benchmark (topic 26 Advanced SQL &
Query Performance), pairing bench/explain_query_plan.sh's real EXPLAIN QUERY PLAN output with
a PRECISE timing comparison -- the `sqlite3` CLI's own `.timer` rounds "real" time to 3 decimal
places, too coarse for a query this fast; `time.perf_counter()` (the standard library's
monotonic, highest-resolution timer) does not have that limitation.

Seeds the SAME shape of data as explain_query_plan.sh (1 user, 3 habits, 200,001 total
check-ins) directly through the Python `sqlite3` module, runs the recent-activity query 200
times BEFORE the index and 200 times AFTER, and reports the total elapsed time for each batch.
Every number below comes from an actual run against a real SQLite file; nothing here is
estimated or assumed.

Run: python3 -m bench.benchmark_sql_tuning   (from capstone-solid-core/code/, inside the venv)
"""

from __future__ import annotations

import os
import sqlite3
import time
from datetime import date, timedelta
from pathlib import Path

REPETITIONS = 200


def _seed(db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    conn.executescript(
        """
        CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (datetime('now')));
        CREATE TABLE habits (id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            name TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (datetime('now')),
            archived INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE checkins (id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE,
            checkin_date TEXT NOT NULL, UNIQUE(habit_id, checkin_date));
        CREATE INDEX idx_habits_user_id ON habits(user_id);
        CREATE INDEX idx_checkins_habit_id ON checkins(habit_id);
        INSERT INTO users (username, password_hash) VALUES ('bench_user', 'unused');
        INSERT INTO habits (user_id, name) VALUES (1, 'Habit A'), (1, 'Habit B'), (1, 'Habit C');
        """
    )
    base = date(1990, 1, 1)
    for habit_id, offset_start in ((1, 0), (2, 22_000), (3, 44_000)):
        rows = [
            (habit_id, (base + timedelta(days=offset_start + i)).isoformat())
            for i in range(66_667)
        ]
        conn.executemany(
            "INSERT INTO checkins (habit_id, checkin_date) VALUES (?, ?)", rows
        )
    conn.commit()
    conn.close()


def _time_query(
    conn: sqlite3.Connection, sql: str, params: tuple[object, ...]
) -> float:
    start = time.perf_counter()
    for _ in range(REPETITIONS):
        conn.execute(sql, params).fetchall()
    return time.perf_counter() - start


def main() -> None:
    db_path = "/tmp/capstone-solid-core-sql-tuning-bench.db"
    if os.path.exists(db_path):
        os.remove(db_path)
    print(f"Seeding {db_path} with 200,001 check-ins across 3 habits, 1 user...")
    _seed(db_path)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    before_sql = (
        "SELECT h.id, c.checkin_date FROM checkins c "
        "JOIN habits h ON h.id = c.habit_id "
        "WHERE h.user_id = ? ORDER BY c.checkin_date DESC LIMIT ?"
    )
    before_result = conn.execute(before_sql, (1, 20)).fetchall()
    before_elapsed = _time_query(conn, before_sql, (1, 20))

    migration_v3 = (
        Path(__file__).parent.parent / "app" / "migration_v3.sql"
    ).read_text(encoding="utf-8")
    conn.executescript(migration_v3)

    after_sql = (
        "SELECT habit_id, checkin_date FROM checkins "
        "WHERE user_id = ? ORDER BY checkin_date DESC LIMIT ?"
    )
    after_result = conn.execute(after_sql, (1, 20)).fetchall()
    after_elapsed = _time_query(conn, after_sql, (1, 20))

    before_rows = [(r["id"], r["checkin_date"]) for r in before_result]
    after_rows = [(r["habit_id"], r["checkin_date"]) for r in after_result]
    assert before_rows == after_rows, "MISMATCH -- the index must not change the RESULT"

    speedup = before_elapsed / after_elapsed if after_elapsed > 0 else float("inf")
    print(
        f"\n{REPETITIONS} repetitions of the recent-activity query, same 200,001-row DB:"
    )
    print(
        f"  BEFORE (join + temp b-tree sort): {before_elapsed:.4f}s total, "
        f"{before_elapsed / REPETITIONS * 1000:.4f}ms/query"
    )
    print(
        f"  AFTER  (single ordered index scan): {after_elapsed:.4f}s total, "
        f"{after_elapsed / REPETITIONS * 1000:.4f}ms/query"
    )
    print(f"  speedup: {speedup:.2f}x")
    print(
        "  results identical (asserted above before these numbers were printed): True"
    )

    conn.close()


if __name__ == "__main__":
    main()
