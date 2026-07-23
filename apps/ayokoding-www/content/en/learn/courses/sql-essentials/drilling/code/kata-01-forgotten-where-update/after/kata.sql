-- Kata 1 (after): the WHERE clause narrows the UPDATE to the one intended row.
DROP TABLE IF EXISTS book;
CREATE TABLE book(id INTEGER PRIMARY KEY, title TEXT NOT NULL, price REAL NOT NULL);
INSERT INTO book(title, price) VALUES
    ('Refactoring', 45.00),
    ('Domain-Driven Design', 55.00),
    ('Clean Code', 35.00);

.headers on
.mode column

-- THE FIX: WHERE id = 2 scopes the write to exactly the row the promo applies to.
UPDATE book SET price = 0 WHERE id = 2;

SELECT id, title, price FROM book ORDER BY id;
