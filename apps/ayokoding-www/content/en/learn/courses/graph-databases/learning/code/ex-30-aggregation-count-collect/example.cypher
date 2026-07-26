// Example 30: Aggregate with count() and collect().
CREATE (p:Person {name: 'Ada'})-[:ACTED_IN]->(:Movie {title: 'M1'})
// => Ada's first movie, p aliased for reuse
CREATE (p)-[:ACTED_IN]->(:Movie {title: 'M2'});
// => Ada's second movie -- two ACTED_IN edges off the SAME person

// co-23: p.name is the IMPLICIT grouping key -- collect(m.title) aggregates per group.
MATCH (p:Person)-[:ACTED_IN]->(m)
// => two rows come out of this MATCH, one per ACTED_IN edge
RETURN p.name, collect(m.title) AS movies;
// => one row per DISTINCT p.name, with every matching m.title folded into a single list
