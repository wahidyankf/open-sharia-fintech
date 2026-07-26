// Example 3: Create a Directed Relationship.
// One CREATE pattern writes BOTH endpoint nodes AND the relationship between them (co-01).
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Charles'});
// => TWO new nodes (Ada, Charles) AND one new :KNOWS relationship, Ada -> Charles
// => direction matters: this does NOT imply Charles knows Ada back

// Round-trip check: the pattern must match with the SAME direction it was written.
MATCH (a:Person {name: 'Ada'})-[:KNOWS]->(b:Person {name: 'Charles'})
RETURN a.name, b.name;
// => matches -- Ada is the start node, Charles is the end node, exactly as created (co-07)
