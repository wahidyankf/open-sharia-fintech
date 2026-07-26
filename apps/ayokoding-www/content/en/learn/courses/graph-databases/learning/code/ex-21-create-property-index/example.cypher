// Example 21: Create a Property Index.
CREATE INDEX person_born FOR (p:Person) ON (p.born);
// => co-22: accelerates any future lookup filtering on p.born

CREATE (:Person {name: 'Ada', born: 1815});
// => the row EXPLAIN below will target
CREATE (:Person {name: 'Grace', born: 1906});
// => a second row, present so the index has more than one entry to choose between

EXPLAIN MATCH (p:Person) WHERE p.born = 1815 RETURN p;
// => EXPLAIN prints the QUERY PLAN without running it -- confirms the index gets used
