// Example 77: Gremlin: Cycle-Safe repeat().until(). (co-25, co-09)
graph = TinkerGraph.open()               // => a fresh in-memory graph, no server required
g = graph.traversal()                    // => the traversal source every step below chains off

g.addV('person').property('name', 'Ada').as('a').    // => vertex 1: Ada, aliased 'a' for reuse
  addV('person').property('name', 'Bob').as('b').    // => vertex 2: Bob, aliased 'b'
  addV('person').property('name', 'Zoe').as('z').    // => vertex 3: Zoe, aliased 'z'
  addE('knows').from('a').to('b').                   // => edge: Ada -> Bob
  addE('knows').from('b').to('z').                   // => edge: Bob -> Zoe
  addE('knows').from('z').to('a').   // => deliberately plants a CYCLE: Ada -> Bob -> Zoe -> Ada
  iterate()                                           // => forces the whole chain above to execute now

g.V().has('name', 'Ada').                             // => starts the traversal at Ada specifically
  repeat(out('knows').simplePath()).until(has('name', 'Zoe')).  // => walks until it reaches Zoe
  path().by('name')                                    // => returns the walked path, name-projected
// => .simplePath() forbids revisiting a vertex ALREADY on the current path -- without it, the
// planted cycle above could loop the traversal indefinitely around Ada -> Bob -> Zoe -> Ada -> ...
// => .by('name') projects EVERY vertex on the path through its `name` property -- without it,
// .path() emits raw Vertex objects, which TinkerGraph renders as v[<numeric-id>], never as a name
