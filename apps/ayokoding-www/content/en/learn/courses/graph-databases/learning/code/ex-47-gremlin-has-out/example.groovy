// Example 47: Gremlin: has() and out(). (co-25, co-08)
graph = TinkerGraph.open()  // => a fresh in-memory graph, no server required
g = graph.traversal()  // => the traversal source every step below chains off

g.addV('person').property('name', 'Ada').as('a').
  addV('person').property('name', 'Charles').as('c').
  addE('knows').from('a').to('c').iterate()
// => same fixture shape as Example 46 -- Ada KNOWS Charles

g.V().has('person', 'name', 'Ada').out('knows').values('name')
// => has() FILTERS the vertex set down to the ONE starting vertex
// => out('knows') then steps ONE hop forward along that edge label
// => values('name') projects just the name property off the resulting vertex
