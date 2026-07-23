-- Example 76: Integrity Checks.
PRAGMA foreign_keys = ON;          -- => enforcement on -- relevant to foreign_key_check below
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => the parent table foreign_key_check will verify against
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER REFERENCES author(id));
                                    -- => the child table -- its FK is what gets checked below
INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace');
                                    -- => 1 author row -- author_id = 1 is referenced below
INSERT INTO book(id, title, author_id) VALUES (1, 'Notes on the Analytical Engine', 1);
                                    -- => 1 book row, correctly referencing an EXISTING author

-- .headers on and .mode column below are display preferences only -- unrelated to the checks.
.headers on
.mode column
-- integrity_check walks the B-tree structure itself -- page corruption, not foreign keys (co-24).
PRAGMA integrity_check;            -- => "ok" means the on-disk structure is sound

-- integrity_check deliberately does NOT check foreign keys -- foreign_key_check does that instead.
PRAGMA foreign_key_check;          -- => zero ROWS returned means zero foreign-key violations (co-03)
