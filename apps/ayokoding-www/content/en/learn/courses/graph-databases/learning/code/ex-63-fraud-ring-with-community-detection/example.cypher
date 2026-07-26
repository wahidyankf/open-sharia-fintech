// Example 63: Fraud Ring via Community Detection. (co-26, co-16)
// A DENSE, fully-connected ring of 4 accounts -- every account transacts with every other one.
CREATE (r1:Account {name: 'R1'})-[:SENT]->(r2:Account {name: 'R2'})-[:SENT]->(r3:Account {name: 'R3'})
      -[:SENT]->(r4:Account {name: 'R4'})-[:SENT]->(r1)
      // => closes the ring: R4 sends back to R1, completing a 4-node cycle
CREATE (r1)-[:SENT]->(r3)
// => a CROSS-ring edge, R1 to R3 -- extra density beyond the base cycle
CREATE (r2)-[:SENT]->(r4);
// => 6 edges among 4 nodes -- a DENSE ring, deliberately over-connected
// A normal, sparse pair, for contrast.
CREATE (:Account {name: 'N1'})-[:SENT]->(:Account {name: 'N2'});
// => 1 edge among 2 nodes -- ordinary, un-suspicious density

CALL gds.graph.project('txns', 'Account', 'SENT');
// => projects both the ring and the ordinary pair into memory under the name 'txns'

CALL gds.louvain.stream('txns')
// => streams one row per node, each tagged with the community Louvain assigned it
YIELD nodeId, communityId
// => nodeId is an internal GDS handle -- resolved to a real node's name on the next line
WITH communityId, collect(gds.util.asNode(nodeId).name) AS members, count(*) AS size
// => groups nodes by their assigned community, collecting names and counting membership size
WHERE size >= 4
// => the density-proxy threshold: only communities with 4+ members are flagged as suspicious
RETURN communityId, members;
// => only the RING's community clears the size>=4 flag -- the normal pair never approaches it
