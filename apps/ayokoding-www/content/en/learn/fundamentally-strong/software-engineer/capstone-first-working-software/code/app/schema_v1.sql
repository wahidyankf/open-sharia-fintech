-- Pass-1 capstone: Habit Tracker -- base schema (topic 10, applied once at PRAGMA user_version 0 -> 1).
-- Three normalized tables, one fact per place (co-05 normalization): a user owns habits, a habit
-- owns check-ins. No repeated columns, no computed/derived data stored (current_streak is always
-- computed by app/domain.py from these rows, never persisted).
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT, -- co-02 primary-keys: aliases SQLite's rowid, auto-assigned
  username TEXT NOT NULL UNIQUE, -- co-04 constraints: NOT NULL + UNIQUE enforced by the engine
  password_hash TEXT NOT NULL, -- co-09/co-10/co-11 (topic 17): an argon2id PHC string, never a raw password
  created_at TEXT NOT NULL DEFAULT (datetime ('now'))
);

CREATE TABLE IF NOT EXISTS habits (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE, -- co-03 foreign-keys: an orphan habit can't exist
  name TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime ('now'))
);

CREATE TABLE IF NOT EXISTS checkins (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  habit_id INTEGER NOT NULL REFERENCES habits (id) ON DELETE CASCADE,
  checkin_date TEXT NOT NULL, -- ISO 'YYYY-MM-DD', one row per (habit, calendar day)
  UNIQUE (habit_id, checkin_date) -- co-04 constraint: the DB itself forbids a double check-in for one day
);

-- co-23: an index on each foreign key avoids an O(n) table scan per "list my habits"/"load this habit's check-ins" query
CREATE INDEX IF NOT EXISTS idx_habits_user_id ON habits (user_id);

CREATE INDEX IF NOT EXISTS idx_checkins_habit_id ON checkins (habit_id);
