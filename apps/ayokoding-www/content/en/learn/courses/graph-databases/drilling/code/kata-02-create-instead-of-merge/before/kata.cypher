// Kata 2 (before): CREATE writes unconditionally -- a retried run duplicates every row.
UNWIND ['Ada', 'Grace'] AS name
CREATE (:Person {name: name});
// => first run: 2 new Person nodes

// simulate a RETRY of the exact same load script after, say, a network blip --
// this is the SAME statement, run a second time within this one file.
UNWIND ['Ada', 'Grace'] AS name
CREATE (:Person {name: name});
// BUG: CREATE has no concept of "this row is already loaded" -- it writes again regardless

MATCH (p:Person)
RETURN count(p) AS person_count;
