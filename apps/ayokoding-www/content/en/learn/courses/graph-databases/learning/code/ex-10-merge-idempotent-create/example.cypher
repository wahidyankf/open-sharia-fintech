// Example 10: MERGE Is Idempotent Create.
// MERGE (co-06) is run TWICE in this one file, back to back, on purpose.
MERGE (p:Person {name: 'Ada'});
// => first run: no matching node exists yet, so MERGE CREATES it
MERGE (p:Person {name: 'Ada'});
// => second run: a node with these exact properties NOW exists, so MERGE MATCHES it instead

MATCH (p:Person {name: 'Ada'})
RETURN count(p) AS ada_count;
// => count(p) proves only ONE node exists after two MERGE calls, not two
