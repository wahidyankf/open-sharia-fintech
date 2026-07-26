// Example 52: Pin a Query to Cypher 5. (co-21)
CREATE (:Order {id: 1, status: 'shipped'});

CYPHER 5 MATCH (n:Order) RETURN n;
// => the CYPHER 5 prefix pins THIS query to the frozen dialect -- bug-fixes only, no new features,
// regardless of whatever the database's own default_language setting happens to be configured to
