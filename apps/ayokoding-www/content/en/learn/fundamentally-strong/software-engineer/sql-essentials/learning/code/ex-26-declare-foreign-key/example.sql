-- Example 26: Declare Foreign Key.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => author table exists -- the FK below will point at it

-- REFERENCES (co-03) declares that book.author_id must point at a real author.id --
-- a static, self-documenting invariant that lives in the schema itself.
CREATE TABLE book(
    id INTEGER PRIMARY KEY,        -- => book's own primary key
    title TEXT NOT NULL,           -- => every book must have a title
    author_id INTEGER REFERENCES author(id)
                                    -- => declares the FK -- enforcement is a SEPARATE step (Example 27)
);

-- .schema prints back the stored definition -- proof the REFERENCES clause was kept.
.schema book
