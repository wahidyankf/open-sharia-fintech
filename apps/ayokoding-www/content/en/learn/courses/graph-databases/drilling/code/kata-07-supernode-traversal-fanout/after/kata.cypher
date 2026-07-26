// Kata 7 (after): matching through the SPECIFIC team avoids the supernode entirely.
CREATE (allstaff:Group {name: 'AllStaff'})
WITH allstaff
UNWIND range(1, 18) AS i
CREATE (:Person {name: 'Emp' + toString(i)})-[:MEMBER_OF]->(allstaff)
WITH allstaff
CREATE (ada:Person {name: 'Ada'})-[:MEMBER_OF]->(allstaff)
CREATE (bob:Person {name: 'Bob'})-[:MEMBER_OF]->(allstaff)
WITH ada, bob
CREATE (team:Group {name: 'GraphTeam'})
CREATE (ada)-[:MEMBER_OF]->(team)
CREATE (bob)-[:MEMBER_OF]->(team);

// THE FIX: match through GraphTeam (degree 2), not AllStaff (degree 20).
MATCH (a:Person {name: 'Ada'})-[:MEMBER_OF]->(grp:Group {name: 'GraphTeam'})<-[:MEMBER_OF]-(colleague:Person)
WHERE colleague <> a
RETURN colleague.name;
