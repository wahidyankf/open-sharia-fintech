// Kata 4 (after): *1..2 bounds the traversal to exactly the "nearby" scope intended.
CREATE (:Person {name: 'Ada'})-[:KNOWS]->(:Person {name: 'Bob'})
      -[:KNOWS]->(:Person {name: 'Cid'})-[:KNOWS]->(:Person {name: 'Dee'})
      -[:KNOWS]->(:Person {name: 'Eve'});

// THE FIX: *1..2 bounds the walk to at most 2 hops, matching the widget's real intent.
MATCH (a:Person {name: 'Ada'})-[:KNOWS*1..2]->(b:Person)
RETURN b.name
ORDER BY b.name;
