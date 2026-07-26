// Example 27: OPTIONAL MATCH Preserves Rows as NULL.
CREATE (:Person {name: 'Ada'});
// => Ada has NO relationships at all
CREATE (m:Person {name: 'Grace'})-[:DIRECTED]->(:Movie {title: 'Compile Error'});
// => Ada directed nothing; Grace directed one movie -- deliberately asymmetric fixture

// OPTIONAL MATCH (co-05) never drops the outer row, even when the inner pattern matches nothing.
MATCH (p:Person)
// => matches BOTH Ada and Grace, unfiltered
OPTIONAL MATCH (p)-[:DIRECTED]->(m)
// => for Ada, this inner pattern finds NOTHING -- but her outer row survives anyway
RETURN p.name, m;
// => Ada's row SURVIVES with m = NULL -- a plain MATCH here would have dropped her entirely
