-- Example 71: Anti-Join -- Missing Rows.
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
                                    -- => the LEFT side of the join -- every row here must appear
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL);
                                    -- => the RIGHT side -- deliberately missing for one author below

INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace'), (2, 'Grace Hopper'), (3, 'Alan Turing');
                                    -- => 3 authors -- only 2 will have a matching book
INSERT INTO book(id, title, author_id) VALUES
    (1, 'Notes on the Analytical Engine', 1),
    (2, 'The First Computer Bug', 2);
                                    -- => Alan Turing (id 3) intentionally has ZERO books

-- .headers on shows the "name" header row below; .mode column aligns the display --
-- both are readability preferences only, unrelated to the anti-join logic below.
.headers on
.mode column
-- LEFT JOIN keeps EVERY author row -- unmatched book columns come back NULL (co-14).
-- WHERE book.id IS NULL then isolates ONLY the authors that never matched anything (co-17).
SELECT author.name
FROM author
LEFT JOIN book ON book.author_id = author.id
WHERE book.id IS NULL;             -- => Alan Turing only -- the "missing rows" anti-join pattern
                                    -- => an INNER JOIN here would have DROPPED Alan entirely
                                    -- => "= NULL" would NOT work here -- co-17's three-valued logic
