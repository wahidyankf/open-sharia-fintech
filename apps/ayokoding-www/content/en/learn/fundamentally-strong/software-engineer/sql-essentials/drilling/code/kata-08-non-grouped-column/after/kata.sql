-- Kata 8 (after): group_concat aggregates every title per group explicitly.
DROP TABLE IF EXISTS book;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER NOT NULL, price REAL NOT NULL);
INSERT INTO book(title, author_id, price) VALUES
    ('Notes on the Analytical Engine', 1, 12.00),
    ('Sketch of the Analytical Engine', 1, 18.00),
    ('COBOL Manual', 2, 9.50);

.headers on
.mode column
.width 10 70 12 12

-- THE FIX: group_concat(title, sep) is a real aggregate -- it names EVERY title
-- in the group explicitly, instead of silently picking one.
SELECT author_id, group_concat(title, '; ') AS titles, count(*) AS book_count, sum(price) AS total_price
FROM book
GROUP BY author_id;
