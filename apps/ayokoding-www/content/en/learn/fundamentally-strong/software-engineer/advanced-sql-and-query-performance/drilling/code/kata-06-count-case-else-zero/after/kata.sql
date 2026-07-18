-- Kata 6 (after): dropping ELSE lets non-matching rows stay NULL, so COUNT
-- correctly skips them; SUM(CASE...) is the correct pattern when a 0 is needed.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS invoice CASCADE;
CREATE TABLE invoice(id INTEGER PRIMARY KEY, status TEXT NOT NULL, amount NUMERIC(8,2) NOT NULL);
INSERT INTO invoice(id, status, amount) VALUES
    (1, 'paid',    100.00),
    (2, 'paid',    200.00),
    (3, 'pending',  50.00),
    (4, 'pending',  75.00),
    (5, 'pending',  20.00);

-- THE FIX: no ELSE -- a non-matching row's CASE evaluates to NULL, and COUNT()
-- (co-10) skips NULLs, so only the 2 genuinely 'paid' rows are counted.
SELECT
    COUNT(CASE WHEN status = 'paid' THEN 1 END) AS paid_count,
    SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END) AS paid_total
    -- SUM legitimately needs the ELSE 0 -- it is folding a running total, not
    -- counting rows, and 0 is the correct additive identity for a non-match.
FROM invoice;
