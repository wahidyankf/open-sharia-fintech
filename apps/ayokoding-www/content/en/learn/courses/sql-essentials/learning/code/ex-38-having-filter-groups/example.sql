-- Example 38: Having Filter Groups
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  author_id INTEGER                           -- => the grouping key HAVING filters on
);

-- author_id 1 has 1 book, author_id 2 has 2 books, author_id 3 has 2 books.
INSERT INTO book (id, title, author_id) VALUES -- => 5 books across 3 author_id groups
  (1, 'Notes on the Analytical Engine', 1),   -- => author_id 1, group of 1 -- fails HAVING
  (2, 'Introduction to Computing', 2),        -- => author_id 2, group of 2 -- passes HAVING
  (3, 'Compilers and Common Sense', 2),       -- => author_id 2, group of 2 -- passes HAVING
  (4, 'On Computable Numbers', 3),            -- => author_id 3, group of 2 -- passes HAVING
  (5, 'The Enigma Papers', 3);                -- => author_id 3, group of 2 -- passes HAVING

-- HAVING filters GROUPS after aggregation -- the opposite of WHERE, which filters
-- ROWS before aggregation. count(*) > 1 keeps only groups with more than one book,
-- so author_id 1 (exactly 1 book) is dropped from the result entirely.
SELECT author_id, count(*) AS book_count       -- => count(*) per surviving group
FROM book                                       -- => the 5-row source table above
GROUP BY author_id                             -- => first, collapse rows into groups
HAVING count(*) > 1                            -- => then, keep only groups matching this
ORDER BY author_id;                            -- => deterministic group order
