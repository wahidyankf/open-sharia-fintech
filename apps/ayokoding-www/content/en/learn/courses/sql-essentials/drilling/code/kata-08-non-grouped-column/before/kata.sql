-- Kata 8 (before): title is neither aggregated nor in GROUP BY -- SQLite leniently
-- picks ONE arbitrary row's title per group instead of raising an error.
DROP TABLE IF EXISTS book;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL, price REAL NOT NULL);
INSERT INTO book(title, author_id, price) VALUES
    ('Notes on the Analytical Engine', 1, 12.00),
    ('Sketch of the Analytical Engine', 1, 18.00),
    ('COBOL Manual', 2, 9.50);

.headers on
.mode column

-- BUG: title is a non-aggregated, non-grouping column -- which title does author_id
-- 1's group report back, when it has TWO distinct titles?
SELECT author_id, title, count(*) AS book_count, sum(price) AS total_price
FROM book
GROUP BY author_id;
