-- Example 46: Normalize Transitive Dependency (3NF)
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

-- PROBLEM: publisher_city depends on publisher_name, NOT directly on id -- a
-- TRANSITIVE dependency (id -> publisher_name -> publisher_city). Both books
-- from 'Oxford Press' repeat 'Oxford' -- change one city and the other silently
-- goes stale, an update anomaly 3NF exists specifically to prevent.
CREATE TABLE book_wide (                       -- => the BEFORE table -- not yet 3NF
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  publisher_name TEXT NOT NULL,               -- => repeated fact, one copy per book row
  publisher_city TEXT NOT NULL                -- => repeated fact, one copy per book row
);

INSERT INTO book_wide (id, title, publisher_name, publisher_city) VALUES -- => 3 rows
  (1, 'Notes on the Analytical Engine', 'Oxford Press', 'Oxford'),        -- => 'Oxford' repeated below
  (2, 'On Computable Numbers', 'Oxford Press', 'Oxford'),      -- => 'Oxford' repeated
  (3, 'Introduction to Computing', 'Harbor Books', 'Boston');  -- => a different publisher

SELECT * FROM book_wide;                        -- => shows publisher_city repeated twice

-- FIX: extract publisher into its own table -- publisher_city now lives in
-- exactly ONE row per publisher, referenced by id instead of copied by value.
CREATE TABLE publisher (                       -- => the AFTER lookup table -- one row per publisher
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  name TEXT NOT NULL,                         -- => publisher's name, required
  city TEXT NOT NULL                          -- => one fact, one place -- 3NF
);

CREATE TABLE book (                            -- => the AFTER hub table -- FK instead of copies
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  publisher_id INTEGER REFERENCES publisher(id) -- => FK -- no more repeated publisher text
);

INSERT INTO publisher (id, name, city) VALUES  -- => 2 publishers, each stored exactly once
  (1, 'Oxford Press', 'Oxford'),               -- => publisher 1 -- referenced by 2 books below
  (2, 'Harbor Books', 'Boston');                -- => publisher 2 -- referenced by 1 book below

INSERT INTO book (id, title, publisher_id) VALUES -- => same 3 books, publisher_city no longer inline
  (1, 'Notes on the Analytical Engine', 1),   -- => publisher_id 1
  (2, 'On Computable Numbers', 1),             -- => shares publisher_id 1, not the city text
  (3, 'Introduction to Computing', 2);         -- => publisher_id 2

-- Updating Oxford Press's city now means changing ONE row (publisher.city) --
-- both of its books pick up the change automatically through the join.
SELECT book.title, publisher.name, publisher.city -- => city now read through the join
FROM book                                       -- => left side of the join
JOIN publisher ON publisher.id = book.publisher_id -- => recombines book with its publisher
ORDER BY book.id;                               -- => deterministic row order
