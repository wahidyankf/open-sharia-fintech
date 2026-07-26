// Example 80a: property-graph representation (co-02).
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Charles'});
// => plants the one fact both other representations encode identically
MATCH (:Person {name: 'Ada'})-[:KNOWS]->(n) RETURN n.name;
// => "Charles" -- a bound NODE's property, via a directed, typed relationship pattern
