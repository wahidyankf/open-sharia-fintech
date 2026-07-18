-- Kata 3 (before): the default RANGE frame double-counts tied peer rows.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS sale CASCADE;
CREATE TABLE sale(id INTEGER PRIMARY KEY, amount NUMERIC(8,2) NOT NULL);
INSERT INTO sale(id, amount) VALUES
    (1, 10.00),
    (2, 20.00),
    (3, 20.00),   -- => TIES with row 2
    (4, 30.00);

-- intent: a strict row-by-row running total -- each row contributes ONCE.
SELECT id, amount,
       SUM(amount) OVER (ORDER BY amount) AS running_total
       -- BUG: no explicit frame -- the DEFAULT is RANGE UNBOUNDED PRECEDING,
       -- which sums every TIED peer together, not one physical row at a time.
FROM sale
ORDER BY amount, id;
