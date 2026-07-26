// Example 46: Gremlin: Add a Vertex and an Edge. (co-25, co-01)
// Run inside the TinkerPop Gremlin Console -- TinkerGraph is a pure in-memory, embedded
// graph engine, so this needs no external server, matching this example's self-containment.
graph = TinkerGraph.open()               // => a fresh in-memory graph, no server required
g = graph.traversal()                    // => the traversal source every step below chains off

g.addV('person').property('name', 'Ada').as('a').
  addV('person').property('name', 'Charles').as('c').
  addE('knows').from('a').to('c').iterate()
// => step-chained: TWO vertices created, aliased 'a' and 'c', THEN one edge between them
// => .iterate() actually EXECUTES the traversal -- Gremlin traversals are lazy until iterated

g.V().has('person', 'name', 'Ada').out('knows').values('name')
// => follow-up traversal: confirms BOTH the vertices and the edge landed correctly
