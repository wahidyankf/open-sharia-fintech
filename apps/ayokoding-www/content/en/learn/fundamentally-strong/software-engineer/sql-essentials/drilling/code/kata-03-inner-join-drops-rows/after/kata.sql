-- Kata 3 (after): LEFT JOIN keeps every author, filling unmatched book columns with NULL.
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS author;
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER REFERENCES author(id));
INSERT INTO author(name) VALUES
    ('Ada Lovelace'),
    ('Grace Hopper'),
    ('Margaret Hamilton');
INSERT INTO book(title, author_id) VALUES ('Notes on the Analytical Engine', 1);

.headers on
.mode column
.nullvalue NULL

-- THE FIX: LEFT JOIN keeps every left-side (author) row, even with zero matches.
SELECT author.name, book.title
FROM author
LEFT JOIN book ON book.author_id = author.id
ORDER BY author.name;
