// Example 80c: Gremlin representation (co-25).
graph = TinkerGraph.open(); g = graph.traversal()  // => a fresh in-memory graph, no server required
g.addV('person').property('name', 'Ada').as('a').    // => vertex 1: Ada, aliased for reuse
  addV('person').property('name', 'Charles').as('c').  // => vertex 2: Charles
  addE('knows').from('a').to('c').iterate()            // => the SAME single fact, as an edge
g.V().has('name', 'Ada').out('knows').values('name')
// => a step-chained traversal result, imperative rather than declarative
