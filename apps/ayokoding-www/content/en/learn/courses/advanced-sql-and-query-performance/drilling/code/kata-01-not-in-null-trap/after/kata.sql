-- Kata 1 (after): NOT EXISTS is immune to NULLs inside the subquery's result.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book, banned_author CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER);
CREATE TABLE banned_author(author_id INTEGER);
INSERT INTO book(id, title, author_id) VALUES
    (1, 'Refactoring', 10),
    (2, 'Domain-Driven Design', 20),
    (3, 'Working Effectively', NULL);
INSERT INTO banned_author(author_id) VALUES (20), (NULL);

-- THE FIX: NOT EXISTS correlates row-by-row and never compares against NULL directly.
SELECT id, title FROM book b
WHERE NOT EXISTS (
    SELECT 1 FROM banned_author ba WHERE ba.author_id = b.author_id
);
