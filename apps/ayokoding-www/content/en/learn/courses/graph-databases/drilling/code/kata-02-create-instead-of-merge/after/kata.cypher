// Kata 2 (after): MERGE is idempotent -- a retried run leaves the roster unchanged.
UNWIND ['Ada', 'Grace'] AS name
MERGE (:Person {name: name});
// => first run: no matching nodes exist yet, so MERGE creates both

// the SAME retry simulation as the buggy version -- this time with MERGE.
UNWIND ['Ada', 'Grace'] AS name
MERGE (:Person {name: name});
// THE FIX: MERGE matches the already-loaded nodes instead of creating new ones

MATCH (p:Person)
RETURN count(p) AS person_count;
