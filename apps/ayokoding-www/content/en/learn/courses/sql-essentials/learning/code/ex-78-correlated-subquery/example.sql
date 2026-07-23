-- Example 78: Correlated Subquery.
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL);
                                    -- => the OUTER table -- one output row per book
CREATE TABLE review(id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES book(id), rating INTEGER NOT NULL);
                                    -- => the table the INNER subquery counts against

INSERT INTO book(id, title) VALUES (1, 'Notes on the Analytical Engine'), (2, 'Sketch of the Analytical Engine');
                                    -- => 2 books -- 1 gets 2 reviews below, 2 gets 1 review
INSERT INTO review(id, book_id, rating) VALUES (1, 1, 5), (2, 1, 4), (3, 2, 3);
                                    -- => book 1 has 2 reviews, book 2 has 1 review

.headers on
.mode column
-- The inner SELECT re-runs ONCE PER OUTER ROW -- "r.book_id = book.id" CORRELATES it to
-- whichever book row is currently being projected (co-08). Not a join -- a per-row scalar.
SELECT title, (SELECT count(*) FROM review r WHERE r.book_id = book.id) AS review_count
FROM book;                         -- => 2 rows -- each with its OWN computed review count
