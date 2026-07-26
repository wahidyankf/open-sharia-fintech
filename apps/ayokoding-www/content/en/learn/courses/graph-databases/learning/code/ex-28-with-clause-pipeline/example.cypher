// Example 28: Pipeline a Query with WITH.
CREATE (p1:Person {name: 'Ada'})-[:ACTED_IN]->(:Movie {title: 'M1'})
// => Ada's first movie, p1 aliased for reuse below
CREATE (p1)-[:ACTED_IN]->(:Movie {title: 'M2'})
// => Ada's second movie
CREATE (p1)-[:ACTED_IN]->(:Movie {title: 'M3'})
// => Ada's third movie
CREATE (:Person {name: 'Bob'})-[:ACTED_IN]->(:Movie {title: 'M4'});
// => Ada: 3 movies, Bob: 1 movie

// WITH (co-23) carries p and the computed movies count FORWARD into a second WHERE stage.
MATCH (p:Person)-[:ACTED_IN]->(m)
// => matches every (person, movie) pair, one row per ACTED_IN edge
WITH p, count(m) AS movies
// => aggregates rows PER person -- movies is now a count, not individual movie rows
WHERE movies > 2
// => this filter runs AFTER aggregation -- impossible with a plain WHERE alone
RETURN p.name, movies;
// => Bob (1 movie) is filtered out HERE -- a plain WHERE before aggregation cannot express this
