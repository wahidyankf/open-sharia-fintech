-- Kata 2 (after): IS NULL is the correct test for "unknown", not =.
DROP TABLE IF EXISTS book;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, published_year INTEGER);
INSERT INTO book(title, published_year) VALUES
    ('The Mythical Man-Month', 1975),
    ('Unknown Draft', NULL),
    ('Peopleware', 1987);

.headers on
.mode column

-- THE FIX: IS NULL, not = NULL, matches rows whose value is unknown.
SELECT id, title FROM book WHERE published_year IS NULL;
