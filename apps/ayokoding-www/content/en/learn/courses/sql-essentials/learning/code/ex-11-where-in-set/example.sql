-- Example 11: Where In Set.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price, author_id) VALUES
    (1, 'The Pragmatic Programmer', 34.99, 1),  -- => id in the set below
    (2, 'Clean Code', 29.99, 1),                -- => id NOT in the set below
    (3, 'The Mythical Man-Month', 24.5, 2);       -- => id in the set below

.headers on
.mode column
-- IN (co-08) tests set membership -- shorthand for chained OR-equality checks.
SELECT * FROM book WHERE id IN (1, 3);
                                    -- => keeps rows whose id matches ANY value in the list
                                    -- => returns ids 1 and 3, skips id 2
