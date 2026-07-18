-- Kata 6 (before): an ELSE 0 inside COUNT(CASE...) makes COUNT count EVERY row.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS invoice CASCADE;
CREATE TABLE invoice(id INTEGER PRIMARY KEY, status TEXT NOT NULL, amount NUMERIC(8,2) NOT NULL);
INSERT INTO invoice(id, status, amount) VALUES
    (1, 'paid',    100.00),
    (2, 'paid',    200.00),
    (3, 'pending',  50.00),
    (4, 'pending',  75.00),
    (5, 'pending',  20.00);

-- intent: count only the PAID invoices (expected: 2).
SELECT
    COUNT(CASE WHEN status = 'paid' THEN 1 ELSE 0 END) AS paid_count
    -- BUG: COUNT() counts every NON-NULL value it's handed -- ELSE 0 hands it
    -- a non-NULL 0 for every pending row too, so COUNT counts ALL 5 rows.
FROM invoice;
