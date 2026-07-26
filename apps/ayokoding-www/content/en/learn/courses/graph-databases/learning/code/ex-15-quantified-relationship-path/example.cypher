// Example 15: Quantified Relationship Path (GQL-conformant syntax, Cypher 25).
CREATE (:Stop {name: 'Central'})-[:NEXT]->(:Stop {name: 'Market'})-[:NEXT]->(:Stop {name: 'Pier'});
// => same shape as Example 14's fixture, renamed Stop/NEXT to keep the two examples independent

// -[:NEXT]->{1,3} (co-09, co-21) is the GQL-conformant quantified-relationship equivalent of *1..3.
MATCH (a:Stop {name: 'Central'})-[:NEXT]->{1,3}(b:Stop)
RETURN b.name;
// => same traversal semantics as Example 14 -- Market (1 hop) and Pier (2 hops) both qualify
