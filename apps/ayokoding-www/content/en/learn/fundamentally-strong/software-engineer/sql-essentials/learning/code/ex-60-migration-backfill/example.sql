-- Example 60: Migration Backfill.
-- Adding a column is only half a migration -- existing rows often need a COMPUTED value,
-- not just a static DEFAULT (co-11).
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => minimal parent table -- just enough to reference below
CREATE TABLE book(
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02)
    title TEXT NOT NULL,           -- => NOT NULL -- every book needs a title
    author_id INTEGER NOT NULL REFERENCES author(id),
                                    -- => the FK link -- one row per book, per author
    price REAL NOT NULL,           -- => unit price, before the quantity multiplication below
    quantity INTEGER NOT NULL      -- => how many copies -- the OTHER input to total_value
);

INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace');
                                    -- => 1 author row -- author_id = 1 is referenced below
INSERT INTO book(id, title, author_id, price, quantity) VALUES
    (1, 'Notes on the Analytical Engine', 1, 12.5, 4),
    (2, 'Sketch of the Analytical Engine', 1, 9.0, 10);
                                    -- => 2 rows -- price and quantity now set for BOTH

-- .headers on shows column names above every result set below; .mode column aligns them --
-- both are a display preference only, with no effect on the migration itself.
.headers on
.mode column
-- A nullable ADD COLUMN (no DEFAULT) -- every existing row reads back NULL until backfilled.
ALTER TABLE book ADD COLUMN total_value REAL;
                                    -- => no DEFAULT clause -- deliberately NULL, awaiting the backfill

SELECT id, title, total_value FROM book;
                                    -- => both rows show total_value = <blank> (NULL) -- not yet computed

-- Backfill: compute the derived value for every row that just gained the new column.
UPDATE book SET total_value = price * quantity;
                                    -- => no WHERE clause -- every row needs backfilling this time (co-11)

SELECT id, title, price, quantity, total_value FROM book;
                                    -- => row 1: 12.5 * 4 = 50.0 -- row 2: 9.0 * 10 = 90.0
