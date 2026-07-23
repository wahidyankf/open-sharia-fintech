-- Example 13: Order By Descending.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price) VALUES
    (1, 'The Pragmatic Programmer', 34.99),  -- => the most expensive row
    (2, 'Clean Code', 29.99),                -- => the middle-priced row
    (3, 'The Mythical Man-Month', 24.5);       -- => the cheapest row

.headers on
.mode column
-- DESC (co-09) reverses the sort direction -- highest value first, most useful
-- for "most expensive first" or "most recent first" style reports.
SELECT * FROM book ORDER BY price DESC;
                                    -- => 34.99, then 29.99, then 24.5 -- strictly decreasing
