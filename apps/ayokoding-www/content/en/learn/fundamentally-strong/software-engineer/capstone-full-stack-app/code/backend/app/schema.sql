-- Full-stack capstone: tasks table (topic 10 SQL Essentials). Reused from Backend Essentials'
-- own capstone schema -- one normalized table, applied once at startup by repository.py's
-- init_db(), safe to call repeatedly.
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'todo',
  created_at TEXT NOT NULL DEFAULT (datetime ('now'))
);
