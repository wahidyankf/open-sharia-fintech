// Example 51b: the SAME question, Cypher over a property graph.
CREATE (a:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Charles'})
// => Ada's first KNOWS edge, a aliased for reuse
CREATE (a)-[:KNOWS]->(:Person {name: 'Babbage'});
// => Ada's second KNOWS edge -- same two-fact fixture as the SPARQL form above

MATCH (:Person {name: 'Ada'})-[:KNOWS]->(n:Person)
// => n is bound to a full NODE object, not a triple-pattern object
RETURN n.name;
// => the NODE bound to n, for every matching pattern -- co-02's contrast, made concrete
