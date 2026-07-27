// Example 43: Identify a Supernode by Degree. (co-17)
// ONE statement, NO semicolon after the first CREATE -- hub must stay bound into the
// UNWIND+CREATE below; a semicolon there would end the statement and hub would be undefined.
CREATE (hub:Person {name: 'Hub'})
// => the eventual supernode -- currently degree 0
WITH hub
UNWIND range(1, 20) AS i
// => generates 20 rows, i = 1 through 20
CREATE (hub)-[:KNOWS]->(:Person {name: 'Leaf' + toString(i)});
// => Hub now has 20 KNOWS edges -- a deliberately synthetic SUPERNODE
CREATE (:Person {name: 'Ordinary'})-[:KNOWS]->(:Person {name: 'Friend'});
// => an ordinary node with degree 1, for contrast

MATCH (n)
// => every node in the database, Hub, its 20 leaves, and the ordinary pair
RETURN n.name, COUNT { (n)--() } AS degree
// => undirected degree count, per node
ORDER BY degree DESC
// => highest-degree node sorts first
LIMIT 5;
// => "Hub" comes back FIRST with degree=20 -- every Leaf and the ordinary pair trail far behind
