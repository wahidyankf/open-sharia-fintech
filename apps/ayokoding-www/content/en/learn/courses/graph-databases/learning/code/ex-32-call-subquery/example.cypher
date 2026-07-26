// Example 32: A CALL {} Subquery.
CREATE (t1:Team {name: 'Alpha'})<-[:PLAYS_FOR]-(:Player {name: 'Ada'})
// => Alpha's first player, t1 aliased for reuse
CREATE (t1)<-[:PLAYS_FOR]-(:Player {name: 'Bob'})
// => Alpha's second player
CREATE (t2:Team {name: 'Beta'})<-[:PLAYS_FOR]-(:Player {name: 'Cid'});
// => Alpha: 2 players, Beta: 1 player

MATCH (t:Team)
// => outer MATCH: one row per team, Alpha and Beta
CALL (t) {
  // co-05: this subquery re-matches per OUTER row -- t is explicitly scoped in via CALL (t)
  MATCH (p:Player)-[:PLAYS_FOR]->(t)
  // => finds players for THIS row's team only, never mixing across teams
  RETURN collect(p.name) AS players
  // => the subquery's own return value -- one list, scoped to this one team
}
RETURN t.name, players;
// => co-23: one correctly-scoped player list PER team, computed inside its own subquery
