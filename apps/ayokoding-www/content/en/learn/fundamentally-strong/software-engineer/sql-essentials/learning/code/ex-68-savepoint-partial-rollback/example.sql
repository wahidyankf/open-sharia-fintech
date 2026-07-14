-- Example 68: Savepoint Partial Rollback.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
                                    -- => a single table -- enough to demonstrate the savepoint dance

-- .headers on shows column names above the final SELECT below; .mode column aligns the
-- display -- both are readability preferences, set before the transaction even opens.
.headers on
.mode column
BEGIN;                              -- => opens the OUTER transaction (co-18)
INSERT INTO book(id, title, price) VALUES (1, 'Notes on the Analytical Engine', 12.5);
                                    -- => row 1 -- committed at the END, along with row 3 below

SAVEPOINT sp;                       -- => marks a point INSIDE the still-open transaction
INSERT INTO book(id, title, price) VALUES (2, 'Bad Draft', -5.0);
                                    -- => a mistake we want to undo WITHOUT losing row 1 too
ROLLBACK TO sp;                     -- => undoes ONLY work since sp -- the outer transaction stays open

INSERT INTO book(id, title, price) VALUES (3, 'Sketch of the Analytical Engine', 9.0);
                                    -- => row 3 -- inserted AFTER the rollback, in the same transaction
COMMIT;                             -- => finalizes rows 1 and 3 -- row 2 never existed past the savepoint

SELECT id, title, price FROM book;  -- => 2 rows: ids 1 and 3 -- the bad draft (id 2) is nowhere
