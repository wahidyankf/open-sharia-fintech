-- Example 43: Null Three-Valued
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  published_year INTEGER                      -- => 2 of 5 rows leave this NULL
);

INSERT INTO book (id, title, published_year) VALUES -- => 5 rows, 2 with a NULL year
  (1, 'Notes on the Analytical Engine', 1843), -- => known year -- still never matches = NULL
  (2, 'Introduction to Computing', 1952),      -- => known year -- still never matches = NULL
  (3, 'Compilers and Common Sense', NULL),      -- => year genuinely unknown
  (4, 'On Computable Numbers', 1936),          -- => known year -- still never matches = NULL
  (5, 'The Enigma Papers', NULL);               -- => year genuinely unknown

-- SQL comparisons are three-valued: TRUE, FALSE, or UNKNOWN. Any comparison
-- against NULL (even `NULL = NULL`) evaluates to UNKNOWN, never TRUE -- so a
-- WHERE clause built on `= NULL` can NEVER match a row, no matter the data.
-- This returns ZERO rows, even though books 3 and 5 genuinely have a NULL year.
SELECT id, title                                -- => never reached -- WHERE matches nothing
FROM book                                       -- => the 5-row source table above
WHERE published_year = NULL                    -- => WRONG -- always UNKNOWN, never TRUE
ORDER BY id;                                    -- => deterministic row order, if any rows matched
