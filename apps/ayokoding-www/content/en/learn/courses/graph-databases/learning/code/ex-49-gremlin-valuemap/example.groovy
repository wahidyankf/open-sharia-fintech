// Example 49: Gremlin: valueMap() (LEGACY overload -- flagged deliberately). (co-25)
graph = TinkerGraph.open()
g = graph.traversal()

g.addV('person').property('name', 'Ada').property('born', 1815).iterate()
// => one vertex, two properties

g.V().hasLabel('person').valueMap(true)
// => valueMap(true) is the LEGACY, deprecated overload -- it still works today, but it is no
// longer the recommended current-TinkerPop way to include vertex id + labels alongside properties.
// Prefer .valueMap().with(WithOptions.tokens) or .elementMap() in new code instead.
