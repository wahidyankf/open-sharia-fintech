-- Example 37: Min Max Aggregate
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

CREATE TABLE book (                            -- => a single flat table, no grouping key here
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  price REAL                                  -- => min/max computed over this column
);

-- 5 books with distinct prices, ranging from 15.00 to 30.00.
INSERT INTO book (id, title, price) VALUES     -- => 5 rows, no author_id this time
  (1, 'Notes on the Analytical Engine', 25.00), -- => neither the min nor the max
  (2, 'Introduction to Computing', 18.50),      -- => neither the min nor the max
  (3, 'Compilers and Common Sense', 22.00),     -- => neither the min nor the max
  (4, 'On Computable Numbers', 30.00),          -- => the max -- priciest book
  (5, 'The Enigma Papers', 15.00);              -- => the min -- cheapest book

-- With NO GROUP BY, min()/max() collapse the ENTIRE table into a single row --
-- the cheapest and priciest book across all 5 rows, not per-group like Examples 34-36.
SELECT min(price) AS cheapest, max(price) AS priciest -- => one summary row, no grouping key
FROM book;                                      -- => the 5-row source table above
