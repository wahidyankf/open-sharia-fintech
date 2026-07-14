-- Example 5: Select All Columns.
-- SELECT * (co-08) projects every declared column, in declaration order.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty (0 rows)
INSERT INTO book(id, title, price, author_id) VALUES
    (1, 'The Pragmatic Programmer', 34.99, 1),  -- => row 1: author_id 1
    (2, 'Clean Code', 29.99, 1),                -- => row 2: same author_id 1
    (3, 'The Mythical Man-Month', 24.5, 2);       -- => row 3: a different author_id
                                    -- => book now holds 3 rows across 4 columns each

.headers on
.mode column
SELECT * FROM book;                -- => returns all 3 rows, all 4 columns -- the full relation
