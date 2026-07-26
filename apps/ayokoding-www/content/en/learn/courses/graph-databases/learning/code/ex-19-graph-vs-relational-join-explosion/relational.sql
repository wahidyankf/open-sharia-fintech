-- Example 19a: 3-hop "friends of friends of friends" via relational self-joins.
CREATE TABLE person (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

-- => one row per person, nothing about relationships lives here
CREATE TABLE knows (a_id INTEGER NOT NULL, b_id INTEGER NOT NULL);

-- => a plain edge-list table -- the relational equivalent of a KNOWS relationship
-- => a_id and b_id are plain INTEGERs -- SQLite enforces no foreign-key link unless declared
INSERT INTO
  person
VALUES
  (1, 'Ada'),
  -- => id 1, Ada -- the WHERE clause at the bottom anchors the whole traversal here
  -- => also becomes alias p1, the leftmost person in every JOIN chain below
  (2, 'Bob'),
  -- => id 2, Bob -- resolved via alias p2 at hop 1
  (3, 'Cid'),
  -- => id 3, Cid -- resolved via alias p3 at hop 2
  (4, 'Dee');

-- => id 4, Dee -- resolved via alias p4 at hop 3, the row the query below returns
-- => 4 people, ids 1-4
INSERT INTO
  knows
VALUES
  (1, 2),
  -- => Ada KNOWS Bob -- hop 1, matched below by JOIN knows k1
  -- => this row alone is what the k1.a_id = p1.id JOIN condition matches against
  (2, 3),
  -- => Bob KNOWS Cid -- hop 2, matched below by JOIN knows k2
  (3, 4);

-- => Cid KNOWS Dee -- hop 3, matched below by JOIN knows k3
-- => 3 edges for 3 hops -- one row per hop, mirroring the one JOIN-pair per hop below
-- => a straight chain: Ada->Bob->Cid->Dee, exactly 3 hops deep
-- => 3 hops needs 3 self-joins on the SAME edge table -- one more JOIN per additional hop
SELECT
  p4.name
  -- => the final person 3 hops away, resolved through 4 aliased copies of person below
  -- => only ONE column is projected -- everything else below is join plumbing to reach it
FROM
  person p1
  -- => p1 is the STARTING person -- filtered to Ada by the WHERE clause at the bottom
  JOIN knows k1 ON k1.a_id = p1.id
  -- => hop 1: p1's outgoing edge
  JOIN person p2 ON p2.id = k1.b_id
  -- => hop 1's destination person
  JOIN knows k2 ON k2.a_id = p2.id
  -- => hop 2: p2's outgoing edge
  JOIN person p3 ON p3.id = k2.b_id
  -- => hop 2's destination person
  JOIN knows k3 ON k3.a_id = p3.id
  -- => hop 3: p3's outgoing edge
  JOIN person p4 ON p4.id = k3.b_id
  -- => hop 3's destination person -- THIS is what a 4th hop would need 2 more of these joins for
WHERE
  p1.name = 'Ada';

-- => the ONLY filter in the entire query -- every JOIN above it is pure traversal plumbing
-- => swap 'Ada' for any other person and the SAME 6-JOIN shape still applies
-- => 6 total JOINs for 3 hops (3 knows-joins + 3 person-joins)
-- => a 4th hop would need 2 MORE joins (one knows, one person) added to this query's text
