-- Example 45: Normalize Repeating Group (1NF)
-- Run: sqlite3 app.db < example.sql
--
-- IMPORTANT: this split fixes 1NF (atomicity) specifically -- NOT 2NF. 2NF is
-- about partial dependency on a COMPOSITE key, a different problem this single
-- split does not address.

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

-- PROBLEM: `tags` packs a variable-length list into ONE text column -- a
-- "repeating group". This column is NOT atomic (1NF requires atomic values).
CREATE TABLE book_flat (                       -- => the BEFORE table -- not yet 1NF
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  tags TEXT                                   -- => e.g. 'mathematics,history' -- not atomic
);

INSERT INTO book_flat (id, title, tags) VALUES -- => 2 rows, each packing multiple tags
  (1, 'Notes on the Analytical Engine', 'mathematics,history'),          -- => 2 tags packed
  (2, 'On Computable Numbers', 'mathematics,computer-science');          -- => 2 tags packed

-- Finding "every book tagged mathematics" here needs a fragile LIKE '%mathematics%'
-- pattern -- and it would also false-match a hypothetical tag like 'mathematics-history'.
SELECT * FROM book_flat;                        -- => shows the packed, non-atomic tags column

-- FIX: split the repeating group into its own child table, one row PER TAG.
-- Now every value in every column is a single, atomic fact -- 1NF satisfied.
CREATE TABLE book (                            -- => the AFTER hub table -- tags moved out
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL                         -- => book title, required
);

CREATE TABLE book_tag (                        -- => the AFTER child table -- one row per tag
  book_id INTEGER REFERENCES book(id),        -- => FK back to the owning book
  tag TEXT NOT NULL,                          -- => exactly ONE atomic tag per row
  PRIMARY KEY (book_id, tag)                  -- => a composite key -- no duplicate pairs
);

INSERT INTO book (id, title) VALUES            -- => same 2 books, tags no longer inline
  (1, 'Notes on the Analytical Engine'),      -- => book 1 -- 2 tags in book_tag below
  (2, 'On Computable Numbers');                -- => book 2 -- 2 tags in book_tag below

INSERT INTO book_tag (book_id, tag) VALUES     -- => 4 rows -- one row PER atomic tag
  (1, 'mathematics'),                         -- => book 1's first tag
  (1, 'history'),                             -- => book 1's second tag
  (2, 'mathematics'),                         -- => book 2's first tag
  (2, 'computer-science');                     -- => book 2's second tag

-- Now "every book tagged mathematics" is a plain, exact WHERE tag = 'mathematics'
-- on book_tag -- no string-pattern hack, no false-positive risk.
SELECT book.title, book_tag.tag                -- => one output row PER book/tag pair
FROM book                                       -- => left side of the join
JOIN book_tag ON book_tag.book_id = book.id    -- => recombines book with its atomic tags
ORDER BY book.id, book_tag.tag;                 -- => deterministic row order
