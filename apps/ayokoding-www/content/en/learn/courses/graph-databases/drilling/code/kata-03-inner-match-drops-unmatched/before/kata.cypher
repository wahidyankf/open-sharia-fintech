// Kata 3 (before): a plain second MATCH behaves like an inner join -- it drops
// anyone whose DIRECTED pattern finds nothing, instead of keeping their row.
CREATE (:Person {name: 'Ada'});
// => Ada has directed NOTHING -- expected to still appear in the report
CREATE (:Person {name: 'Grace'})-[:DIRECTED]->(:Movie {title: 'Compile Error'});
// => Grace directed exactly one movie

MATCH (p:Person)
// => matches BOTH Ada and Grace so far
MATCH (p)-[:DIRECTED]->(m:Movie)
// BUG: a second plain MATCH requires the pattern to ALSO match, dropping Ada entirely
RETURN p.name, m.title;
