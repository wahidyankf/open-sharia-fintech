// Example 64: Model a Small Knowledge Graph. (co-01, co-11, co-08)
CREATE (ada:Person {name: 'Ada'})-[:WORKS_AT]->(org:Organization {name: 'Analytical Labs'})
// => Person -[:WORKS_AT]-> Organization, the first typed relationship
CREATE (org)-[:FOCUSES_ON]->(:Topic {name: 'Graph Databases'});
// => Person -> Organization -> Topic, three DIFFERENT node types, two DIFFERENT relationship types

MATCH (p:Person {name: 'Ada'})-[:WORKS_AT]->(org:Organization)-[:FOCUSES_ON]->(t:Topic)
// => a single chained pattern walks BOTH typed relationships in one MATCH
RETURN p.name, org.name, t.name;
// => 2-hop pattern (co-08): who -> through which org -> works on what topic
