-- Kata 3 (after): an explicit ROWS frame counts each physical row exactly once.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS sale CASCADE;
CREATE TABLE sale(id INTEGER PRIMARY KEY, amount NUMERIC(8,2) NOT NULL);
INSERT INTO sale(id, amount) VALUES
    (1, 10.00),
    (2, 20.00),
    (3, 20.00),
    (4, 30.00);

-- THE FIX: ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW walks physical
-- rows one at a time, regardless of ties in the ORDER BY column.
SELECT id, amount,
       SUM(amount) OVER (
           ORDER BY amount, id
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ) AS running_total
FROM sale
ORDER BY amount, id;
