// Example 78a: the knowledge-graph facts, as a labeled property graph. (co-02)
CREATE (:Person {name: 'Ada'})-[:WORKS_AT]->(:Organization {name: 'Analytical Labs'})
// => Person node, WORKS_AT relationship, Organization node -- all in one CREATE
      -[:FOCUSES_ON]->(:Topic {name: 'Graph Databases'});
// => 3 typed nodes, 2 typed relationships -- properties (name) bundled directly onto each node
