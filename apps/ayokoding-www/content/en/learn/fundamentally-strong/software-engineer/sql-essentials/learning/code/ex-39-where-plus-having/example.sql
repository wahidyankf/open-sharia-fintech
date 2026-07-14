-- Example 39: Where Plus Having
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  author_id INTEGER,                          -- => the grouping key for sum() below
  price REAL,                                 -- => summed per group after WHERE filters
  in_stock INTEGER                            -- => 1 = in stock, 0 = out of stock
);

-- Book id 3 is the ONLY out-of-stock row -- watch it disappear before grouping.
INSERT INTO book (id, title, author_id, price, in_stock) VALUES -- => 5 rows, 1 out-of-stock
  (1, 'Notes on the Analytical Engine', 1, 25.00, 1),   -- => in stock -- survives WHERE
  (2, 'Introduction to Computing',       2, 18.50, 1),  -- => in stock -- survives WHERE
  (3, 'Compilers and Common Sense',      2, 22.00, 0),   -- => dropped by WHERE, first
  (4, 'On Computable Numbers',           3, 30.00, 1),  -- => in stock -- survives WHERE
  (5, 'The Enigma Papers',               3, 15.00, 1);  -- => in stock -- survives WHERE

-- Two filters, two different phases. WHERE runs FIRST, on individual rows, before
-- any grouping happens -- it removes book id 3 (in_stock = 0) entirely. GROUP BY
-- then collapses the SURVIVING rows. HAVING runs LAST, on the resulting groups --
-- author_id 2's remaining sum (18.50, book id 3 already gone) fails the > 20 test.
SELECT author_id, sum(price) AS total_price    -- => sum(price) per surviving group
FROM book                                       -- => the 5-row source table above
WHERE in_stock = 1                             -- => row filter -- BEFORE aggregation
GROUP BY author_id                             -- => collapse the surviving rows
HAVING sum(price) > 20                         -- => group filter -- AFTER aggregation
ORDER BY author_id;                            -- => deterministic group order
