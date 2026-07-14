-- Example 36: Group By Avg
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => single flat table, same shape as Example 34
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  author_id INTEGER,                          -- => the grouping key for avg() below
  price REAL,                                 -- => averaged per group below
  in_stock INTEGER,                           -- => not used by this example's query
  published_year INTEGER                      -- => not used by this example's query
);

-- Same 5-book dataset used across this tier's aggregation examples.
INSERT INTO book (id, title, author_id, price, in_stock, published_year) VALUES
  (1, 'Notes on the Analytical Engine', 1, 25.00, 1, 1843),  -- => author_id 1, price 25.00
  (2, 'Introduction to Computing',       2, 18.50, 1, 1952), -- => author_id 2, price 18.50
  (3, 'Compilers and Common Sense',      2, 22.00, 0, NULL), -- => author_id 2, price 22.00
  (4, 'On Computable Numbers',           3, 30.00, 1, 1936), -- => author_id 3, price 30.00
  (5, 'The Enigma Papers',               3, 15.00, 1, NULL); -- => author_id 3, price 15.00

-- avg(price) computes the mean price WITHIN each author_id group -- author_id 2's
-- (18.50 + 22.00) / 2 = 20.25, author_id 3's (30.00 + 15.00) / 2 = 22.5.
SELECT author_id, avg(price) AS avg_price      -- => avg(price) per group, computed below
FROM book                                       -- => the 5-row source table above
GROUP BY author_id                             -- => one output row per distinct author_id
ORDER BY author_id;                            -- => deterministic group order
