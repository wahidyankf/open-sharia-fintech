-- Capstone step 3 (companion to serve.py): the canonical gold-serving query.
-- serve.py runs this exact statement as GOLD_REGION_TOTALS_SQL; this file exists
-- as the plain-SQL artifact a BI tool or a reviewer could run directly against
-- the star schema built by transform.py, without going through Python at all.
CREATE OR REPLACE TABLE gold_region_totals AS
SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS line_count
FROM fact_order_line
GROUP BY region;
