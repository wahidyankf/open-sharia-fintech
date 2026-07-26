// Example 6: Match a Relationship Pattern.
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Charles'});
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Babbage'});
// => Ada now KNOWS two different people -- two separate :KNOWS relationships

// The pattern (a)-[:KNOWS]->(b) (co-05, co-07, co-08) matches once PER real edge found.
MATCH (a:Person)-[:KNOWS]->(b:Person)
RETURN a.name, b.name;
// => two rows -- one per real KNOWS edge -- because pattern-matching enumerates every occurrence
