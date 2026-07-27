-- Capstone step 3 (companion to serve.py): the canonical gold-serving query.
-- serve.py runs this exact statement as GOLD_REGION_TOTALS_SQL; this file exists
-- as the plain-SQL artifact a BI tool or a reviewer could run directly against
-- the star schema built by transform.py, without going through Python at all.
CREATE OR REPLACE TABLE gold_region_totals AS  -- => co-04: GOLD -- Databricks docs: "consumption-ready, de-normalized, read-optimized"
SELECT region, SUM(amount) AS total_revenue, COUNT(*) AS line_count  -- => co-10: revenue is additive -- sums correctly across the region dimension
FROM fact_order_line  -- => co-04: reads from the star schema's fact table, built by transform.py
GROUP BY region;  -- => co-04: one served row PER region -- exactly the shape a dashboard would query directly
