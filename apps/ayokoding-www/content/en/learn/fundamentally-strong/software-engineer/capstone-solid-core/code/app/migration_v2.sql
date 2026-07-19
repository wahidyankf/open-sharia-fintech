-- Pass-1 capstone: Habit Tracker -- additive migration (topic 10, co-22 schema-migration).
-- Applied once at PRAGMA user_version 1 -> 2 by app/repository.py's init_db(). An ADDITIVE
-- ALTER TABLE with a DEFAULT never breaks a row that already exists -- every pre-migration
-- habit reads back with archived = 0 (not archived) with no backfill step needed.
-- 0 = active, 1 = archived
ALTER TABLE habits
ADD COLUMN archived INTEGER NOT NULL DEFAULT 0;
