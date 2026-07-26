// Example 12b: age represented as a SEPARATE node + relationship, for contrast.
CREATE (p:Person {name: 'Ada'})-[:IN_AGE_GROUP]->(:AgeGroup {label: '30-39'});
// => modeling age as its own node ADDS a hop for what was a scalar fact

MATCH (p:Person {name: 'Ada'})-[:IN_AGE_GROUP]->(g:AgeGroup)
RETURN g.label;
// => now needs a 1-hop traversal to read what used to be a direct property
