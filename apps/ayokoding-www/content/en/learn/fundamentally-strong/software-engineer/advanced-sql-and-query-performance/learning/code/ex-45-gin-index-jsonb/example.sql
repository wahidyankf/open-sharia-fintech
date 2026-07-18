-- Example 45: GIN Index on jsonb.
-- GIN (co-20, Generalized Inverted Index) indexes the INDIVIDUAL elements inside a
-- composite value -- for jsonb, that means every key and value becomes independently
-- searchable, which the @> containment operator below relies on.
SET client_min_messages TO WARNING;
DROP TABLE IF EXISTS product CASCADE;
                                    -- => resets state -- this example is fully self-contained
-- A single JSONB column stores a flexible, semi-structured attribute bag --
-- the kind of schema-optional data GIN indexes are specifically built to search.
CREATE TABLE product(id INTEGER PRIMARY KEY, attributes JSONB NOT NULL);
                                    -- => attributes: a flexible per-product bag of key/value pairs
INSERT INTO product(id, attributes)
SELECT
    n,
    jsonb_build_object(
        'color', (ARRAY['red', 'blue', 'green'])[1 + (n % 3)],
        'size',  (ARRAY['S', 'M', 'L'])[1 + (n % 3)]
    )
FROM generate_series(1, 100000) AS n;
                                    -- => 100,000 products, each with a color and size attribute

-- CREATE INDEX ... USING gin (co-20) indexes every key/value pair INSIDE each jsonb
-- document, enabling the @> "contains" operator to use the index efficiently.
-- Unlike a B-tree, which stores ONE entry per row, a GIN index stores one entry
-- PER KEY inside the jsonb document -- a product with 5 attributes contributes
-- 5 separate index entries, not 1.
CREATE INDEX idx_product_attributes_gin ON product USING gin (attributes);
ANALYZE product;

-- @> (co-20) tests whether the LEFT jsonb value CONTAINS the RIGHT one -- here,
-- "does this product's attributes include color: red?"
EXPLAIN SELECT id FROM product WHERE attributes @> '{"color": "red"}'::jsonb;
                                    -- => Bitmap Heap Scan + Bitmap Index Scan on idx_product_attributes_gin
                                    -- => the GIN index serves the containment predicate directly
