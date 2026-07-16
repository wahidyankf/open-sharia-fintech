-- Capstone: hardened task API schema. Applied once at startup (unchanged mechanism from
-- Backend-Essentials); this capstone ADDS the `users` table for real password-hash-backed auth.
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'todo',
  created_at TEXT NOT NULL DEFAULT (datetime ('now'))
);

-- co-09: password_hash stores ONLY an argon2id PHC string -- this column NEVER holds a raw password.
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime ('now'))
);
