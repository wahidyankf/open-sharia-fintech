-- Example 74: Denormalization, Measured.
-- Denormalizing (co-27) a hot read path -- copying a customer's name directly onto
-- every order row instead of joining to look it up -- trades write cost (updating
-- that name means touching MANY rows, not one) for read speed (no JOIN at all).
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS order_normalized, order_denormalized, customer_ref CASCADE;
                                    -- => resets state -- this example is fully self-contained

-- NORMALIZED: customer name lives in ONE place, orders reference it by id.
-- customer_ref is shared by BOTH the normalized and denormalized order tables
-- below -- it exists so the UPDATE comparison later has a fair, single source
-- of truth to rename from.
CREATE TABLE customer_ref(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE order_normalized(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customer_ref(id), amount NUMERIC(10,2) NOT NULL);
INSERT INTO customer_ref(id, name) SELECT n, 'Customer ' || n FROM generate_series(1, 1000) AS n;
INSERT INTO order_normalized(id, customer_id, amount)
SELECT n, 1 + (n % 1000), (10 + (n % 90))::NUMERIC FROM generate_series(1, 200000) AS n;
                                    -- => 200,000 orders across 1,000 customers -- ~200 orders each

-- DENORMALIZED: customer_name is COPIED directly onto every order row (co-27) --
-- redundant, but a read never has to JOIN to display it.
-- The FOREIGN KEY to customer_ref is KEPT even in the denormalized table --
-- denormalization duplicates data for READ speed, it does not have to abandon
-- referential integrity.
CREATE TABLE order_denormalized(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL REFERENCES customer_ref(id), customer_name TEXT NOT NULL, amount NUMERIC(10,2) NOT NULL);
INSERT INTO order_denormalized(id, customer_id, customer_name, amount)
SELECT o.id, o.customer_id, c.name, o.amount
FROM order_normalized o JOIN customer_ref c ON c.id = o.customer_id;
-- This index is what keeps the WRITE-side UPDATE below (WHERE customer_id =
-- 500) fast -- without it, finding "every order for customer 500" would
-- require a full table scan of all 200,000 rows.
CREATE INDEX idx_order_denormalized_customer_id ON order_denormalized(customer_id);
ANALYZE customer_ref;
ANALYZE order_normalized;
ANALYZE order_denormalized;

\timing on
-- READ: "list recent orders with the customer's name" -- normalized needs a JOIN.
SELECT o.id, c.name, o.amount FROM order_normalized o JOIN customer_ref c ON c.id = o.customer_id
    WHERE o.id BETWEEN 100000 AND 100100;
-- READ: the SAME logical result, denormalized -- no JOIN at all.
SELECT id, customer_name, amount FROM order_denormalized WHERE id BETWEEN 100000 AND 100100;

-- WRITE: "Customer 500 changes their display name" -- the REAL cost of
-- denormalization shows up here, not on insert.
-- Normalized: the name lives in exactly ONE row -- one UPDATE, one row touched.
UPDATE customer_ref SET name = 'Customer 500 (Renamed)' WHERE id = 500;
-- Denormalized: the SAME name is duplicated onto EVERY order that customer placed
-- -- the UPDATE must find and rewrite ALL of them to stay consistent (co-27).
UPDATE order_denormalized SET customer_name = 'Customer 500 (Renamed)' WHERE customer_id = 500;
\timing off

-- This COUNT quantifies the exact write-amplification cost: however many rows
-- print here is how many extra rows the denormalized UPDATE had to rewrite
-- compared to the normalized version's single-row UPDATE above.
SELECT COUNT(*) AS rows_touched_by_denormalized_update FROM order_denormalized WHERE customer_id = 500;
