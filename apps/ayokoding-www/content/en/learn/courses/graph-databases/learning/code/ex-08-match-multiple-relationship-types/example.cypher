// Example 8: Match Multiple Relationship Types.
CREATE (m:Movie {title: 'Null Pointer Blues'})
// => one Movie, aliased m
CREATE (m)<-[:ACTED_IN]-(:Person {name: 'Ada'})
// => Ada ACTED_IN m
CREATE (m)<-[:DIRECTED]-(:Person {name: 'Grace'});
// => Grace DIRECTED the SAME m -- same two-edge-type shape as Example 7

// The pipe (co-07) means "either type" -- both edges now fit the pattern.
MATCH (:Movie)<-[:ACTED_IN|DIRECTED]-(p:Person)
// => the OR now admits BOTH relationship types in one pattern
RETURN p.name;
// => BOTH Ada and Grace come back -- the pattern (co-08) no longer excludes DIRECTED
