-- Example 42: Null Coalesce
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
  (1, 'Notes on the Analytical Engine', 1843), -- => known year -- coalesce() passes it through
  (2, 'Introduction to Computing', 1952),      -- => known year -- coalesce() passes it through
  (3, 'Compilers and Common Sense', NULL),      -- => becomes 0 below, not left blank
  (4, 'On Computable Numbers', 1936),          -- => known year -- coalesce() passes it through
  (5, 'The Enigma Papers', NULL);               -- => becomes 0 below, not left blank

-- coalesce(a, b, ...) returns the FIRST non-NULL argument, left to right -- here,
-- published_year if it exists, otherwise the literal 0 as a placeholder value.
SELECT id, title, coalesce(published_year, 0) AS year_or_zero
                                                 -- => year_or_zero never shows NULL
FROM book                                       -- => the 5-row source table above
ORDER BY id;                                    -- => deterministic row order
