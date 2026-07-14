-- Kata 1 (before): UPDATE with no WHERE zeroes every row, not just the intended one.
DROP TABLE IF EXISTS book;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
INSERT INTO book(title, price) VALUES
    ('Refactoring', 45.00),
    ('Domain-Driven Design', 55.00),
    ('Clean Code', 35.00);

.headers on
.mode column

-- intent: put ONE book (id 2) on a free promo -- the WHERE clause is missing.
UPDATE book SET price = 0;

SELECT id, title, price FROM book ORDER BY id;
