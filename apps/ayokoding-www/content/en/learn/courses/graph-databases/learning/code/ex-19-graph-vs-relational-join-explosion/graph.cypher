// Example 19b: the SAME 3-hop question, one Cypher pattern (co-03).
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})
      -[:KNOWS]->(:Person {name: 'Cid'})-[:KNOWS]->(:Person {name: 'Dee'});
// => the IDENTICAL 3-hop chain as the SQL fixture above -- Ada->Bob->Cid->Dee

// *3 means EXACTLY 3 hops -- the same shape a 4-hop question would need only *4 for.
MATCH (a:Person {name: 'Ada'})-[:KNOWS*3]->(d:Person)
// => co-03: ONE pattern, no matter how deep the bound goes
RETURN d.name;
// => one pattern, exact-3-hop bound -- changing *3 to *4 is a ONE-character edit, not 2 new JOINs
