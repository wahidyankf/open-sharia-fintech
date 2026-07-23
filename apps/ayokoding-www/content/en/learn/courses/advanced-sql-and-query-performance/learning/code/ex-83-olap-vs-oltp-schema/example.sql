-- Example 83: OLTP-Normalized vs OLAP Star Schema.
-- OLTP schemas (co-28) normalize EVEN dimension hierarchies (category, region) into
-- their own tables to eliminate redundancy for cheap transactional updates. OLAP
-- star schemas deliberately DENORMALIZE those hierarchies into wide dimension
-- tables, trading redundancy for fewer joins on analytical aggregate queries.
SET client_min_messages TO WARNING;
-- Both schema variants (OLTP tables AND the OLAP star schema tables) are
-- dropped together up front, so this example is safely re-runnable end to end.
DROP TABLE IF EXISTS sale_transaction, product, category, customer, region,
    fact_sale, dim_product, dim_customer CASCADE;
                                    -- => resets state -- this example is fully self-contained

-- OLTP-NORMALIZED: category and region are SEPARATE tables -- a "total by
-- category and region" report needs to join FOUR tables together.
-- Every FK below enforces referential integrity -- a classic OLTP design goal
-- that keeps updates to a category or region name a SINGLE-row change.
CREATE TABLE category(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE region(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE product(id INTEGER PRIMARY KEY, name TEXT NOT NULL, category_id INTEGER NOT NULL REFERENCES category(id));
CREATE TABLE customer(id INTEGER PRIMARY KEY, name TEXT NOT NULL, region_id INTEGER NOT NULL REFERENCES region(id));
CREATE TABLE sale_transaction(id INTEGER PRIMARY KEY, product_id INTEGER NOT NULL REFERENCES product(id),
    customer_id INTEGER NOT NULL REFERENCES customer(id), quantity INTEGER NOT NULL, unit_price NUMERIC(10,2) NOT NULL);

-- Two categories, two regions -- deliberately small dimension tables, since
-- the interesting scale lives in the 200,000-row fact/transaction table below.
INSERT INTO category(id, name) VALUES (1, 'Electronics'), (2, 'Books');
INSERT INTO region(id, name) VALUES (1, 'West'), (2, 'East');
INSERT INTO product(id, name, category_id) SELECT n, 'Product ' || n, 1 + (n % 2) FROM generate_series(1, 100) AS n;
INSERT INTO customer(id, name, region_id) SELECT n, 'Customer ' || n, 1 + (n % 2) FROM generate_series(1, 500) AS n;
INSERT INTO sale_transaction(id, product_id, customer_id, quantity, unit_price)
SELECT n, 1 + FLOOR(RANDOM() * 100)::INTEGER, 1 + FLOOR(RANDOM() * 500)::INTEGER,
    1 + (n % 5), (10 + (n % 90))::NUMERIC
FROM generate_series(1, 200000) AS n;
                                    -- => RANDOM() assignment (not n%100/n%500) avoids an unintended
                                    -- => parity correlation between product_id and customer_id
-- ANALYZE runs on ALL FIVE OLTP tables together -- the revenue query below
-- joins across all of them, so the planner needs fresh statistics on each.
ANALYZE category; ANALYZE region; ANALYZE product; ANALYZE customer; ANALYZE sale_transaction;

-- OLAP STAR SCHEMA: category and region names are DENORMALIZED directly onto
-- the dimension tables themselves -- the SAME report needs to join only TWO.
-- dim_product and dim_customer are the STAR SCHEMA's dimension tables --
-- fact_sale is the FACT table, holding only foreign keys and measures
-- (quantity, unit_price), the classic OLAP star-schema shape.
CREATE TABLE dim_product(product_key INTEGER PRIMARY KEY, name TEXT NOT NULL, category_name TEXT NOT NULL);
CREATE TABLE dim_customer(customer_key INTEGER PRIMARY KEY, name TEXT NOT NULL, region_name TEXT NOT NULL);
-- fact_sale holds no NAME columns at all -- pure keys and measures, the
-- defining shape of an OLAP fact table.
CREATE TABLE fact_sale(sale_id INTEGER PRIMARY KEY, product_key INTEGER NOT NULL, customer_key INTEGER NOT NULL,
    quantity INTEGER NOT NULL, unit_price NUMERIC(10,2) NOT NULL);

-- A correlated scalar subquery does the ONE-TIME flattening work here -- in a
-- real OLAP pipeline this would be an ETL/ELT job, not an ad-hoc query.
INSERT INTO dim_product(product_key, name, category_name)
SELECT id, name, (SELECT name FROM category WHERE id = product.category_id) FROM product;
INSERT INTO dim_customer(customer_key, name, region_name)
SELECT id, name, (SELECT name FROM region WHERE id = customer.region_id) FROM customer;
-- fact_sale is a straight copy of sale_transaction's columns -- only the
-- SCHEMA shape around it differs, not the underlying transactional data.
INSERT INTO fact_sale SELECT id, product_id, customer_id, quantity, unit_price FROM sale_transaction;
-- All three star-schema tables analyzed once seeded, matching the same
-- pattern used for the OLTP tables above.
ANALYZE dim_product; ANALYZE dim_customer; ANALYZE fact_sale;

-- \timing on turns on psql's built-in wall-clock timer, so the join-count
-- difference below translates into a real, measurable time comparison.
\timing on
-- The SAME analytical question, "total revenue by category and region":
-- OLTP-normalized version -- FOUR tables joined together.
-- Every join here walks a FK relationship -- product -> category, customer ->
-- region -- exactly the hierarchy OLTP normalization keeps as separate tables.
SELECT c.name AS category, r.name AS region, SUM(t.quantity * t.unit_price) AS revenue
FROM sale_transaction t
JOIN product p ON p.id = t.product_id
JOIN category c ON c.id = p.category_id
JOIN customer cu ON cu.id = t.customer_id
JOIN region r ON r.id = cu.region_id
GROUP BY c.name, r.name ORDER BY c.name, r.name;

-- OLAP star schema version -- only TWO tables joined -- category/region are
-- ALREADY flattened onto the dimension tables (co-28).
-- Both queries compute the IDENTICAL aggregate result -- only the number of
-- JOINs the planner must execute differs between the two schema designs.
SELECT dp.category_name AS category, dc.region_name AS region, SUM(f.quantity * f.unit_price) AS revenue
FROM fact_sale f
JOIN dim_product dp ON dp.product_key = f.product_key
JOIN dim_customer dc ON dc.customer_key = f.customer_key
GROUP BY dp.category_name, dc.region_name ORDER BY category, region;
\timing off
-- This trade-off mirrors Example 74's denormalization measurement -- OLAP
-- schemas accept write-side redundancy in exchange for read-side simplicity,
-- at a scale where analytical queries vastly outnumber transactional writes.
