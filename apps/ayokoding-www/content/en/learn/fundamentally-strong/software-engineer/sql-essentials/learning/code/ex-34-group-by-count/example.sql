-- Example 34: Group By Count
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => single flat table -- no author table here
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  author_id INTEGER,                          -- => no FK needed -- just a grouping key here
  price REAL,                                 -- => not used by this example's query
  in_stock INTEGER,                           -- => not used by this example's query
  published_year INTEGER                      -- => not used by this example's query
);

-- 5 books: author_id 1 has 1 book, author_id 2 has 2, author_id 3 has 2.
INSERT INTO book (id, title, author_id, price, in_stock, published_year) VALUES
  (1, 'Notes on the Analytical Engine', 1, 25.00, 1, 1843),  -- => author_id 1, group of 1
  (2, 'Introduction to Computing',       2, 18.50, 1, 1952), -- => author_id 2, group of 2
  (3, 'Compilers and Common Sense',      2, 22.00, 0, NULL), -- => author_id 2, group of 2
  (4, 'On Computable Numbers',           3, 30.00, 1, 1936), -- => author_id 3, group of 2
  (5, 'The Enigma Papers',               3, 15.00, 1, NULL); -- => author_id 3, group of 2

-- GROUP BY collapses rows sharing the same author_id into one row per group;
-- count(*) then counts how many original rows collapsed into each group.
SELECT author_id, count(*) AS book_count       -- => count(*) per group, computed below
FROM book                                       -- => the 5-row source table above
GROUP BY author_id                             -- => one output row per distinct author_id
ORDER BY author_id;                            -- => deterministic group order
