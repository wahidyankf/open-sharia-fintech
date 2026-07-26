// Example 7: Filter by Relationship Type.
CREATE (m:Movie {title: 'Segfault at Dawn'})
// => one Movie node, aliased m for the next two CREATE lines to reuse
CREATE (m)<-[:ACTED_IN]-(:Person {name: 'Ada'})
// => Ada ACTED_IN m
CREATE (m)<-[:DIRECTED]-(:Person {name: 'Grace'});
// => Grace DIRECTED the SAME m -- two DIFFERENT relationship types on one movie

// Naming :ACTED_IN in the pattern (co-07) excludes the :DIRECTED edge entirely.
MATCH (:Movie)<-[:ACTED_IN]-(actor:Person)
// => the relationship TYPE is part of the pattern's shape -- :DIRECTED simply does not fit here
RETURN actor.name;
// => only Ada -- Grace's :DIRECTED edge simply does not fit this pattern's shape (co-08)
