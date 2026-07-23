-- Kata 5 (after): ROLLUP(category, region) rolls up in the INTENDED hierarchy --
-- a subtotal per category first, then the grand total.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS sale CASCADE;
CREATE TABLE sale(id INTEGER PRIMARY KEY, category TEXT NOT NULL, region TEXT NOT NULL, amount NUMERIC(8,2) NOT NULL);
INSERT INTO sale(id, category, region, amount) VALUES
    (1, 'Books',      'West', 100.00),
    (2, 'Books',      'East',  50.00),
    (3, 'Games',      'West',  80.00),
    (4, 'Games',      'East',  20.00);

-- THE FIX: ROLLUP(category, region) (co-08) matches the report's actual
-- hierarchy -- category is the OUTER grouping, region the inner one.
SELECT category, region, SUM(amount) AS total
FROM sale
GROUP BY ROLLUP(category, region)
ORDER BY category NULLS LAST, region NULLS LAST;
