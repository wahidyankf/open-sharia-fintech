// Example 53: Pin a Query to Cypher 25. (co-21)
CREATE (:Order {id: 1, status: 'shipped'});

CYPHER 25 MATCH (n:Order) RETURN n;
// => same query, same fixture as Example 52, pinned to the EVOLVING Cypher 25 dialect instead --
// identical result here, because this particular pattern uses no dialect-specific feature
