-- Example 25: Delete Row.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title) VALUES
    (1, 'The Pragmatic Programmer'),  -- => survives the DELETE below
    (2, 'Clean Code'),                  -- => targeted by the DELETE below
    (3, 'The Mythical Man-Month');       -- => survives the DELETE below

-- DELETE FROM ... WHERE (co-12) removes only the matching rows -- the table stays.
DELETE FROM book WHERE id = 2;     -- => row id 2 is gone permanently; ids 1 and 3 remain

-- turn on headers + column alignment so the result below reads as a table
.headers on
.mode column
SELECT * FROM book;                -- => only ids 1 and 3 remain, in that order
SELECT count(*) FROM book;         -- => count drops from 3 to 2 -- exactly one row removed
