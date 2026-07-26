// Example 33b: the SAME many-to-many fact, a TAKES relationship (co-12, co-03).
CREATE (:Student {name: 'Ada'})-[:TAKES]->(:Course {name: 'Graph Theory'});
// => the relationship itself IS the join table -- no separate junction node needed

MATCH (s:Student)-[:TAKES]->(c:Course)
// => a single 1-hop pattern -- no intermediate junction to join through
RETURN s.name, c.name;
// => ZERO extra joins -- the pattern is one hop, whether one student or one thousand
