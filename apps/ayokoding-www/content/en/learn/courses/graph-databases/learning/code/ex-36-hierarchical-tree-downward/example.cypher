// Example 36: Walk a Hierarchical Tree Downward. (co-13, co-09)
// ONE query, two CREATE clauses with NO semicolon between them, so mgr stays bound
// across BOTH clauses -- this is what avoids accidentally creating a SECOND Manager node.
CREATE (mgr:Person {name: 'Manager'})<-[:REPORTS_TO]-(:Person {name: 'Senior'})
      <-[:REPORTS_TO]-(:Person {name: 'Junior'})
// => a 2-hop downward chain off mgr: Manager <- Senior <- Junior
CREATE (mgr)<-[:REPORTS_TO]-(:Person {name: 'Senior2'});
// => a THIRD, direct report, reusing the SAME mgr -- not a second Manager node

MATCH (m:Person {name: 'Manager'})<-[:REPORTS_TO*]-(report)
// => reversed arrow (co-09) walks DOWNWARD -- every direct AND indirect report of Manager
RETURN DISTINCT report.name;
// => three reports total: Senior (1 hop), Senior2 (1 hop), Junior (2 hops, via Senior)
