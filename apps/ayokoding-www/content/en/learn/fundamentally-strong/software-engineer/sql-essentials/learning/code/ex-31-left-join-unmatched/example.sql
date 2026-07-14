-- Example 31: Left Join Unmatched
-- Run: sqlite3 app.db < example.sql

-- Dot-commands (CLI-only, no trailing comment allowed on their own line):
-- print column headers, align into columns, and spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

-- Schema: author (parent) and book (child, referencing author via author_id).
CREATE TABLE author (                          -- => parent table -- referenced by book below
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned on insert
  name TEXT NOT NULL,                         -- => every author needs a name
  country TEXT                                -- => nullable -- not used in this example
);

CREATE TABLE book (                            -- => child table -- author_id links back up
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned on insert
  title TEXT NOT NULL,                        -- => every book needs a title
  author_id INTEGER REFERENCES author(id)     -- => FK -- not enforced without PRAGMA foreign_keys=ON
);

-- 4 authors -- Margaret Hamilton (id 4) deliberately has ZERO books below.
INSERT INTO author (id, name, country) VALUES
  (1, 'Ada Lovelace', 'UK'),                  -- => author 1 -- has 1 book below
  (2, 'Grace Hopper', 'US'),                  -- => author 2 -- has 2 books below
  (3, 'Alan Turing', 'UK'),                   -- => author 3 -- has 2 books below
  (4, 'Margaret Hamilton', 'US');              -- => no book row references author_id 4

-- Only 5 books, spread across authors 1-3 -- author 4 is never referenced.
INSERT INTO book (id, title, author_id) VALUES
  (1, 'Notes on the Analytical Engine', 1),   -- => author_id 1
  (2, 'Introduction to Computing', 2),        -- => author_id 2
  (3, 'Compilers and Common Sense', 2),       -- => author_id 2, same author as row above
  (4, 'On Computable Numbers', 3),            -- => author_id 3
  (5, 'The Enigma Papers', 3);                -- => author_id 3, same author as row above

-- An INNER JOIN here would silently DROP Margaret Hamilton -- she has no match.
-- LEFT JOIN keeps every row from the LEFT table (author), regardless of a match.
SELECT author.name, book.title                -- => columns pulled from BOTH tables
FROM author                                    -- => left table -- every row is kept
LEFT JOIN book ON book.author_id = author.id   -- => right side (book) may be all-NULL per row
ORDER BY author.id;                             -- => deterministic, stable row order
