-- Example 24: Update All Rows.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, in_stock INTEGER NOT NULL DEFAULT 0);
                                    -- => book table exists, currently empty
INSERT INTO book(id, title, in_stock) VALUES
    (1, 'The Pragmatic Programmer', 0),  -- => starts out of stock
    (2, 'Clean Code', 0);                  -- => starts out of stock

-- No WHERE clause (co-11) means the predicate is implicitly "true for every row" --
-- UPDATE touches the entire table. This is easy to do by accident -- always double-check.
UPDATE book SET in_stock = 1;
                                    -- => every row's in_stock flips from 0 to 1, no exceptions

.headers on
.mode column
SELECT * FROM book;                -- => both rows now show in_stock = 1
