// Example 42: Fraud Cycle Detection. (co-16, co-09)
CREATE (a:Account {name: 'A'})-[:SENT]->(:Account {name: 'B'})-[:SENT]->(:Account {name: 'C'})-[:SENT]->(a);
// => a planted 3-hop CYCLE: A -> B -> C -> A -- money flows back to its own origin

MATCH p = (a:Account)-[:SENT*3..5]->(a)
RETURN [n IN nodes(p) | n.name] AS ring;
// => co-09: the pattern's start and end node are the SAME variable "a" -- only a real cycle matches
