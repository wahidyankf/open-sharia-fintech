-- Example 74: Seed from SQL File -- schema.sql (structure only, no data).
-- Splitting structure from data is a common convention: schema.sql defines the shape,
-- seed.sql fills it -- each applied as its own separate sqlite3 CLI invocation (co-24).
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);  -- => the parent table
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL REFERENCES author(id));
                                    -- => the child table -- zero rows in EITHER table yet
