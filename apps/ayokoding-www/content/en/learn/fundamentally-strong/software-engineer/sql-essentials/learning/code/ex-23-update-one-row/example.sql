-- Example 23: Update One Row.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price) VALUES
    (1, 'The Pragmatic Programmer', 34.99),  -- => the row the WHERE clause below will match
    (2, 'Clean Code', 29.99);                  -- => not matched -- stays untouched below

-- UPDATE ... SET ... WHERE (co-11) mutates only the rows the WHERE clause matches.
UPDATE book SET price = 15 WHERE id = 1;
                                    -- => only the row with id = 1 changes -- id 2 is untouched

-- turn on headers + column alignment so the result below reads as a table
.headers on
.mode column
SELECT * FROM book;                -- => id 1 now shows 15.0, id 2 still shows its original 29.99
