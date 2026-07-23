-- Kata 1 (before): NOT IN against a subquery containing NULL matches NOTHING.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book, banned_author CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER);
CREATE TABLE banned_author(author_id INTEGER);
INSERT INTO book(id, title, author_id) VALUES
    (1, 'Refactoring', 10),
    (2, 'Domain-Driven Design', 20),
    (3, 'Working Effectively', NULL);
-- a data-entry gap: one banned_author row was inserted with a NULL author_id
INSERT INTO banned_author(author_id) VALUES (20), (NULL);

-- intent: list every book whose author is NOT on the banned list.
SELECT id, title FROM book WHERE author_id NOT IN (SELECT author_id FROM banned_author);
