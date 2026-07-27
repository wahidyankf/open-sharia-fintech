// Example 31: ORDER BY, LIMIT, and SKIP.
CREATE (:Person {name: 'Ada', born: 1815});
// => oldest of the five
CREATE (:Person {name: 'Grace', born: 1906});
CREATE (:Person {name: 'Alan', born: 1912});
CREATE (:Person {name: 'Katherine', born: 1918});
// => second-most-recently born
CREATE (:Person {name: 'Radia', born: 1943});
// => most recently born of the five -- expected to sort FIRST under DESC below

// co-23: ORDER BY sorts, LIMIT caps, SKIP offsets -- all THREE apply AFTER RETURN's projection.
MATCH (p:Person)
// => all 5 people, unfiltered
RETURN p.name
// => projects just the name -- born is used for sorting only, not returned
ORDER BY p.born DESC
// => sorts the 5 rows newest-born first
SKIP 0
// => SKIP 0 means "start from the very top" -- must precede LIMIT (Cypher clause order is
// ORDER BY, then SKIP, then LIMIT)
LIMIT 3;
// => the 3 MOST RECENTLY BORN people, most recent first
