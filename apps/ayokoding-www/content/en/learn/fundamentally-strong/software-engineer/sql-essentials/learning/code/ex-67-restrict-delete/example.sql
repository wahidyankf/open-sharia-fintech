-- Example 67: Restrict Delete.
PRAGMA foreign_keys = ON;          -- => enforcement must be on for RESTRICT to actually block anything

CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => the PARENT side -- the row this example tries to delete
CREATE TABLE book(
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02)
    title TEXT NOT NULL,           -- => every book needs a title
    author_id INTEGER REFERENCES author(id) ON DELETE RESTRICT
                                    -- => RESTRICT is the opposite of CASCADE: blocks the parent delete
);

INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace');
                                    -- => 1 author row -- still referenced by the book below
INSERT INTO book(id, title, author_id) VALUES (1, 'Notes on the Analytical Engine', 1);
                                    -- => the ONE child row that makes the delete below illegal

-- .headers on and .mode column below are display preferences, consistent with every other
-- example in this tier -- they have no bearing on the RESTRICT behavior demonstrated next.
.headers on
.mode column
-- Blocked: author 1 still has a referencing book row -- RESTRICT rejects this delete outright.
DELETE FROM author WHERE id = 1;   -- => fails -- the engine refuses to orphan the book row above
                                    -- => contrast Example 66: CASCADE ALLOWS this same shape of delete
