-- Kata 4 (before): RANK() lets a tie inflate the row count past the intended N.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS book CASCADE;
CREATE TABLE book(id INTEGER PRIMARY KEY, author_id INTEGER NOT NULL, title TEXT NOT NULL, price NUMERIC(6,2) NOT NULL);
INSERT INTO book(id, author_id, title, price) VALUES
    (1, 1, 'Refactoring',            45.00),
    (2, 1, 'Domain-Driven Design',   40.00),
    (3, 1, 'Clean Code',             40.00),  -- ties Domain-Driven Design for 2nd place
    (4, 1, 'Working Effectively',    30.00);

-- intent: exactly the top-2 highest-priced books per author.
SELECT author_id, title, price, rnk
FROM (
    SELECT author_id, title, price,
           RANK() OVER (PARTITION BY author_id ORDER BY price DESC) AS rnk
    FROM book
) ranked
WHERE rnk <= 2
ORDER BY author_id, price DESC, title;
