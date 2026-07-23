-- Kata 5 (before): PRAGMA foreign_keys is OFF by default -- an orphan insert succeeds silently.
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS author;
CREATE TABLE author(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, author_id INTEGER REFERENCES author(id));
INSERT INTO author(name) VALUES ('Ada Lovelace');

.headers on
.mode column

-- BUG: author_id 99 does not exist in author -- no PRAGMA foreign_keys=ON was ever set,
-- so SQLite does not enforce the REFERENCES clause for this connection.
INSERT INTO book(title, author_id) VALUES ('Ghost Reference', 99);

SELECT id, title, author_id FROM book;
