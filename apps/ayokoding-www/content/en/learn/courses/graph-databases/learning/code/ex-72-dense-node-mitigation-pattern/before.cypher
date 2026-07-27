// Example 72a: BEFORE -- every verified account points DIRECTLY at one shared label node.
CREATE (verified:Status {label: 'verified'})
// => the single shared node every account below will connect to
WITH verified
// => keep "verified" bound into the UNWIND+CREATE below -- ONE statement, NO semicolon after the
// first CREATE; a semicolon there would end the statement and "verified" would go out of scope,
// silently minting a fresh blank node per row instead of sharing one (see Example 43)
UNWIND range(1, 5) AS i
// => 5 accounts, deliberately small here -- the same shape scales to 100,000 in production
CREATE (:Account {name: 'Acc' + toString(i)})-[:HAS_STATUS]->(verified);
// => "verified" is now a SUPERNODE -- its degree grows by 1 for every verified account, unbounded
