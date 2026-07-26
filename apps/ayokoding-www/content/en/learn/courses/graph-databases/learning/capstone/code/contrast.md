# Capstone Step 4 -- The Relational Contrast

_Traces to: `load.py`'s domain, `recommend.py`'s recommendation and `run.py`'s friends-of-friends
questions._ (co-03)

The identical "people who bought X also bought Y" question `recommend.py` answers with one Cypher
pattern, against the identical fixture, written as an explicit-join relational query naming its
exact join count -- plus the identical friends-of-friends question, showing how its relational cost
grows with traversal depth.

## Schema

```sql
CREATE TABLE person (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE item (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE knows (
  person_id INTEGER NOT NULL,
  other_id INTEGER NOT NULL
);

CREATE TABLE bought (
  person_id INTEGER NOT NULL,
  item_id INTEGER NOT NULL
);
```

## Data (matching `load.py`'s fixture exactly)

```sql
INSERT INTO
  person
VALUES
  (1, 'Ada'),
  (2, 'Bob'),
  (3, 'Cid'),
  (4, 'Dee'),
  (5, 'Zoe');

INSERT INTO
  item
VALUES
  (1, 'Keyboard'),
  (2, 'Monitor'),
  (3, 'Mousepad');

INSERT INTO
  knows
VALUES
  (1, 2),
  (2, 3),
  (3, 4),
  (1, 5),
  (1, 3);

INSERT INTO
  bought
VALUES
  (1, 1),
  (2, 1),
  (2, 3),
  (3, 2);
```

## The recommendation question, relationally

```sql
SELECT
  rec.name
FROM
  person u
  JOIN bought b1 ON b1.person_id = u.id -- join 1: u's own purchases
  JOIN bought b2 ON b2.item_id = b1.item_id -- join 2: co-buyers of the same item
  JOIN person other ON other.id = b2.person_id
  AND other.id <> u.id -- join 3: the OTHER buyer
  JOIN bought b3 ON b3.person_id = other.id -- join 4: that other buyer's purchases
  JOIN item rec ON rec.id = b3.item_id -- join 5: resolve item id to name
WHERE
  u.name = 'Ada'
  AND NOT EXISTS (
    SELECT
      1
    FROM
      bought b4
    WHERE
      b4.person_id = u.id
      AND b4.item_id = rec.id
  );

-- the exclusion filter, matching Cypher's WHERE NOT (u)-[:BOUGHT]->(rec)
```

**5 explicit JOINs plus a correlated `NOT EXISTS` subquery**, for the same question `recommend.py`
answers with one `MATCH ... WHERE NOT (u)-[:BOUGHT]->(rec)` pattern. Result: `Mousepad` -- identical
to `recommend.py`'s own output.

## The friends-of-friends question, relationally

`run.py`'s `MATCH (a:Person {name: $name})-[:KNOWS*1..2]-(b:Person)` bounds a traversal to at most 2
hops in ONE pattern, regardless of how many hops deep the bound goes. The relational equivalent
needs one additional self-join of the `knows`/`person` tables per additional hop of depth:

```sql
-- 1 hop:
SELECT DISTINCT
  p2.name
FROM
  person p1
  JOIN knows k1 ON k1.person_id = p1.id
  JOIN person p2 ON p2.id = k1.other_id
WHERE
  p1.name = 'Ada';

-- 2 hops -- ONE MORE self-join pair than the 1-hop query above. On its own this query returns only
-- nodes reached at EXACTLY 2 hops, not the full "1 or 2 hops" set `*1..2` returns:
SELECT DISTINCT
  p3.name
FROM
  person p1
  JOIN knows k1 ON k1.person_id = p1.id
  JOIN person p2 ON p2.id = k1.other_id
  JOIN knows k2 ON k2.person_id = p2.id
  JOIN person p3 ON p3.id = k2.other_id
WHERE
  p1.name = 'Ada';
```

Bounding at 3 hops instead of 2 would add a THIRD self-join pair to the relational query; Cypher's
own bound only changes one number (`*1..3` instead of `*1..2`) inside the exact same single pattern.

Matching `*1..2`'s own "1 or 2 hops" semantics exactly needs one more relational tool the Cypher
pattern never needs: a `UNION` of the 1-hop and 2-hop queries above, because the 2-hop query alone
only returns nodes reached at exactly 2 hops:

```sql
-- 1..2 hops -- UNION of the two queries above, matching *1..2's "1 or 2 hops" semantics exactly:
SELECT DISTINCT
  p2.name
FROM
  person p1
  JOIN knows k1 ON k1.person_id = p1.id
  JOIN person p2 ON p2.id = k1.other_id
WHERE
  p1.name = 'Ada'
UNION
SELECT DISTINCT
  p3.name
FROM
  person p1
  JOIN knows k1 ON k1.person_id = p1.id
  JOIN person p2 ON p2.id = k1.other_id
  JOIN knows k2 ON k2.person_id = p2.id
  JOIN person p3 ON p3.id = k2.other_id
WHERE
  p1.name = 'Ada';
```

## Why the graph wins here (co-03)

Every additional hop of depth in the relational form costs one more explicit self-join -- the query
text itself grows with the traversal depth being asked for. The Cypher form's `*1..2` (and, for the
capstone's own shortest-path step, `shortestPath()`'s unbounded `*`) keeps the SAME query text
regardless of how deep the bound goes; only the bound number changes, or nothing changes at all.
This is co-03's argument made concrete against this capstone's own fixture, not an abstract claim:
5 joins plus a correlated subquery for one recommendation question, and a self-join pair per
additional hop for the friends-of-friends question, against one unchanging Cypher pattern shape
each.
