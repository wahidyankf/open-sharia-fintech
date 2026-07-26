// Example 13: A Relationship with Properties.
CREATE (a:Person {name: 'Ada'}), (m:Movie {title: 'The Long Compile'})
// => two bare nodes, aliased a and m, no relationship between them YET
CREATE (a)-[:RATED {stars: 5, on: '2026-01-04'}]->(m);
// => the {stars, on} property map lives ON THE RELATIONSHIP (co-01, co-11), not on a or m

MATCH (a:Person)-[r:RATED]->(m:Movie)
// => r is bound to the RELATIONSHIP itself, not either endpoint node
RETURN a.name, r.stars, m.title;
// => r.stars reads directly off the relationship -- neither node was touched to store it
