-- Example 55: Upsert On Conflict
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table
  id INTEGER PRIMARY KEY,                     -- => the conflict target below
  title TEXT NOT NULL,                        -- => book title, required
  price REAL                                  -- => the column the upsert corrects
);

-- First insert: a plain new row, id 1.
INSERT INTO book (id, title, price) VALUES (1, 'On Computable Numbers', 30.00); -- => row exists now

SELECT * FROM book;                             -- => one row, price 30.00

-- Second "insert" targets the SAME id (1) -- a plain INSERT here would raise a
-- UNIQUE/PRIMARY KEY constraint error. ON CONFLICT(id) DO UPDATE turns that
-- error into an UPDATE instead: an "upsert" -- insert if new, update if it exists.
INSERT INTO book (id, title, price)             -- => targets the same id as the first insert
VALUES (1, 'On Computable Numbers', 32.50)      -- => same id 1, a corrected price
ON CONFLICT (id) DO UPDATE SET                  -- => fires because id 1 already exists
  price = excluded.price;                       -- => excluded.price is the NEW attempted value

SELECT * FROM book;                             -- => still ONE row, price now 32.50
