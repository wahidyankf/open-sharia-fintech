# Graph Databases (By Example, Cypher + Python)

**Course ID**: `graph-databases` · **Format**: By Example · **Language**: Cypher + Python.

**Short summary**: Modeling and querying connected data

**Scope note**: the property-graph model and Cypher — nodes/relationships/properties, traversal, and the
problems where a graph beats relational (recommendations, fraud, knowledge graphs) — accessed from Python.
`†`: Cypher is the query language (note GQL = ISO/IEC 39075:2024). Sits beside the other non-relational
families in [`34-nosql-databases`](./nosql-databases.md).

## Why this exists · the big idea

- **The problem before the solution**: when the relationships between entities are the real question
  (who-knows-whom, paths, recommendations), a relational store answers with join explosions that get
  exponentially slower with each hop.
- **Keep-this-if-you-forget-everything**: when connections are first-class data, model them as first-class —
  a graph makes a k-hop traversal cost roughly k, where the relational equivalent multiplies.
- **Big ideas touched**: `consistency-latency-throughput` (deep-traversal performance is the win),
  `coupling-vs-cohesion` (the domain here _is_ connectedness itself).

## Prerequisites

- **Prior topics**: [topic 10 SQL Essentials](./sql-essentials.md) (the relational model to contrast),
  [topic 34 NoSQL Databases](./nosql-databases.md) (the non-relational framing), and
  [topic 4 Just Enough Python](./just-enough-python.md).
- **Tools & environment**: a macOS/Linux terminal; a local **Neo4j** (or GQL-compatible) instance (Docker
  fine; check the edition license); **Python 3.x** with a pinned CVE-clean driver; the Cypher shell.
