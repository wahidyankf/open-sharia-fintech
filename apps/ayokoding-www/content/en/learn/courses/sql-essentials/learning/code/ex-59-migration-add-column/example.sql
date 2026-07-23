-- Example 59: Migration Add Column.
-- An additive migration -- adding a nullable-or-defaulted column -- never breaks existing rows.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => a minimal parent table -- just enough for a book to reference
CREATE TABLE book(
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02) -- auto-assigned on insert
    title TEXT NOT NULL,           -- => every book needs a title -- NOT NULL enforced
    author_id INTEGER NOT NULL REFERENCES author(id),
                                    -- => the FK link -- declared, though not yet enforced (co-03)
    price REAL NOT NULL            -- => the schema BEFORE this example's migration runs
);

INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace');
                                    -- => 1 author row -- author_id = 1 will be referenced below
INSERT INTO book(id, title, author_id, price) VALUES
    (1, 'Notes on the Analytical Engine', 1, 12.5),
    (2, 'Sketch of the Analytical Engine', 1, 9.0);
                                    -- => book now holds 2 rows, written BEFORE the migration below

.headers on
.mode column
-- The pre-migration shape -- no "edition" column exists yet.
SELECT id, title, price FROM book; -- => 2 rows, 3 columns -- the schema before any change

-- ADD COLUMN ... DEFAULT is SQLite's safe, additive migration: no table rewrite,
-- no downtime, and every EXISTING row reads back with the declared default (co-22).
ALTER TABLE book ADD COLUMN edition INTEGER DEFAULT 1;
                                    -- => rewrites ONLY the schema catalog -- row data is untouched

-- Same 2 rows, now with a 4th column -- both pre-existing rows got the default, not NULL.
SELECT id, title, price, edition FROM book;
                                    -- => edition is 1 for BOTH rows -- neither was NULL or dropped
