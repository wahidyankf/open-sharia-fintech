// Kata 7 (before): matching colleagues through the company-wide AllStaff group
// fans out through the HIGHEST-degree node in the graph, and returns nearly
// everyone instead of just the real team.
CREATE (allstaff:Group {name: 'AllStaff'})
// => the eventual SUPERNODE -- degree grows by 1 for every employee below
WITH allstaff
UNWIND range(1, 18) AS i
CREATE (:Person {name: 'Emp' + toString(i)})-[:MEMBER_OF]->(allstaff)
// => 18 unrelated employees, ALL connected to the SAME AllStaff node
WITH allstaff, count(*) AS _
// => an AGGREGATING WITH -- collapses the 18 UNWIND rows back to 1. A bare `WITH allstaff`
// here would still carry 18 rows, so every write below would fire 18 times, not once.
CREATE (ada:Person {name: 'Ada'})-[:MEMBER_OF]->(allstaff)
CREATE (bob:Person {name: 'Bob'})-[:MEMBER_OF]->(allstaff)
// => Ada and Bob also belong to AllStaff, like everyone else -- AllStaff's degree is now 20
WITH ada, bob
CREATE (team:Group {name: 'GraphTeam'})
CREATE (ada)-[:MEMBER_OF]->(team)
CREATE (bob)-[:MEMBER_OF]->(team);
// => GraphTeam's degree is only 2 -- just Ada and Bob, their REAL shared team

// BUG: matching through AllStaff instead of the specific team fans out through
// the highest-degree node in the whole graph, unnecessarily.
MATCH (a:Person {name: 'Ada'})-[:MEMBER_OF]->(grp:Group {name: 'AllStaff'})<-[:MEMBER_OF]-(colleague:Person)
WHERE colleague <> a
RETURN colleague.name
ORDER BY colleague.name;
