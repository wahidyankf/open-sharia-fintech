-- Example 65a: the SAME knowledge-graph question, 5 normalized tables (co-03).
CREATE TABLE person (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => entity table 1 of 3 -- one row per Person node in Example 64's graph
-- => id auto-increments via INTEGER PRIMARY KEY -- the same pattern every entity table here uses
CREATE TABLE organization (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => entity table 2 of 3 -- one row per Organization node
CREATE TABLE topic (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => entity table 3 of 3 -- one row per Topic node
-- => 3 CREATE TABLE statements above, ZERO of which mention a relationship yet
CREATE TABLE works_at (
  person_id INTEGER NOT NULL,
  -- => foreign key by convention -- SQLite does not enforce it without an explicit constraint
  org_id INTEGER NOT NULL
  -- => paired with person_id -- together the row IS the WORKS_AT fact, nothing more
);

-- => junction table 1 of 2 -- models the WORKS_AT relationship as a row, not an edge
CREATE TABLE focuses_on (
  org_id INTEGER NOT NULL,
  -- => foreign key by convention, same caveat as works_at.person_id above
  topic_id INTEGER NOT NULL
  -- => paired with org_id -- together the row IS the FOCUSES_ON fact
);

-- => junction table 2 of 2 -- structurally identical to works_at, just naming a different pair
-- => TWO separate join tables, one per relationship, mirroring the two edge types in Example 64
-- => 5 tables total: 3 entity tables + 2 junction tables, versus 3 node labels + 2 edge types
INSERT INTO
  person
VALUES
  (1, 'Ada');

-- => id 1, Ada -- the anchor every JOIN chain below starts walking from
-- => nothing on this row says WHERE Ada works -- that fact lives only in works_at
-- => the one Person row
INSERT INTO
  organization
VALUES
  (1, 'Analytical Labs');

-- => id 1, Analytical Labs -- reached via works_at, one hop from Ada
-- => the one Organization row
INSERT INTO
  topic
VALUES
  (1, 'Graph Databases');

-- => id 1, Graph Databases -- reached via focuses_on, two hops from Ada
-- => the one Topic row
INSERT INTO
  works_at
VALUES
  (1, 1);

-- => (person_id 1, org_id 1) -- the fact "Ada works at Analytical Labs" lives ONLY in this row
-- => a second employer for Ada would be a SECOND row here, not a change to this one
-- => the one WORKS_AT junction row: person 1 works at org 1
INSERT INTO
  focuses_on
VALUES
  (1, 1);

-- => (org_id 1, topic_id 1) -- the fact "Analytical Labs focuses on Graph Databases" lives here
-- => a second focus topic would likewise be a SECOND row, not a change to this one
-- => the one FOCUSES_ON junction row: org 1 focuses on topic 1
-- => the query itself: person -> org -> topic, the SAME 2-hop question as Example 64
SELECT
  person.name,
  -- => hop 0: the starting person's own name
  organization.name,
  -- => hop 1: the organization reached via works_at
  topic.name
  -- => hop 2: the topic reached via focuses_on -- 3 columns, 3 DIFFERENT tables
  -- => none of the 3 projected columns come from the 2 junction tables themselves
FROM
  person
  -- => starts from the person table, the same anchor Example 64's MATCH started from
  JOIN works_at ON works_at.person_id = person.id
  -- => join 1: person's own WORKS_AT junction rows
  -- => this is where the traversal FIRST leaves the person table
  JOIN organization ON organization.id = works_at.org_id
  -- => join 2: resolves the junction row's org_id to a real organization row
  JOIN focuses_on ON focuses_on.org_id = organization.id
  -- => join 3: that organization's own FOCUSES_ON junction rows
  -- => a second junction lookup, mirroring join 1's shape one hop later
  JOIN topic ON topic.id = focuses_on.topic_id;

-- => join 4: resolves the junction row's topic_id to a real topic row
-- => 4 JOINs total for a 2-hop question -- 2 entity-lookup joins, 2 junction-table joins
-- => a 3rd hop (say, topic -> author) would add ANOTHER entity table AND junction table pair
-- => each junction table doubles the JOIN cost of its relationship -- entity lookup PLUS resolution
-- => this is the SAME "join explosion" argument as Example 19, now with mixed relationship types
