-- Example 7: Where Equality.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price, author_id) VALUES
    (1, 'The Pragmatic Programmer', 34.99, 1),  -- => id 1
    (2, 'Clean Code', 29.99, 1),                -- => id 2
    (3, 'The Mythical Man-Month', 24.5, 2);       -- => id 3

-- turn on headers + column alignment so the result below reads as a table
.headers on
.mode column
-- WHERE selects rows (co-08) -- = tests exact equality, evaluated per row before output.
SELECT * FROM book WHERE id = 1;   -- => keeps only the row whose id equals 1 -- exactly one row
