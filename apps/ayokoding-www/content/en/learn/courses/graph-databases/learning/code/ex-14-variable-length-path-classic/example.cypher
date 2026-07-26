// Example 14: Variable-Length Path (Classic Syntax).
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})-[:KNOWS]->(:Person {name: 'Cid'});
// => a 2-hop chain: Ada -> Bob -> Cid

// [:KNOWS*1..3] (co-09) traverses 1, 2, OR 3 hops of :KNOWS in one pattern -- still valid syntax,
// though not GQL-conformant (see Example 15 for the modern equivalent).
MATCH (a:Person {name: 'Ada'})-[:KNOWS*1..3]-(b:Person)
RETURN DISTINCT b.name;
// => hand-traced: Bob (1 hop) and Cid (2 hops) both fall within *1..3 -- DISTINCT drops duplicates
