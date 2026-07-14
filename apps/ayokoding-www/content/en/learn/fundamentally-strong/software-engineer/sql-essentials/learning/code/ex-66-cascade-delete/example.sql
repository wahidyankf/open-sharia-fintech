-- Example 66: Cascade Delete.
-- SQLite disables foreign-key ENFORCEMENT by default -- ON DELETE actions need it turned on (co-03).
PRAGMA foreign_keys = ON;          -- => a per-connection setting -- must be re-issued every connect

CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => the PARENT side of the relationship below
CREATE TABLE book(
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02)
    title TEXT NOT NULL,           -- => every book needs a title
    author_id INTEGER REFERENCES author(id) ON DELETE CASCADE
                                    -- => CASCADE propagates a parent delete to every matching child
);

INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace');
                                    -- => 1 author row -- the parent this example deletes below
INSERT INTO book(id, title, author_id) VALUES
    (1, 'Notes on the Analytical Engine', 1),
    (2, 'Sketch of the Analytical Engine', 1);
                                    -- => 2 child rows, both pointing at author 1

-- .headers on shows column names above every count(*) result below; .mode column aligns
-- them for readability -- purely display, unrelated to the CASCADE behavior below.
.headers on
.mode column
SELECT count(*) AS books_before FROM book WHERE author_id = 1;
                                    -- => 2 -- both books still reference author 1

DELETE FROM author WHERE id = 1;   -- => deletes the PARENT row -- CASCADE fires automatically
                                    -- => a SINGLE statement triggers both the parent AND child deletes

SELECT count(*) AS books_after FROM book WHERE author_id = 1;
                                    -- => 0 -- both child rows were removed too, not just orphaned
SELECT count(*) AS authors_after FROM author;
                                    -- => 0 -- the author row itself is gone
                                    -- => contrast Example 67: RESTRICT would have BLOCKED this delete
