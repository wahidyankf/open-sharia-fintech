-- Capstone: seed.sql -- applied AFTER schema.sql, exactly like Example 74's split (co-10, co-24).
INSERT INTO author(id, name) VALUES (1, 'Ada Lovelace'), (2, 'Grace Hopper');
INSERT INTO publisher(id, name) VALUES (1, 'Analytical Press');
INSERT INTO book(id, title, author_id, publisher_id, price) VALUES
    (1, 'Notes on the Analytical Engine', 1, 1, 12.5),
    (2, 'Sketch of the Analytical Engine', 1, 1, 9.0),
    (3, 'The First Computer Bug', 2, NULL, 15.0);
                                    -- => book 3 has NO publisher -- proves publisher_id's optionality
INSERT INTO tag(id, name) VALUES (1, 'history'), (2, 'computing');
INSERT INTO book_tag(book_id, tag_id) VALUES (1, 1), (1, 2), (2, 2);
