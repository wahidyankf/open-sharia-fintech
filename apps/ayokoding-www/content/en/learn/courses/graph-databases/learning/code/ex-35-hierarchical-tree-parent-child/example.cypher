// Example 35: Walk a Hierarchical Tree Upward. (co-13)
CREATE (:Person {name: 'IC'})-[:REPORTS_TO]->(:Person {name: 'Manager'})
      -[:REPORTS_TO]->(:Person {name: 'Director'})-[:REPORTS_TO]->(:Person {name: 'CEO'});
// => a 3-hop reporting chain, IC at the bottom, CEO at the top

MATCH (ic:Person {name: 'IC'})-[:REPORTS_TO*]->(boss)
// => unbounded * walks the chain AS FAR AS IT GOES upward from ic
RETURN boss.name;
// => hand-traced: Manager (1 hop), Director (2 hops), CEO (3 hops) -- the WHOLE chain upward
