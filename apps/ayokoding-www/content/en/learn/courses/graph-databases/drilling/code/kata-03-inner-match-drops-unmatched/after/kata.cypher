// Kata 3 (after): OPTIONAL MATCH keeps every outer row, even with zero DIRECTED edges.
CREATE (:Person {name: 'Ada'});
CREATE (:Person {name: 'Grace'})-[:DIRECTED]->(:Movie {title: 'Compile Error'});

MATCH (p:Person)
// THE FIX: OPTIONAL MATCH never drops the outer row, filling m with NULL instead
OPTIONAL MATCH (p)-[:DIRECTED]->(m:Movie)
RETURN p.name, m.title;
