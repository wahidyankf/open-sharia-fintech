-- Example 71: Preview: the Relational Contrast. (co-03)
-- The SAME "people who bought X also bought Y" question as Example 70, relationally.
-- => 3 tables total: 2 entity tables (app_user, item) + 1 junction table (bought)
CREATE TABLE app_user (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => entity table 1 of 2 -- one row per User node from Example 70
-- => id auto-increments via INTEGER PRIMARY KEY -- same pattern as every entity table in this course
CREATE TABLE item (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => entity table 2 of 2 -- one row per Item node
CREATE TABLE bought (
  user_id INTEGER NOT NULL,
  -- => foreign key by convention -- SQLite does not enforce it without an explicit constraint
  item_id INTEGER NOT NULL
  -- => paired with user_id -- together the row IS the BOUGHT fact, nothing more
);

-- => the single junction table modeling the BOUGHT relationship as a row, not an edge
-- => 3 tables, 1 junction -- structurally identical to Example 33's student/course/enrollment shape
INSERT INTO
  app_user
VALUES
  (1, 'Ada'),
  -- => id 1, Ada -- the WHERE clause below anchors the whole query at this one user
  (2, 'Bob');

-- => id 2, Bob -- Ada's ONLY co-buyer, resolved via the "other" alias below
-- => both people from Example 70's seed
INSERT INTO
  item
VALUES
  (1, 'Keyboard'),
  -- => id 1, Keyboard -- the shared item that makes Ada and Bob co-buyers
  (2, 'Mousepad');

-- => id 2, Mousepad -- the recommendation the query below must surface
-- => both items from Example 70's seed
INSERT INTO
  bought
VALUES
  (1, 1),
  -- => Ada bought Keyboard -- matched by JOIN bought b1 as u's own purchase
  (2, 1),
  -- => Bob bought Keyboard too -- this shared row is what makes b2 find Bob as a co-buyer
  (2, 2);

-- => Bob ALSO bought Mousepad -- this is the row b3/rec ultimately surfaces as the recommendation
-- => 3 rows total, 2 buyers -- the SAME shape as Example 70's own driver seed
-- => identical fixture to Example 70's driver seed: Ada+Bob share Keyboard, Bob also has Mousepad
-- => the query itself: same "co-buyers' other purchases" question as Example 70's MATCH
SELECT
  rec.name
  -- => the ONLY projected column -- the recommended item's name, resolved via alias rec
FROM
  app_user u
  -- => starts from the app_user table, the same anchor Example 70's MATCH started from
  JOIN bought b1 ON b1.user_id = u.id -- join 1: u's own purchases
  -- => u.id is still unbound here -- WHERE below is what pins it to Ada
  JOIN bought b2 ON b2.item_id = b1.item_id -- join 2: co-buyers of the same item
  -- => b2 walks from an item BACK to every purchase row of that same item, including u's own
  -- => without join 3 below, this alone would report u as their own co-buyer too
  JOIN app_user other ON other.id = b2.user_id
  -- => resolves b2's user_id back to a real app_user row, aliased "other"
  AND other.id <> u.id -- join 3: the OTHER buyer
  -- => excludes u themselves -- without this, "other" would include u as their own co-buyer
  JOIN bought b3 ON b3.user_id = other.id -- join 4: that other buyer's purchases
  -- => walks from the co-buyer to EVERYTHING they ever bought, not just the shared item
  JOIN item rec ON rec.id = b3.item_id -- join 5: resolve item id to name
  -- => the final hop -- rec.name is the ONLY column this whole query ultimately returns
  -- => 5 JOINs to reach a name that is 4 relationship-hops away from the starting user
WHERE
  u.name = 'Ada'
  -- => filters down to the single starting user, matching Example 70's $name parameter
  -- => this is the ONLY place 'Ada' appears -- everything above it runs for every user until here
  AND NOT EXISTS (
    -- => the correlated subquery: does u ALREADY own rec? -- Cypher's WHERE NOT, spelled out
    -- => "correlated" means it re-runs once PER candidate row, referencing u and rec from outside it
    SELECT
      1
      -- => the literal value 1 -- NOT EXISTS only cares whether a row exists, never its content
      -- => could equally be SELECT * -- the projected value is discarded either way
    FROM
      bought b4
      -- => a FRESH alias -- b4 is unrelated to b1/b2/b3 above, scoped only to this subquery
      -- => reads the SAME bought table as the outer query, just with a different filter purpose
    WHERE
      b4.user_id = u.id
      -- => same u as the outer query -- this is what makes the subquery correlated, not independent
      AND b4.item_id = rec.id
      -- => same rec as the outer query -- true only if u already bought THIS specific candidate item
  );

-- => Mousepad passes: Ada never bought it. Keyboard would fail this NOT EXISTS check
-- => the exclusion filter, matching Cypher's WHERE NOT (u)-[:BOUGHT]->(rec)
-- => 5 explicit JOINs (plus a correlated subquery) for the SAME 4-hop pattern Example 70 expressed
-- as one MATCH -- this is the "exact join count and query text" the capstone's contrast documents
-- => a 6th recommendation source would mean a 6th JOIN, hand-written, not a bigger traversal bound
-- => output: "Mousepad" -- the one item Bob owns that Ada does not, surfaced through 5 JOINs
