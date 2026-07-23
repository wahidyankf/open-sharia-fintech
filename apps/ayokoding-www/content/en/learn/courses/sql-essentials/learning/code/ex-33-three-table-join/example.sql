-- Example 33: Three-Table Join
-- Run: sqlite3 app.db < example.sql

-- Dot-commands: print headers, align columns, spell out NULL instead of blank.
.headers on
.mode column
.nullvalue NULL

-- Three related tables: author and publisher are both parents of book.
CREATE TABLE author (                          -- => first parent table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  name TEXT NOT NULL                          -- => author's name, required
);

CREATE TABLE publisher (                       -- => second parent table
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  name TEXT NOT NULL                          -- => publisher's name, required
);

CREATE TABLE book (                            -- => hub table -- has TWO parents
  id INTEGER PRIMARY KEY,                     -- => aliases rowid, auto-assigned
  title TEXT NOT NULL,                        -- => book title, required
  author_id INTEGER REFERENCES author(id),     -- => FK #1 -- links to author
  publisher_id INTEGER REFERENCES publisher(id) -- => FK #2 -- links to publisher
);
-- Both FKs are simple (single-column), unlike Example 65's composite key.

INSERT INTO author (id, name) VALUES           -- => 2 authors, both referenced below
  (1, 'Ada Lovelace'),                        -- => author 1 -- writes 1 book below
  (2, 'Alan Turing');                         -- => author 2 -- writes 2 books below

INSERT INTO publisher (id, name) VALUES        -- => 2 publishers, both referenced below
  (1, 'Oxford Press'),                        -- => publisher 1 -- publishes 2 books below
  (2, 'Harbor Books');                        -- => publisher 2 -- publishes 1 book below

INSERT INTO book (id, title, author_id, publisher_id) VALUES -- => links both parent FKs
  (1, 'Notes on the Analytical Engine', 1, 1),   -- => Ada Lovelace, Oxford Press
  (2, 'On Computable Numbers', 2, 1),            -- => Alan Turing, Oxford Press
  (3, 'The Enigma Papers', 2, 2);                -- => Alan Turing, Harbor Books

-- Two JOIN clauses chain together -- book is the hub, author and publisher are
-- both its parents. Each JOIN adds one more parent table's columns to the row.
SELECT book.title, author.name AS author_name, publisher.name AS publisher_name
                                                 -- => columns pulled from all three tables
FROM book                                       -- => hub table -- the join starts here
JOIN author ON author.id = book.author_id          -- => pulls in the author's columns
JOIN publisher ON publisher.id = book.publisher_id  -- => pulls in the publisher's columns
ORDER BY book.id;                                    -- => deterministic row order
