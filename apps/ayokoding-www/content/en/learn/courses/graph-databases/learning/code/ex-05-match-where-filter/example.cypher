// Example 5: Match with a WHERE Filter.
CREATE (:Person {name: 'Ada', born: 1815});
// => born BEFORE the 1900 cutoff -- expected to survive the filter below
CREATE (:Person {name: 'Grace', born: 1906});
// => born AFTER 1900 -- expected to be filtered OUT
CREATE (:Person {name: 'Alan', born: 1912});
// => also born after 1900 -- expected to be filtered OUT too

// WHERE (co-05) filters the matched pattern before RETURN projects it.
MATCH (p:Person)
// => matches all 3 people, unfiltered so far
WHERE p.born < 1900
// => the boolean condition every surviving row must satisfy
RETURN p.name;
// => only Ada (born 1815) satisfies p.born < 1900 -- Grace and Alan are filtered out
