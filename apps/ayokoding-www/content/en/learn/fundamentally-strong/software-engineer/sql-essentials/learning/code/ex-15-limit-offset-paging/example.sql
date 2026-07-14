-- Example 15: Limit Offset Paging.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price) VALUES
    (1, 'The Pragmatic Programmer', 34.99),  -- => page 1 -- skipped by OFFSET 2 below
    (2, 'Clean Code', 29.99),                -- => page 1 -- skipped by OFFSET 2 below
    (3, 'The Mythical Man-Month', 24.5),      -- => page 2 -- returned below
    (4, 'Refactoring', 39.99);                 -- => page 2 -- returned below

.headers on
.mode column
-- OFFSET (co-09) skips N rows before LIMIT starts counting -- the standard
-- "page 2 of results" pattern: page size 2, OFFSET 2 skips page 1's rows.
SELECT * FROM book ORDER BY id LIMIT 2 OFFSET 2;
                                    -- => skips ids 1-2 (page 1), returns ids 3-4 (page 2)
