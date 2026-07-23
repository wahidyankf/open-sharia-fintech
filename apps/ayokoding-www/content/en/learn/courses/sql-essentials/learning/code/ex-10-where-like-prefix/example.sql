-- Example 10: Where Like Prefix.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL, author_id INTEGER);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, price, author_id) VALUES
    (1, 'The Pragmatic Programmer', 34.99, 1),  -- => title starts with "The "
    (2, 'Clean Code', 29.99, 1),                -- => title does NOT start with "The "
    (3, 'The Mythical Man-Month', 24.5, 2);       -- => title starts with "The "

.headers on
.mode column
-- LIKE (co-08) pattern-matches text -- % is a wildcard for zero-or-more characters.
SELECT * FROM book WHERE title LIKE 'The %';
                                    -- => matches any title starting with the literal "The "
                                    -- => returns ids 1 and 3; "Clean Code" does not match
