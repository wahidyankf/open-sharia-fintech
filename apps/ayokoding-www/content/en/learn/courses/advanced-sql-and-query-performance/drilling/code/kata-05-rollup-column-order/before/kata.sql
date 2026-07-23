-- Kata 5 (before): ROLLUP is ORDER-sensitive -- the wrong column order produces
-- subtotals at the wrong level of the hierarchy, not the ones the report needs.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS sale CASCADE;
CREATE TABLE sale(id INTEGER PRIMARY KEY, category TEXT NOT NULL, region TEXT NOT NULL, amount NUMERIC(8,2) NOT NULL);
INSERT INTO sale(id, category, region, amount) VALUES
    (1, 'Books',      'West', 100.00),
    (2, 'Books',      'East',  50.00),
    (3, 'Games',      'West',  80.00),
    (4, 'Games',      'East',  20.00);

-- intent: total per CATEGORY (across all regions), plus a grand total.
SELECT category, region, SUM(amount) AS total
FROM sale
-- BUG: ROLLUP(region, category) rolls up in the WRONG order -- it produces a
-- subtotal per REGION (across categories), not per category as intended.
GROUP BY ROLLUP(region, category)
ORDER BY region NULLS LAST, category NULLS LAST;
