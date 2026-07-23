-- Kata 2 (before): WHERE column = NULL never matches under three-valued logic.
DROP TABLE IF EXISTS book;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, published_year INTEGER);
INSERT INTO book(title, published_year) VALUES
    ('The Mythical Man-Month', 1975),
    ('Unknown Draft', NULL),
    ('Peopleware', 1987);

.headers on
.mode column

-- intent: find every book whose published_year was never recorded.
SELECT id, title FROM book WHERE published_year = NULL;
