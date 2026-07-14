-- Kata 5 (after): PRAGMA foreign_keys=ON rejects the same orphan insert.
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS author;
-- THE FIX: turn on enforcement for this connection BEFORE any writes happen.
PRAGMA foreign_keys = ON;

CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER REFERENCES author(id));
INSERT INTO author(name) VALUES ('Ada Lovelace');

.headers on
.mode column

-- author_id 99 still does not exist -- this insert is now rejected.
INSERT INTO book(title, author_id) VALUES ('Ghost Reference', 99);

SELECT id, title, author_id FROM book;
