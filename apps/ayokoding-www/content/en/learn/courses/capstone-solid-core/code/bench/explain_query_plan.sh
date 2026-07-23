#!/usr/bin/env bash
# capstone-solid-core: Step 3's EXPLAIN-guided-index demonstration (topic 26 Advanced SQL &
# Query Performance). This app's database is SQLite, not PostgreSQL -- topic 26's own teaching
# engine is PostgreSQL specifically for `EXPLAIN ANALYZE`'s execution-time statistics
# (sqlite.org/lang_explain.html: SQLite's grammar has EXPLAIN and EXPLAIN QUERY PLAN, no
# ANALYZE keyword -- confirmed by reading that page directly). The TECHNIQUE topic 26 teaches
# -- read what the planner will do, add an index that removes an expensive step, confirm with
# the planner AND a real timing measurement -- is identical here, applied to the engine this
# specific app actually runs (sqlite.org/eqp.html documents EXPLAIN QUERY PLAN's own output).
# The timed before/after comparison lives in bench/benchmark_sql_tuning.py (perf_counter has
# far more resolution than this CLI's own `.timer` for a query this fast); this script only
# shows the real, captured QUERY PLAN shape changing.
set -euo pipefail

DB="/tmp/capstone-solid-core-eqp-bench.db"
rm -f "$DB"

echo "==> seeding: 1 user, 3 habits, 200,001 total check-ins (normalized schema, no denormalized column yet)"
sqlite3 "$DB" <<'SQL'
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (datetime('now')));
CREATE TABLE habits (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, name TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT (datetime('now')), archived INTEGER NOT NULL DEFAULT 0);
CREATE TABLE checkins (id INTEGER PRIMARY KEY AUTOINCREMENT, habit_id INTEGER NOT NULL REFERENCES habits(id) ON DELETE CASCADE, checkin_date TEXT NOT NULL, UNIQUE(habit_id, checkin_date));
CREATE INDEX idx_habits_user_id ON habits(user_id);
CREATE INDEX idx_checkins_habit_id ON checkins(habit_id);
INSERT INTO users (username, password_hash) VALUES ('bench_user', 'unused');
INSERT INTO habits (user_id, name) VALUES (1, 'Habit A'), (1, 'Habit B'), (1, 'Habit C');

WITH RECURSIVE seq(n) AS (SELECT 0 UNION ALL SELECT n + 1 FROM seq WHERE n < 66666)
INSERT INTO checkins (habit_id, checkin_date) SELECT 1, date('1990-01-01', n || ' days') FROM seq;
WITH RECURSIVE seq(n) AS (SELECT 0 UNION ALL SELECT n + 1 FROM seq WHERE n < 66666)
INSERT INTO checkins (habit_id, checkin_date) SELECT 2, date('2050-01-01', n || ' days') FROM seq;
WITH RECURSIVE seq(n) AS (SELECT 0 UNION ALL SELECT n + 1 FROM seq WHERE n < 66666)
INSERT INTO checkins (habit_id, checkin_date) SELECT 3, date('2110-01-01', n || ' days') FROM seq;
SQL
echo "==> seeded: $(sqlite3 "$DB" 'SELECT COUNT(*) FROM checkins') rows in checkins"

echo
echo "=== BEFORE: EXPLAIN QUERY PLAN for the recent-activity query (JOIN, no denormalized user_id) ==="
sqlite3 "$DB" "EXPLAIN QUERY PLAN SELECT h.id, c.checkin_date FROM checkins c JOIN habits h ON h.id = c.habit_id WHERE h.user_id = 1 ORDER BY c.checkin_date DESC LIMIT 20;"

echo
echo "==> applying migration_v3.sql (denormalize checkins.user_id + composite index)"
sqlite3 "$DB" <"$(dirname "${BASH_SOURCE[0]}")/../app/migration_v3.sql"

echo
echo "=== AFTER: EXPLAIN QUERY PLAN for the recent-activity query (single index, no join, no sort) ==="
sqlite3 "$DB" "EXPLAIN QUERY PLAN SELECT habit_id, checkin_date FROM checkins WHERE user_id = 1 ORDER BY checkin_date DESC LIMIT 20;"

echo
echo "=== correctness: BEFORE and AFTER return the identical 20 rows ==="
diff \
	<(sqlite3 "$DB" "SELECT h.id, c.checkin_date FROM checkins c JOIN habits h ON h.id = c.habit_id WHERE h.user_id = 1 ORDER BY c.checkin_date DESC LIMIT 20;") \
	<(sqlite3 "$DB" "SELECT habit_id, checkin_date FROM checkins WHERE user_id = 1 ORDER BY checkin_date DESC LIMIT 20;") &&
	echo "IDENTICAL -- the index changed the PLAN, not the RESULT"
