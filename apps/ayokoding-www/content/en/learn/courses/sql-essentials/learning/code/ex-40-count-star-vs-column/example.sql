-- Example 40: Count Star vs Column
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  published_year INTEGER                      -- => 2 of the 5 rows leave this NULL
);

-- Books 3 and 5 have an unknown (NULL) published_year.
INSERT INTO book (id, title, published_year) VALUES -- => 5 rows, 2 with a NULL year
  (1, 'Notes on the Analytical Engine', 1843), -- => known year -- counted by both forms
  (2, 'Introduction to Computing', 1952),      -- => known year -- counted by both forms
  (3, 'Compilers and Common Sense', NULL),      -- => unknown year -- excluded below
  (4, 'On Computable Numbers', 1936),          -- => known year -- counted by both forms
  (5, 'The Enigma Papers', NULL);               -- => unknown year -- excluded below

-- count(*) counts ROWS, full stop -- NULLs included. count(column) counts only
-- NON-NULL values in that specific column -- the two forms diverge whenever the
-- counted column itself can hold NULL, exactly like published_year here.
SELECT count(*) AS row_count, count(published_year) AS known_year_count
                                                 -- => two different counts, same table
FROM book;                                      -- => the 5-row source table above
