-- Kata 3 (before): an inner join silently drops authors with zero books.
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS author;
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER REFERENCES author(id));
INSERT INTO author(name) VALUES
    ('Ada Lovelace'),
    ('Grace Hopper'),
    ('Margaret Hamilton');
-- Grace Hopper (id 2) and Margaret Hamilton (id 3) have zero books each so far.
INSERT INTO book(title, author_id) VALUES ('Notes on the Analytical Engine', 1);

.headers on
.mode column

-- intent: list every author in the catalog, alongside any books they've published.
SELECT author.name, book.title
FROM author
JOIN book ON book.author_id = author.id
ORDER BY author.name;