- **Assumed knowledge**: relational joins (to feel the contrast); basic Python driver use; the idea of
  entities and relationships.

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **GQL = ISO/IEC 39075:2024** (published 2024-04-12, first new ISO DB query-language
  standard since SQL/1987, Cypher-inspired, SQL's sibling). **Neo4j Community Edition = GPLv3** (not
  AGPLv3 — confirmed against the official `neo4j/neo4j` repo; secondary sources conflate this with Enterprise
  Edition's AGPLv3 history). (iso.org/standard/76120 / github.com/neo4j/neo4j)
- 2026-07-12 — verified (CORRECTION, version-sensitive): Neo4j moved to **calendar versioning** (2025.x,
  2026.x) and now ships **two parallel Cypher versions** — **Cypher 5** (frozen, bug-fixes only) and
  **Cypher 25** (evolving; default for new databases from Neo4j 2026.02). Content must state which Cypher
  version its examples target rather than assuming a single unversioned "Cypher." (neo4j.com/docs/cypher-manual)
- 2026-07-12 — DD-34/DD-35 enumeration sweep (per-store primary-source read): variable-length `[:REL*1..3]`
  is "still available but not GQL conformant"; the GQL-conformant equivalents are quantified relationships
  (`-[:REL]->{1,3}`) and the `SHORTEST k`/`ALL SHORTEST` path selectors — both taught, in sequence. GDS
  procedure names verified current (`gds.pageRank.stream`, `gds.betweenness.stream` — promoted out of the
  older `gds.alpha.*` namespace; `gds.shortestPath.dijkstra` vs `gds.allShortestPaths.dijkstra` are distinct).
  SPARQL 1.1 (W3C Rec, 2013) is the stable version to teach — SPARQL 1.2 is W3C Working-Draft-only as of
  2026-07 and must not be cited as fact. `[Needs Verification]` at authoring time: the exact `[:REL*1..3]`
  literal example against a current Neo4j doc page, the SPARQL `CONSTRUCT` grammar block, and Gremlin
  `hasLabel()` — all well-attested but re-confirm the exact syntax at content-authoring. (neo4j.com/docs/cypher-manual/current/patterns · neo4j.com/docs/graph-data-science/current · w3.org/TR/sparql11-query · tinkerpop.apache.org/docs/current/reference)

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · property-graph-model** — a property graph is built from nodes, relationships, labels, and key/value properties as first-class citizens.
- **co-02 · labeled-property-graph-vs-rdf** — the labeled-property-graph model (Neo4j-style) differs from an RDF triple-store, which represents every fact as a subject-predicate-object triple.
- **co-03 · when-graph-beats-relational** — deeply connected, relationship-heavy, variable-depth queries are where a graph traversal beats a relational join chain.
- **co-04 · index-free-adjacency** — each node stores a direct pointer to its adjacent relationships, so a hop's cost stays proportional to the local neighborhood rather than the whole graph.
- **co-05 · cypher-read-clauses** — `MATCH`/`WHERE`/`RETURN` form Cypher's core read pipeline: pattern-match, filter, project.
- **co-06 · cypher-write-clauses** — `CREATE` unconditionally writes a pattern; `MERGE` matches-or-creates it idempotently, with `ON CREATE`/`ON MATCH` branches.
- **co-07 · relationship-direction-and-type** — a Cypher relationship pattern is directed and typed (`()-[:REL]->()`), and both direction and type narrow a match.
- **co-08 · pattern-matching** — a Cypher query is a declarative graph shape: the engine finds every subgraph matching the drawn pattern.
- **co-09 · variable-length-and-quantified-paths** — the classic `[:REL*1..3]` syntax (still valid, not GQL-conformant) and the modern quantified relationship/path-pattern syntax (`-[:REL]->{1,3}`, GQL-conformant) both traverse a variable number of hops in one pattern.
- **co-10 · shortest-path-queries** — the legacy `shortestPath()`/`allShortestPaths()` functions and the modern GQL-conformant `SHORTEST k`/`ALL SHORTEST`/`ANY` path selectors compute minimum-hop or minimum-weight paths.
- **co-11 · graph-modeling-nodes-vs-properties-vs-relationships** — deciding whether a fact becomes a node, a property, or a relationship is the central graph-modeling skill.
- **co-12 · many-to-many-modeling** — a relationship, which can itself carry properties, replaces a join table for many-to-many facts.
- **co-13 · hierarchical-tree-modeling** — parent/child hierarchies are modeled as directed relationships walked recursively.
- **co-14 · bill-of-materials-modeling** — a recursive part-of graph (assemblies containing sub-assemblies) is a canonical variable-depth graph problem.
- **co-15 · recommendation-queries** — "people who did X also did Y" recommendations are graph traversals over shared connections.
- **co-16 · fraud-pattern-detection** — suspicious structures (shared identifiers, payment rings, dense clusters) surface as graph patterns that row-at-a-time relational scans miss.
- **co-17 · supernodes-and-dense-node-problem** — a node with a disproportionate relationship count slows traversal through it and needs deliberate handling.
- **co-18 · graph-sharding-challenges** — partitioning a densely connected graph across machines inherently cuts relationships, unlike sharding independent rows.
- **co-19 · acid-transactions-in-graph-dbs** — Neo4j operations run inside fully ACID transactions, unlike the eventual-consistency norm common elsewhere in NoSQL.
- **co-20 · bulk-import-and-loading** — `LOAD CSV` (online, transactional, row-at-a-time) and `neo4j-admin database import` (offline, high-throughput, whole-database) are the two data-loading paths.
- **co-21 · neo4j-versioning-and-editions** — Neo4j's calendar versioning (2025.x/2026.x) ships two parallel Cypher language versions, frozen Cypher 5 and evolving Cypher 25, selectable per query.
- **co-22 · constraints-and-indexes** — `CREATE CONSTRAINT`/`CREATE INDEX` enforce uniqueness and accelerate property lookups in an otherwise schema-optional store.
- **co-23 · aggregation-and-pipelining** — `WITH`, `UNWIND`, `CALL {}` subqueries, `ORDER BY`/`LIMIT`/`SKIP`, and aggregating functions chain query stages and shape results.
- **co-24 · rdf-triples-and-sparql** — RDF models facts as subject-predicate-object triples, queried with SPARQL's `SELECT`/`WHERE`/`FILTER`/`OPTIONAL`/`PREFIX`.
- **co-25 · gremlin-traversal-language** — Gremlin (Apache TinkerPop) is an imperative, step-chained traversal language (`g.V().has().out()`) portable across many graph engines.
- **co-26 · graph-data-science-procedures** — centrality (PageRank, betweenness) and community detection (Louvain) run as callable GDS library procedures over an in-memory graph projection.

## Worked examples

Colocated under `graph-databases/learning/code/`; Cypher (Neo4j) / SPARQL / Gremlin plus a Python driver,
each runnable (DD-20/DD-30). Contiguous `ex-01..ex-80`. Every example cites the `co-NN` it exercises;
every concept above is exercised by ≥1 example.

### Beginner

- **ex-01 · create-single-node** — `CREATE (:Person {name: 'Ada', born: 1815})` — verify `MATCH (p:Person {name:'Ada'}) RETURN p` returns exactly one row. (co-01, co-06)
- **ex-02 · create-node-with-multiple-labels** — `CREATE (:Person:Engineer {name: 'Grace'})` — verify `MATCH (n) WHERE n:Person AND n:Engineer RETURN n` finds it. (co-01)
- **ex-03 · create-directed-relationship** — `CREATE (:Person {name:'Ada'})-[:KNOWS]->(:Person {name:'Charles'})` — verify a `MATCH` pattern round-trips both endpoints and the direction. (co-01, co-07)
- **ex-04 · match-return-all-nodes** — `MATCH (n) RETURN n LIMIT 25` — verify the returned count matches the seeded fixture size. (co-05)
- **ex-05 · match-where-filter** — `MATCH (p:Person) WHERE p.born < 1900 RETURN p.name` — verify only pre-1900 people are returned. (co-05)
- **ex-06 · match-relationship-pattern** — `MATCH (a:Person)-[:KNOWS]->(b:Person) RETURN a.name, b.name` — verify every returned pair has a real `KNOWS` edge. (co-05, co-07, co-08)
- **ex-07 · match-relationship-type-filter** — `MATCH (:Movie)<-[:ACTED_IN]-(actor:Person) RETURN actor.name` — verify only `ACTED_IN` edges (not `DIRECTED`) are matched. (co-07, co-08)
- **ex-08 · match-multiple-relationship-types** — `MATCH (:Movie)<-[:ACTED_IN|DIRECTED]-(p:Person) RETURN p.name` — verify people connected either way appear. (co-07, co-08)
- **ex-09 · undirected-pattern-match** — `MATCH (a:Person)--(b:Person) RETURN a.name, b.name` — verify direction-agnostic matches include both directions. (co-07, co-08)
- **ex-10 · merge-idempotent-create** — run `MERGE (p:Person {name:'Ada'})` twice — verify only one node exists after both runs. (co-06)
- **ex-11 · merge-on-create-on-match** — `MERGE (p:Person {name:'Ada'}) ON CREATE SET p.created = timestamp() ON MATCH SET p.seen = coalesce(p.seen,0)+1` — verify the branch taken matches whether the node pre-existed. (co-06)
- **ex-12 · property-vs-node-decision** — model "age" as a property vs a separate `AgeGroup` node — verify the property choice keeps the query one hop. (co-11)
- **ex-13 · relationship-with-properties** — `CREATE (a)-[:RATED {stars: 5}]->(m)` — verify the property reads off the relationship, not a node. (co-01, co-11)
- **ex-14 · variable-length-path-classic** — `MATCH (a:Person)-[:KNOWS*1..3]-(b:Person) RETURN DISTINCT b.name` — verify friends-of-friends up to 3 hops matches a hand count. (co-09)
- **ex-15 · quantified-relationship-path** — `MATCH (a:Stop)-[:NEXT]->{1,3}(b:Stop) RETURN b.name` — verify the same result set as ex-14's classic `*1..3` form on an equivalent fixture. (co-09, co-21)
- **ex-16 · shortest-path-legacy-function** — `MATCH p = shortestPath((a:Person {name:'Ada'})-[:KNOWS*]-(b:Person {name:'Zoe'})) RETURN length(p)` — verify the hop count matches a hand-traced path. (co-10)
- **ex-17 · all-shortest-paths-legacy** — `MATCH p = allShortestPaths((a)-[:KNOWS*..4]-(b)) RETURN p` — verify every returned path has the same minimal length. (co-10)
- **ex-18 · index-free-adjacency-timing** — time a 1-hop traversal on a 10-node vs 10,000-node graph — verify latency stays flat rather than scaling with total graph size. (co-04)
- **ex-19 · graph-vs-relational-join-explosion** — run the same 4-hop "friends of friends of friends" question as SQL self-joins vs one Cypher pattern — verify the SQL join count grows with each hop while the Cypher query stays one pattern. (co-03)
- **ex-20 · create-unique-constraint** — `CREATE CONSTRAINT person_name FOR (p:Person) REQUIRE p.name IS UNIQUE` — verify a duplicate-name insert is rejected. (co-22)
- **ex-21 · create-property-index** — `CREATE INDEX person_born FOR (p:Person) ON (p.born)` — verify `EXPLAIN MATCH (p:Person) WHERE p.born = 1815 RETURN p` shows the index in the plan. (co-22)
- **ex-22 · acid-transaction-rollback** — wrap two writes in one Python driver transaction and force an error on the second — verify the first write is rolled back, not partially committed. (co-19)
- **ex-23 · load-csv-basic** — `LOAD CSV WITH HEADERS FROM 'file:///people.csv' AS row MERGE (:Person {name: row.name})` — verify the node count equals the CSV row count. (co-20)
- **ex-24 · neo4j-admin-bulk-import** — `neo4j-admin database import full --nodes=... --relationships=...` against a fresh database — verify imported counts match the source files. (co-20)
- **ex-25 · rdf-triple-basic** — write three RDF triples (`ex:Ada ex:knows ex:Charles .`) in Turtle — verify each is a valid subject-predicate-object statement. (co-24, co-02)
- **ex-26 · sparql-select-basic** — `SELECT ?name WHERE { ?p foaf:name ?name }` over the triples from ex-25 — verify the same "who does Ada know" answer as the Cypher version in ex-06. (co-24, co-02)

### Intermediate

- **ex-27 · optional-match-nulls** — `MATCH (p:Person) OPTIONAL MATCH (p)-[:DIRECTED]->(m) RETURN p.name, m` — verify people with no `DIRECTED` edge return `null`, not a dropped row. (co-05)
- **ex-28 · with-clause-pipeline** — `MATCH (p:Person)-[:ACTED_IN]->(m) WITH p, count(m) AS movies WHERE movies > 2 RETURN p.name` — verify only prolific actors pass the `WITH` filter. (co-23)
- **ex-29 · unwind-list-to-rows** — `UNWIND [1, 2, 3] AS x CREATE (:Number {value: x})` — verify three separate nodes are created. (co-23)
- **ex-30 · aggregation-count-collect** — `MATCH (p:Person)-[:ACTED_IN]->(m) RETURN p.name, collect(m.title) AS movies` — verify each actor's movie list matches expectation. (co-23)
- **ex-31 · order-limit-skip** — `MATCH (p:Person) RETURN p ORDER BY p.born DESC LIMIT 5 SKIP 0` — verify the 5 most-recently-born people are returned in order. (co-23)
- **ex-32 · call-subquery** — `MATCH (t:Team) CALL (t) { MATCH (p:Player)-[:PLAYS_FOR]->(t) RETURN collect(p) AS players } RETURN t, players` — verify per-team player lists are correctly scoped. (co-23, co-05)
- **ex-33 · many-to-many-join-table-vs-relationship** — model "students take courses" as a join table (SQL) vs a `TAKES` relationship (Cypher) — verify both return the same enrollment answer; contrast query shape. (co-12, co-03)
- **ex-34 · relationship-property-many-to-many** — `(s:Student)-[:TAKES {grade:'A'}]->(c:Course)` — verify the grade is queryable per enrollment, not duplicated per student. (co-12)
- **ex-35 · hierarchical-tree-parent-child** — model an org chart with `[:REPORTS_TO]` and walk it upward — verify the chain from an IC to the CEO. (co-13)
- **ex-36 · hierarchical-tree-downward** — find all direct+indirect reports of a manager via a reversed variable-length `[:REPORTS_TO*]` pattern — verify against a hand-built org tree. (co-13, co-09)
- **ex-37 · bill-of-materials-parts-explosion** — model `(:Part)-[:PART_OF]->(:Assembly)` and traverse all sub-parts of a top assembly — verify the full parts list matches a hand-built BOM. (co-14, co-09)
- **ex-38 · bom-relational-contrast** — the same BOM query as a recursive SQL CTE vs the Cypher variable-length pattern — verify identical results; note the SQL CTE's added complexity. (co-14, co-03)
- **ex-39 · recommendation-co-occurrence** — `MATCH (u:User)-[:BOUGHT]->(:Item)<-[:BOUGHT]-(other)-[:BOUGHT]->(rec:Item) WHERE NOT (u)-[:BOUGHT]->(rec) RETURN rec, count(*) AS score ORDER BY score DESC` — verify recommended items exclude already-bought ones. (co-15, co-08)
- **ex-40 · recommendation-collaborative-filter** — extend ex-39 with a minimum shared-purchase threshold — verify low-overlap users are excluded from scoring. (co-15, co-23)
- **ex-41 · fraud-shared-attribute-ring** — `MATCH (a:Account)-[:USES]->(d:Device)<-[:USES]-(b:Account) WHERE a <> b RETURN a, b, d` — verify a planted shared-device fraud ring surfaces and an unrelated pair does not. (co-16, co-08)
- **ex-42 · fraud-cycle-detection** — `MATCH p=(a:Account)-[:SENT*3..5]->(a) RETURN p` — verify a planted circular-payment ring is detected. (co-16, co-09)
- **ex-43 · supernode-identification** — `MATCH (n) RETURN n, size((n)--()) AS degree ORDER BY degree DESC LIMIT 5` — verify the top-degree node matches a known synthetic supernode. (co-17)
- **ex-44 · supernode-traversal-cost** — compare traversal time expanding through a supernode vs an average-degree node — verify the supernode expansion is measurably slower. (co-17, co-04)
- **ex-45 · graph-sharding-edge-cut** — partition a small synthetic graph across two shards by a naive node-ID split — verify the number of relationships crossing shards is nonzero and costly to traverse. (co-18)
- **ex-46 · gremlin-add-vertex-edge** — `g.addV('person').property('name','Ada').as('a').addV('person').property('name','Charles').as('c').addE('knows').from('a').to('c')` — verify both vertices and the edge exist via a follow-up traversal. (co-25, co-01)
- **ex-47 · gremlin-has-out** — `g.V().has('person','name','Ada').out('knows').values('name')` — verify it returns `'Charles'`, matching the Cypher equivalent from ex-06. (co-25, co-08)
- **ex-48 · gremlin-path-step** — `g.V().has('name','Ada').repeat(out('knows')).times(2).path()` — verify the returned path length matches a hand-traced 2-hop walk. (co-25, co-09)
- **ex-49 · gremlin-valuemap** — `g.V().hasLabel('person').valueMap(true)` — verify every vertex's properties and id are returned as a map. (co-25)
- **ex-50 · sparql-filter-optional** — `SELECT ?name ?mbox WHERE { ?x foaf:name ?name . OPTIONAL { ?x foaf:mbox ?mbox } FILTER regex(?name, "Ada") }` — verify a person without an email still appears with an unbound `?mbox`. (co-24)
- **ex-51 · sparql-vs-cypher-same-question** — answer "who does Ada know" in both SPARQL and Cypher against equivalent data — verify identical answer sets; contrast triple-pattern vs property-graph syntax. (co-24, co-02)
- **ex-52 · cypher-version-pin-cypher5** — prefix a query with the `CYPHER 5` version directive (`CYPHER 5 MATCH (n:Order) RETURN n`) — verify it executes under the frozen Cypher 5 dialect. (co-21)
- **ex-53 · cypher-version-pin-cypher25** — prefix with `CYPHER 25` (`CYPHER 25 MATCH (n:Order) RETURN n`) — verify it executes under Cypher 25 and returns the identical result to ex-52. (co-21)
- **ex-54 · graph-modeling-refactor-property-to-node** — refactor a `city: 'Berlin'` property into a `(:City {name:'Berlin'})` node plus a `[:LIVES_IN]` relationship because city needs its own attributes — verify queries against city attributes now work. (co-11)

### Advanced

- **ex-55 · gds-graph-projection** — `CALL gds.graph.project('social', 'Person', 'KNOWS') YIELD graphName, nodeCount, relationshipCount` — verify the projected counts match the source graph. (co-26)
- **ex-56 · gds-pagerank-stream** — `CALL gds.pageRank.stream('social') YIELD nodeId, score` — verify the highest-scoring node matches the known most-connected person in a synthetic fixture. (co-26)
- **ex-57 · gds-betweenness-centrality** — `CALL gds.betweenness.stream('social') YIELD nodeId, score` — verify a known bridge node scores highest. (co-26)
- **ex-58 · gds-louvain-community-detection** — `CALL gds.louvain.stream('social') YIELD nodeId, communityId` — verify two planted clusters resolve to two distinct community IDs. (co-26)
- **ex-59 · gds-node-similarity** — `CALL gds.nodeSimilarity.stream('social') YIELD node1, node2, similarity` — verify two users with heavily overlapping purchases score high similarity. (co-26, co-15)
- **ex-60 · gds-dijkstra-source-target** — `CALL gds.shortestPath.dijkstra.stream('social', {sourceNode: a, targetNode: b}) YIELD totalCost, path` — verify the weighted cost matches a hand-computed shortest path. (co-26, co-10)
- **ex-61 · gds-dijkstra-single-source** — `CALL gds.allShortestPaths.dijkstra.stream('social', {sourceNode: a}) YIELD targetNode, totalCost` — verify distances to every reachable node match individually-computed shortest paths. (co-26, co-10)
- **ex-62 · recommendation-with-gds-similarity** — combine `gds.nodeSimilarity` output with a Cypher `MATCH` to produce ranked item recommendations — verify the top recommendation for a seeded user matches expectation. (co-26, co-15)
- **ex-63 · fraud-ring-with-community-detection** — run Louvain over a transaction graph and flag any community above a density threshold — verify a planted fraud ring is flagged and a normal community is not. (co-26, co-16)
- **ex-64 · knowledge-graph-modeling** — model people, organizations, and topics with typed relationships; query a 2-hop "who works on what topic through which org" pattern — verify against a hand-built answer. (co-01, co-11, co-08)
- **ex-65 · knowledge-graph-vs-relational-contrast** — the same knowledge-graph query as SQL joins across 4 normalized tables vs one Cypher pattern — verify identical results; document the join-count difference. (co-03, co-08)
- **ex-66 · capstone-load-domain** — `.../learning/capstone/code/load.py` loads the domain via Cypher `MERGE` from a Python driver — verify node/relationship counts match the source dataset exactly. (co-06, co-20)
- **ex-67 · capstone-neighborhood-query** — a Python-driven neighborhood query (1-hop + 2-hop) over the loaded domain — verify results against a hand-checked small case. (co-05, co-08)
- **ex-68 · capstone-friends-of-friends** — a variable-length friends-of-friends query run from Python — verify the result set matches a hand-traced subgraph. (co-09)
- **ex-69 · capstone-shortest-path** — a Python-driven shortest-path query over the loaded domain — verify the path length against a hand-traced minimum. (co-10)
- **ex-70 · capstone-recommendation** — a "people who X also Y" recommendation query run from Python — verify the top recommendation is sensible and reproducible. (co-15)
- **ex-71 · capstone-relational-contrast** — write the equivalent relational query with explicit joins for the capstone domain — verify the contrast document names the exact join count and query text. (co-03)
- **ex-72 · dense-node-mitigation-pattern** — refactor a supernode (e.g. a "verified" label shared by 100k accounts) into an intermediate grouping node — verify traversal through the refactored model is measurably cheaper. (co-17, co-11)
- **ex-73 · sharding-strategy-comparison** — compare a naive ID-range shard vs a community-aware (Louvain-informed) shard on the same graph — verify the community-aware shard cuts fewer relationships. (co-18, co-26)
- **ex-74 · acid-concurrent-write-conflict** — two concurrent Python driver transactions writing the same node's property — verify Neo4j's locking causes one to fail/retry rather than silently corrupt the value. (co-19)
- **ex-75 · constraint-enforced-on-bulk-import** — attempt `neo4j-admin database import` with duplicate unique-constrained keys — verify the import tool reports the violation rather than silently loading duplicates. (co-22, co-20)
- **ex-76 · sparql-construct-derived-graph** — a `CONSTRUCT` query building a new triple set from matched patterns — verify the derived triples match the expected inferred facts. (co-24)
- **ex-77 · gremlin-repeat-until-cycle-safe** — `g.V().has('name','Ada').repeat(out('knows').simplePath()).until(has('name','Zoe')).path()` — verify the traversal terminates and avoids revisiting nodes in a cyclic graph. (co-25, co-09)
- **ex-78 · property-graph-vs-rdf-modeling-tradeoff** — model the same knowledge-graph facts as both a labeled-property-graph and an RDF triple set — verify both represent the same facts; contrast query ergonomics and standardization trade-offs. (co-02, co-24)
- **ex-79 · gql-conformant-shortest-path** — `MATCH p = SHORTEST 1 (a:Person)-[:KNOWS]-+(b:Person) RETURN length(p)` — the modern, GQL-conformant path-selector syntax replacing legacy `shortestPath()` — verify it returns the identical length as ex-16's legacy query on the same fixture. (co-21, co-10)
- **ex-80 · capstone-preview-multi-model-report** — `.../learning/capstone/code/contrast.md` compares the same recommendation domain across property-graph (Cypher), RDF (SPARQL), and Gremlin representations — verify each representation answers the same question and the report states the trade-offs concretely with query text. (co-02, co-24, co-25, co-03)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small recommendation/knowledge-graph over a property graph — load a domain (people +
  items + relationships), answer real graph questions (neighborhoods, variable-length paths, shortest
  path, a recommendation), from Python — and contrast the equivalent relational query to show why the
  graph wins.
- **Concepts exercised**: [ ] property-graph modeling (nodes/rels/labels) (co-01, co-11) [ ] Cypher
  `MATCH`/`MERGE` (co-05, co-06) [ ] a variable-length traversal (co-09) [ ] a shortest-path query (co-10)
  [ ] a recommendation query (co-15) [ ] a graph-vs-SQL contrast (co-03).
- **Ordered steps**:
  1. `.../learning/capstone/code/load.py` — load the domain via Cypher `MERGE`. Verify node/relationship
     counts match the dataset.
  2. `queries.cypher` + `run.py` — neighborhood + friends-of-friends (variable-length) queries. Verify
     results match a hand-checked small case.
  3. `recommend.py` — a "people who X also Y" recommendation + a shortest-path query. Verify sensible,
     verifiable output.
  4. `contrast.md` — the equivalent relational query with its join explosion; explain the graph advantage.
     Verify the contrast is concrete (query text + why).
- **Acceptance criteria**: the graph loads correctly; every query returns verifiable results; the
  recommendation is sensible; the relational contrast is concrete and justified.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Graph Databases: New Opportunities for Connected Data** — Ian Robinson, Jim Webber, Emil Eifrem (2015, 2nd ed.). Free, canonical introduction to property graph modeling and the graph database landscape. <https://graphdatabases.com/>
- **Graph Algorithms: Practical Examples in Apache Spark and Neo4j** — Mark Needham & Amy E. Hodler (2019). Standard reference on classic graph algorithms — PageRank, community detection, centrality — applied to graph databases.

**Papers & articles**

- **Cypher: An Evolving Query Language for Property Graphs** — Nadime Francis, Alastair Green, Paolo Guagliardo, Leonid Libkin, et al. (2018). Paper formalizing the semantics of Cypher, the query language later standardized as part of ISO GQL. <https://dl.acm.org/doi/10.1145/3183713.3190657>
- **Apache TinkerPop / Gremlin Reference Documentation** — Apache Software Foundation (continually maintained). The canonical specification and reference for the Gremlin graph traversal language used across many graph databases. <https://tinkerpop.apache.org/docs/current/reference/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Data depth — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Data depth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 6 · Databases & data depth.

> _Content originated in the now-closed FS-SE plan (topic 35); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
