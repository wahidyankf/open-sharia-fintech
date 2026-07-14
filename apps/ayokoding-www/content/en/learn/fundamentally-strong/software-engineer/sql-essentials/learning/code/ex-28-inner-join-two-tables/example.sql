-- Example 28: Inner Join Two Tables.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => author table exists, currently empty
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER REFERENCES author(id));
                                    -- => book table exists, currently empty
INSERT INTO author(id, name) VALUES
    (1, 'Ada Lovelace'),            -- => referenced by book row 1 below
    (2, 'Grace Hopper');             -- => referenced by book row 2 below
INSERT INTO book(title, author_id) VALUES
    ('Notes on the Analytical Engine', 1),  -- => author_id 1 -- pairs with Ada Lovelace
    ('Compilers and Computers', 2);           -- => author_id 2 -- pairs with Grace Hopper

-- turn on headers + column alignment so the joined result reads as a table
.headers on
.mode column
-- JOIN ... ON (co-13) recombines normalized data -- matches book.author_id to author.id,
-- row by row, and only rows with a match on BOTH sides appear in the output.
SELECT book.title, author.name
FROM book                          -- => the left side of the join -- one row per book
JOIN author ON book.author_id = author.id;
                                    -- => the ON clause -- the exact key equality the join tests
                                    -- => each book row pairs with exactly its own author's name
