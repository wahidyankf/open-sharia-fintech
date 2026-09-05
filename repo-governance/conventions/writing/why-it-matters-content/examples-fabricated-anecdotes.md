---
title: "Examples: Fabricated Anecdotes"
description: Worked before/after rewrites of a fabricated corporate case study and a fabricated platform scenario
category: explanation
subcategory: conventions
tags:
  - ayokoding-www
  - tutorial-content
  - factual-accuracy
  - why-it-matters
  - hallucination-prevention
created: 2026-05-09
when_to_use: Read this when rewriting a Why It Matters section that names a company or cites an unsourced metric.
---

# Examples: Fabricated Anecdotes

## Before and After: Removing a Fabricated Corporate Case Study

**FAIL: Prohibited (fabricated corporate case study)**

```markdown
**Why It Matters**: When Shopify refactored order processing from anemic to rich
domain models, they reduced order-related bugs by 73%. Business rules previously
scattered across 15 service classes were consolidated into domain objects, making
the codebase dramatically easier to maintain.
```

Problems with this example:

- Names a real company (Shopify) without a citable source
- Provides specific metrics (73%, 15 service classes) that appear precise but are invented
- No engineering blog post, paper, or conference talk supports this claim

**PASS: Required (theoretical explanation)**

```markdown
**Why It Matters**: Anemic domain models scatter business rules across service classes
rather than encapsulating them in domain objects. This creates three compounding problems:
business rules become invisible to domain experts, they duplicate silently across services
as the system grows, and they are difficult to test in isolation. Martin Fowler identified
the Anemic Domain Model as an anti-pattern in 2003, noting that it violates object-oriented
principles by separating data from the behaviour that operates on it. When domain objects
own their invariants, the same logic that makes an order invalid in a unit test is the
same logic that runs in production — there is no gap for bugs to enter.
```

This rewrite conveys the same pedagogical value — readers understand why the pattern
matters — without fabricating evidence.

---

## Before and After: Replacing a Generic Platform Scenario

**FAIL: Prohibited (fabricated platform scenario)**

```markdown
**Why It Matters**: A ride-sharing platform integrated this pattern and saw their
service recovery time drop from 45 seconds to under 3 seconds during peak load.
The pattern prevents cascading failures from taking down the entire system.
```

Problems:

- "A ride-sharing platform" is a fabricated stand-in for a company name
- "45 seconds to under 3 seconds" is a specific metric with no source
- The final sentence is the actual valuable insight; the anecdote adds nothing

**PASS: Required (theoretical explanation)**

```markdown
**Why It Matters**: Without circuit breaker isolation, a slow or failing downstream
service holds connections open until they time out. Under load, new requests queue
behind the blocked ones, exhausting the thread pool and bringing the calling service
down as well. The pattern prevents this cascade by failing fast — returning an
immediate error rather than waiting — which keeps the rest of the system operational.
Recovery happens through periodic probing rather than waiting for the operator to
intervene.
```

---
