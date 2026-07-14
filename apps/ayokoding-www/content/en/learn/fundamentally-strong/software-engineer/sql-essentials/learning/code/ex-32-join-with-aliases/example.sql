-- Example 32: Join with Aliases
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE author (                          -- => parent table -- referenced by book below
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  name TEXT NOT NULL                          -- => author's name, required
);

CREATE TABLE book (                            -- => child table -- author_id links back up
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  author_id INTEGER REFERENCES author(id)     -- => FK, matched against author.id below
);

INSERT INTO author (id, name) VALUES           -- => 2 authors, joined against book below
  (1, 'Ada Lovelace'),                        -- => author 1 -- has 1 book below
  (2, 'Grace Hopper');                        -- => author 2 -- has 2 books below

INSERT INTO book (id, title, author_id) VALUES -- => 3 books, referencing the 2 authors above
  (1, 'Notes on the Analytical Engine', 1),   -- => author_id 1
  (2, 'Introduction to Computing', 2),        -- => author_id 2
  (3, 'Compilers and Common Sense', 2);       -- => author_id 2, same author as row above

-- Same query as Example 31's join, written with table aliases -- `b` and `a`.
-- Aliases shorten `FROM book b JOIN author a` so `b.author_id = a.id` reads cleanly
-- without repeating the full table names in every qualified column reference.
SELECT b.title, a.name                         -- => columns pulled through both aliases
FROM book b                                    -- => `b` now stands in for `book`
JOIN author a ON b.author_id = a.id            -- => `a` now stands in for `author`
ORDER BY b.id;                                 -- => deterministic row order
