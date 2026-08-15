---
title: "Learning Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Concepts

1. **co-01 · dependency-injection** — dependencies are declared and supplied by the container.
2. **co-02 · inversion-of-control** — the container owns construction and lifecycle.
3. **co-03 · constructor-injection** — constructors make required dependencies explicit.
4. **co-04 · beans** — component stereotypes register managed collaborators.
5. **co-05 · bean-lifecycle** — scope and lifecycle affect instance behavior.
6. **co-06 · configuration** — configuration classes declare explicit beans.
7. **co-07 · autoconfiguration** — Boot configures supported classpath conventions.
8. **co-08 · starters** — starters provide coherent managed dependency sets.
9. **co-09 · application-properties** — external configuration changes behavior without source edits.
10. **co-10 · profiles** — profiles select environment-specific configuration.
11. **co-11 · rest-controller** — controllers bind HTTP requests to JSON responses.
12. **co-12 · request-mapping** — mappings bind path, query, and body inputs.
13. **co-13 · service-layer** — services hold business decisions between HTTP and persistence.
14. **co-14 · repository-layer** — repositories isolate persistence access.
15. **co-15 · validation** — constraints reject invalid input at the boundary.
16. **co-16 · error-handling** — advice maps failures to stable error envelopes.
17. **co-17 · jpa-entity** — entities model table-backed state.
18. **co-18 · jpa-repository** — repository interfaces provide CRUD and queries.
19. **co-19 · transactions** — transactions make a multi-step write atomic.
20. **co-20 · n-plus-one** — ORM traversal can multiply queries and needs measurement.
21. **co-21 · json-serialization** — DTOs are serialized at HTTP boundaries.
22. **co-22 · actuator** — health and metrics expose operational state.
23. **co-23 · testing-spring** — whole-context and slice tests have different scopes.
24. **co-24 · mock-bean** — MockitoBean replaces a context collaborator in a focused test.
25. **co-25 · jvm-classloading** — classes load lazily through class loaders.
26. **co-26 · jit** — hot code is optimized after warm-up.
27. **co-27 · gc-generational** — short-lived allocation is collected efficiently.
28. **co-28 · gc-collectors** — collector choice exposes throughput/pause trade-offs.
29. **co-29 · memory-model** — heap behavior and pauses are measurable operational signals.
30. **co-30 · packaging** — Boot packages a runnable jar.

Every ex-01 through ex-78 has a colocated source artifact under
[learning/code](./code/README.md).
