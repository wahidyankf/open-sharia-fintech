-- Example 77: Design a 3NF Schema.
-- Four relations, each holding ONE fact-type, related purely by key values (co-01, co-05):
CREATE TABLE author(                -- => relation 1 of 4 -- one row per author
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02)
    name TEXT NOT NULL             -- => the ONE fact-type this table holds
);                                  -- => an author's facts live HERE, nowhere else (co-07)

CREATE TABLE publisher(             -- => relation 2 of 4 -- INDEPENDENT of author, no shared row
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02)
    name TEXT NOT NULL,            -- => a SECOND, independent fact-type -- its own table
    city TEXT                      -- => city depends ONLY on publisher.id -- no transitive path
);                                  -- => a publisher's facts live HERE, nowhere else

CREATE TABLE book(                  -- => relation 3 of 4 -- the table with the MOST foreign keys
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02)
    title TEXT NOT NULL,           -- => the book's OWN fact -- not duplicated from anywhere
    author_id INTEGER NOT NULL REFERENCES author(id),
                                    -- => book POINTS AT an author -- never repeats the author's name
    publisher_id INTEGER REFERENCES publisher(id),
                                    -- => book POINTS AT a publisher -- never repeats its city
    price REAL NOT NULL            -- => a fact about THIS book -- not about its author or publisher
);                                  -- => a book's facts live HERE, nowhere else

CREATE TABLE tag(                   -- => relation 4 of 4 -- a controlled vocabulary of labels
    id INTEGER PRIMARY KEY,        -- => aliases rowid (co-02)
    name TEXT NOT NULL UNIQUE      -- => UNIQUE (co-04) -- 'history' can only exist as ONE row
);                                  -- => a tag's facts live HERE, nowhere else

CREATE TABLE book_tag(              -- => the many-to-many JUNCTION -- not a "5th fact-type" table
    book_id INTEGER NOT NULL REFERENCES book(id),
                                    -- => FK half of the composite key (Example 65's pattern)
    tag_id INTEGER NOT NULL REFERENCES tag(id),
                                    -- => the OTHER FK half of the composite key
    PRIMARY KEY (book_id, tag_id)  -- => the many-to-many junction from Example 65, reused here
);                                  -- => book_tag holds ONLY key pairs -- no other columns at all

-- .schema (no argument) prints EVERY stored CREATE TABLE -- proof the design landed as intended.
.schema
