// Kata 5 (before): no CREATE CONSTRAINT was ever run -- nothing stops a duplicate name.
CREATE (:Person {name: 'Ada'});
// => succeeds -- the first (and, if a constraint existed, the ONLY) Person named Ada
CREATE (:Person {name: 'Ada'});
// BUG: a SECOND node with the same name -- nothing rejects it, because no constraint exists

MATCH (p:Person {name: 'Ada'})
RETURN count(p) AS ada_count;
