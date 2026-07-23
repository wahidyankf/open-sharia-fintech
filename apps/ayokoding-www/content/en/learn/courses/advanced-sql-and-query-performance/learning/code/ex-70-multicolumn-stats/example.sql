-- Example 70: Multicolumn Statistics.
-- The planner ASSUMES columns are statistically independent by default -- for
-- correlated columns (co-25) like city and country, that assumption multiplies
-- selectivities together and badly underestimates. CREATE STATISTICS fixes it.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS customer_location CASCADE;
                                    -- => resets state -- this example is fully self-contained
CREATE TABLE customer_location(id INTEGER PRIMARY KEY, city TEXT NOT NULL, country TEXT NOT NULL);
INSERT INTO customer_location(id, city, country)
SELECT n,
    CASE WHEN n % 10 = 0 THEN 'Paris' ELSE 'Jakarta' END,
    CASE WHEN n % 10 = 0 THEN 'France' ELSE 'Indonesia' END
                                    -- => city and country are PERFECTLY CORRELATED here -- every
                                    -- => 'Paris' row is ALSO 'France', every 'Jakarta' row is 'Indonesia'
FROM generate_series(1, 100000) AS n;
ANALYZE customer_location;

-- BEFORE CREATE STATISTICS: the planner treats city and country as INDEPENDENT --
-- it multiplies their individual selectivities (10% * 10% = 1%) instead of using
-- the TRUE combined selectivity (10%, since they always travel together).
EXPLAIN SELECT * FROM customer_location WHERE city = 'Paris' AND country = 'France';
                                    -- => rows=991 estimated by DEFAULT independence assumption
                                    -- => (100,000 * 10% * 10% = ~1,000) -- the TRUE count is ~10,000

-- THE FIX (co-25): tell the planner these two columns are functionally dependent.
CREATE STATISTICS customer_location_city_country_stats (dependencies)
    ON city, country FROM customer_location;
ANALYZE customer_location;
                                    -- => a SECOND ANALYZE is required -- extended statistics are
                                    -- => only computed the NEXT time ANALYZE runs, not retroactively

EXPLAIN SELECT * FROM customer_location WHERE city = 'Paris' AND country = 'France';
                                    -- => rows=10083 estimated -- now matches the TRUE count closely,
                                    -- => because the dependency statistics corrected the multiplication
