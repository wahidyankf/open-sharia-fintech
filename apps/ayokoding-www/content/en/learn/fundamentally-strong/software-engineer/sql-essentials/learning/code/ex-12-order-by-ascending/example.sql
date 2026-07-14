-- Example 12: Order By Ascending.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price) VALUES
    (1, 'The Pragmatic Programmer', 34.99),  -- => stored first, but storage order != output order
    (2, 'Clean Code', 29.99),                -- => stored second
    (3, 'The Mythical Man-Month', 24.5);       -- => stored third

-- turn on headers + column alignment so the sorted result reads as a table
.headers on
.mode column
-- ORDER BY (co-09) sorts the result set; ASC (the default) sorts low-to-high / A-to-Z.
SELECT * FROM book ORDER BY title ASC;
                                    -- => "Clean Code" sorts before "The..." titles alphabetically
