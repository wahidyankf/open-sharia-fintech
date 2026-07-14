-- Example 74: Seed from SQL File -- seed.sql (data only, applied AFTER schema.sql, co-10).
-- This file assumes schema.sql ALREADY ran -- applying seed.sql alone, first, would fail
-- with "no such table: author".
INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace'), (2, 'Grace Hopper');
                                    -- => 2 author rows -- author_id 1 and 2 below reference these
INSERT INTO book(id, title, author_id) VALUES
    (1, 'Notes on the Analytical Engine', 1),  -- Ada's first book
    (2, 'Sketch of the Analytical Engine', 1),  -- Ada's second book
    (3, 'The First Computer Bug', 2);           -- Grace's only book
                                    -- => 3 book rows -- the count Example 74's verify checks
