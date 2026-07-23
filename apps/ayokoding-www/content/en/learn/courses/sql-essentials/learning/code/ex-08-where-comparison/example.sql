-- Example 8: Where Comparison.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price, author_id) VALUES
    (1, 'The Pragmatic Programmer', 34.99, 1),  -- => price above the threshold below
    (2, 'Clean Code', 29.99, 1),                -- => price above the threshold below
    (3, 'The Mythical Man-Month', 24.5, 2);       -- => price BELOW the threshold below

.headers on
.mode column
-- > is a comparison operator (co-08) -- keeps rows where the predicate is true.
SELECT * FROM book WHERE price > 25;
                                    -- => 34.99 and 29.99 pass the threshold; 24.5 does not
                                    -- => returns 2 rows (ids 1, 2), excludes id 3
