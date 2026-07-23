-- Example 65: Composite Primary Key.
-- A junction table's identity is the PAIR of foreign keys, not a surrogate id column (co-02, co-05).
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL);
                                    -- => minimal parent -- just enough for book_tag to reference
CREATE TABLE tag(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => the OTHER parent -- book_tag links book to tag, many-to-many
CREATE TABLE book_tag(
    book_id INTEGER NOT NULL REFERENCES book(id),
                                    -- => FK half of the composite key
    tag_id INTEGER NOT NULL REFERENCES tag(id),
                                    -- => the OTHER FK half of the composite key
    PRIMARY KEY (book_id, tag_id)  -- => the PAIR must be unique -- no separate id column needed
);

INSERT INTO book(id, title) VALUES (1, 'Notes on the Analytical Engine');
                                    -- => 1 book row -- book_id = 1 is referenced below
INSERT INTO tag(id, name) VALUES (1, 'history'), (2, 'computing');
                                    -- => 2 tag rows -- tag_id 1 and 2 are referenced below

-- .headers on and .mode column below are display preferences only -- no dot-command
-- takes a trailing comment on its own line, so these two notes live here instead.
.headers on
.mode column
INSERT INTO book_tag(book_id, tag_id) VALUES (1, 1), (1, 2);
                                    -- => two DIFFERENT pairs -- both accepted
SELECT * FROM book_tag;            -- => 2 rows -- book 1 tagged 'history' AND 'computing'

-- The SAME (book_id, tag_id) pair a second time -- this violates the composite PRIMARY KEY.
INSERT INTO book_tag(book_id, tag_id) VALUES (1, 1);
                                    -- => rejected -- (1, 1) already exists as a row
