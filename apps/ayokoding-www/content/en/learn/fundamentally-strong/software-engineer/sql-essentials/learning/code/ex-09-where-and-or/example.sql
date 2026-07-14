-- Example 9: Where And Or.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price, author_id) VALUES
    (1, 'The Pragmatic Programmer', 34.99, 1),  -- => passes both conditions below
    (2, 'Clean Code', 29.99, 1),                -- => passes both conditions below
    (3, 'The Mythical Man-Month', 24.5, 2),      -- => fails author_id = 1
    (4, 'Cheap Notes', 5.0, 1);                   -- => fails price > 10

.headers on
.mode column
-- AND (co-08) keeps a row only when BOTH predicates evaluate true for that row.
SELECT * FROM book WHERE price > 10 AND author_id = 1;
                                    -- => id 3 excluded by author_id, id 4 excluded by price
                                    -- => returns exactly ids 1 and 2
