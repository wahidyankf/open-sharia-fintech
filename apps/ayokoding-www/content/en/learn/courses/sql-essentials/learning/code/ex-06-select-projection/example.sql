-- Example 6: Select Projection.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price, author_id) VALUES
    (1, 'The Pragmatic Programmer', 34.99, 1),  -- => row 1
    (2, 'Clean Code', 29.99, 1),                -- => row 2
    (3, 'The Mythical Man-Month', 24.5, 2);       -- => row 3

.headers on
.mode column
-- Naming one column instead of * (co-08) is projection -- fewer columns come back,
-- same number of rows. price/author_id never leave the engine for this query.
SELECT title FROM book;            -- => returns only the title column, all 3 rows
