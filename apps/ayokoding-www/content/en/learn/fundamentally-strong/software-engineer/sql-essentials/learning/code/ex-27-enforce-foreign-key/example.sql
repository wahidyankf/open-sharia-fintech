-- Example 27: Enforce Foreign Key.
-- CRITICAL: foreign keys are OFF by default in SQLite -- this pragma must run per
-- connection, every time, or REFERENCES clauses are decoration only (co-03).
PRAGMA foreign_keys=ON;

CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => author table exists, currently empty -- no id 99 in it
CREATE TABLE book(
    id INTEGER PRIMARY KEY,        -- => book's own primary key
    title TEXT NOT NULL,           -- => every book must have a title
    author_id INTEGER REFERENCES author(id)
    -- => REFERENCES alone does nothing without the PRAGMA above -- both are required
);

-- author_id 99 does not exist in the author table -- an orphan reference.
INSERT INTO book(title, author_id) VALUES('Ghost Book', 99);
                                    -- => with the pragma ON, the engine checks the reference first
                                    -- => raises: FOREIGN KEY constraint failed

.headers on
.mode column
SELECT count(*) FROM book;         -- => confirms the rejected row never landed -- table stays empty
