-- capstone-solid-core: Step 3's EXPLAIN-guided index (topic 26 Advanced SQL & Query
-- Performance, topic 10 co-22 schema-migration). Applied once at PRAGMA user_version 2 -> 3
-- by app/repository_sqlite.py's init_db().
--
-- WHY: GET /habits/activity/recent (Step 3's new "recent activity across ALL my habits"
-- endpoint) needs each user's most recent check-ins, newest first, without caring which
-- specific habit each one belongs to. Reached through the ORIGINAL normalized schema, that
-- query has to JOIN checkins to habits just to filter by user_id, then SORT the joined rows by
-- checkin_date -- confirmed for real via EXPLAIN QUERY PLAN (see bench/explain_query_plan.sh):
-- `SEARCH h USING COVERING INDEX idx_habits_user_id (user_id=?)` then
-- `SEARCH c USING COVERING INDEX sqlite_autoindex_checkins_1 (habit_id=?)` (NOT a full table
-- scan -- both sides of the join already use an index) followed by `USE TEMP B-TREE FOR ORDER BY`.
--
-- FIX: a deliberate, DOCUMENTED denormalization (topic 26 co-XX denormalization-tradeoffs) --
-- copy `user_id` onto `checkins` (it never changes after a habit is created, so there is no
-- update-anomaly risk this specific denormalization introduces) and index (user_id,
-- checkin_date DESC). The query becomes a single ordered index walk with NO join and NO sort:
-- `SEARCH checkins USING INDEX idx_checkins_user_id_date (user_id=?)`.
--
-- Backfill uses SQLite's `UPDATE ... FROM` (correlated update), supported since SQLite 3.33.0
-- (2020-08-14, https://sqlite.org/releaselog/3_33_0.html) -- well below this app's pinned
-- runtime (Python 3.13's bundled SQLite is materially newer). The new column stays nullable at
-- the schema level (SQLite cannot add a NOT NULL column with no default to a non-empty table
-- in one step); repository_sqlite.py always supplies it going forward, so it is never actually
-- null in practice.
ALTER TABLE checkins
ADD COLUMN user_id INTEGER REFERENCES users (id) ON DELETE CASCADE;

UPDATE checkins
SET user_id = habits.user_id
FROM habits
WHERE habits.id = checkins.habit_id;

CREATE INDEX IF NOT EXISTS idx_checkins_user_id_date ON checkins (user_id, checkin_date DESC);
