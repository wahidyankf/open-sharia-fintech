// Example 34: A Property on a Many-to-Many Relationship. (co-12)
CREATE (s:Student {name: 'Ada'})-[:TAKES {grade: 'A'}]->(:Course {name: 'Graph Theory'})
// => Ada's first enrollment, s aliased for reuse -- grade 'A' lives ON this edge
CREATE (s)-[:TAKES {grade: 'B'}]->(:Course {name: 'Databases'});
// => the SAME student, two different enrollments, each with its OWN grade on the edge

MATCH (s:Student)-[t:TAKES]->(c:Course)
// => t is bound to the RELATIONSHIP -- t.grade below reads off the edge, not a node
RETURN c.name, t.grade;
// => t.grade is queryable PER enrollment -- not duplicated onto the student or the course
