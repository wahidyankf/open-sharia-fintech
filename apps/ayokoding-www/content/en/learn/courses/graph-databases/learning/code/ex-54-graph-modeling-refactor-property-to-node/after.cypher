// Example 54b: city refactored into its OWN node + relationship. (co-11)
CREATE (:Person {name: 'Ada'})-[:LIVES_IN]->(:City {name: 'Berlin', population: 3700000});
// => city now HAS its own attributes (population) -- impossible when it was a scalar property

MATCH (p:Person)-[:LIVES_IN]->(c:City)
WHERE c.population > 1000000
RETURN p.name, c.name;
// => a query against CITY's own attributes now works -- it could not before the refactor
