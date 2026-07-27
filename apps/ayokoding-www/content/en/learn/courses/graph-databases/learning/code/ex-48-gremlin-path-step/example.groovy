// Example 48: Gremlin: repeat().path(). (co-25, co-09)
graph = TinkerGraph.open()  // => a fresh in-memory graph, no server required
g = graph.traversal()  // => the traversal source every step below chains off

g.addV('person').property('name', 'Ada').as('a').
  addV('person').property('name', 'Bob').as('b').
  addV('person').property('name', 'Cid').as('c').
  addE('knows').from('a').to('b').
  addE('knows').from('b').to('c').iterate()
// => a 2-hop chain: Ada -> Bob -> Cid, identical shape to Example 14's Cypher fixture
// => .iterate() actually EXECUTES the traversal -- Gremlin traversals are lazy until iterated

g.V().has('name', 'Ada').repeat(out('knows')).times(2).path().by('name')
// => repeat(out('knows')) is the STEP to repeat -- one knows-hop, per repetition
// => .times(2) bounds the repeat to EXACTLY 2 repetitions
// => .path() returns the full route walked, not just the final vertex
// => .by('name') projects EVERY vertex on the path through its `name` property -- without it,
// .path() emits raw Vertex objects, which TinkerGraph renders as v[<numeric-id>], never as a name
