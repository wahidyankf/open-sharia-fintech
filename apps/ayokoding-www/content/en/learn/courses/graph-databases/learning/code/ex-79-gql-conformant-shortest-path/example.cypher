// Example 79: GQL-Conformant SHORTEST Path Selector. (co-21, co-10)
// ONE query, two CREATE clauses with NO semicolon between them, so a and z stay bound
// across BOTH clauses -- exactly Example 16's fix, avoiding a second Ada/Zoe pair.
CREATE (a:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})-[:KNOWS]->(z:Person {name: 'Zoe'})
// => a 2-hop chain: Ada(a) -> Bob -> Zoe(z)
CREATE (a)-[:KNOWS]->(z);
// => a DIRECT 1-hop shortcut, reusing the SAME a and z -- the identical fixture shape as Example 16

MATCH p = SHORTEST 1 (a:Person {name: 'Ada'})-[:KNOWS]-+(b:Person {name: 'Zoe'})
// => co-21: SHORTEST 1 is the GQL-conformant path-SELECTOR syntax -- "1" means return the
// single shortest match; -+ quantifies one-or-more hops of :KNOWS in the GQL-conformant style
RETURN length(p);
// => 1 -- the direct shortcut wins over the 2-hop chain, same answer as Example 16's shortestPath()
