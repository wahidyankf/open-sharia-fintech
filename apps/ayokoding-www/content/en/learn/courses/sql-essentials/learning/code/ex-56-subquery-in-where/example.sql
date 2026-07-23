-- Example 56: Subquery in Where
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE author (                          -- => parent table -- referenced by book below
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  name TEXT NOT NULL,                         -- => author's name, required
  country TEXT                                -- => filtered by the subquery below
);

CREATE TABLE book (                            -- => child table -- author_id links back up
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  author_id INTEGER REFERENCES author(id)     -- => FK, matched against the subquery result
);

-- Two UK authors, one US author -- Grace Hopper's book should NOT appear below.
INSERT INTO author (id, name, country) VALUES  -- => 3 authors, 2 in the subquery's result set
  (1, 'Ada Lovelace', 'UK'),                  -- => UK -- id 1 IS in the subquery result
  (2, 'Grace Hopper', 'US'),                  -- => US -- id 2 is NOT in the subquery result
  (3, 'Alan Turing', 'UK');                   -- => UK -- id 3 IS in the subquery result

INSERT INTO book (id, title, author_id) VALUES -- => 4 books across the 3 authors
  (1, 'Notes on the Analytical Engine', 1),   -- => author_id 1 -- kept by the outer filter
  (2, 'Introduction to Computing', 2),        -- => author_id 2 -- excluded by the outer filter
  (3, 'On Computable Numbers', 3),            -- => author_id 3 -- kept by the outer filter
  (4, 'The Enigma Papers', 3);                -- => author_id 3 -- kept by the outer filter

-- The inner SELECT runs FIRST, producing a list of UK author ids (1, 3). The
-- outer WHERE ... IN (...) then keeps only book rows whose author_id is in
-- that list -- Grace Hopper's book (author_id 2, country US) is excluded.
SELECT title                                    -- => only the title column is needed
FROM book                                       -- => the 4-row source table above
WHERE author_id IN (                            -- => subquery result: {1, 3}
  SELECT id FROM author WHERE country = 'UK'    -- => runs first, before the outer filter
)
ORDER BY id;                                    -- => deterministic row order
