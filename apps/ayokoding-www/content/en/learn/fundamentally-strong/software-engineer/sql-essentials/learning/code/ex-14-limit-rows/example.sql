-- Example 14: Limit Rows.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price) VALUES
    (1, 'The Pragmatic Programmer', 34.99),  -- => row 1 -- kept by LIMIT 2 below
    (2, 'Clean Code', 29.99),                -- => row 2 -- kept by LIMIT 2 below
    (3, 'The Mythical Man-Month', 24.5);       -- => row 3 -- cut off by LIMIT 2 below

.headers on
.mode column
-- LIMIT (co-09) caps the row count the engine returns -- evaluated AFTER ORDER BY,
-- so pair it with ORDER BY whenever "first N" needs to mean something specific.
SELECT * FROM book LIMIT 2;        -- => stops after 2 rows even though 3 rows match overall
