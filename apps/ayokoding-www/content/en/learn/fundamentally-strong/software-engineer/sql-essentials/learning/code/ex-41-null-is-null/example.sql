-- Example 41: Null Is Null
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  published_year INTEGER                      -- => unknown for 2 of the 5 rows
);

INSERT INTO book (id, title, published_year) VALUES -- => 5 rows, 2 with a NULL year
  (1, 'Notes on the Analytical Engine', 1843), -- => known year -- excluded from result
  (2, 'Introduction to Computing', 1952),      -- => known year -- excluded from result
  (3, 'Compilers and Common Sense', NULL),      -- => year genuinely unknown
  (4, 'On Computable Numbers', 1936),          -- => known year -- excluded from result
  (5, 'The Enigma Papers', NULL);               -- => year genuinely unknown

-- NULL means "unknown", not zero or empty string -- so testing for it needs its
-- own operator. IS NULL is that operator; Example 43 shows why `= NULL` fails.
SELECT id, title                                -- => the two columns shown for matches
FROM book                                       -- => the 5-row source table above
WHERE published_year IS NULL                   -- => matches exactly the 2 unknown rows
ORDER BY id;                                    -- => deterministic row order
