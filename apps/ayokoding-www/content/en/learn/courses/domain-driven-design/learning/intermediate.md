---
title: "Intermediate Examples"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 20
---

## Aggregates, repositories, and domain events

Each complete artifact is annotated and runnable with `python3 example.py`; its assertion is the
observable result. The design consequence names the boundary the example protects.

### Worked Example 29: Aggregate boundary

**Context**: An order owns its lines. **Artifact**: [`example.py`](code/ex-29-aggregate-boundary/example.py). **Observable result**: the root totals children. **Design consequence**: related changes enter one consistency boundary. **Key takeaway**: aggregate state belongs to its root.

### Worked Example 30: Aggregate-root access

**Context**: Expose lines read-only. **Artifact**: [`example.py`](code/ex-30-aggregate-root-access/example.py). **Observable result**: callers receive a tuple. **Design consequence**: external mutation cannot skip the root. **Key takeaway**: only roots mutate children.

### Worked Example 31: Cross-child invariant

**Context**: Enforce an order credit limit. **Artifact**: [`example.py`](code/ex-31-aggregate-invariant-across-children/example.py). **Observable result**: over-limit additions raise. **Design consequence**: a rule sees the full child set. **Key takeaway**: put each invariant in one aggregate.

### Worked Example 32: Consistency boundary

**Context**: Replace lines atomically. **Artifact**: [`example.py`](code/ex-32-consistency-boundary/example.py). **Observable result**: invalid replacement leaves old state. **Design consequence**: no partial aggregate persists. **Key takeaway**: validate complete state before commit.

### Worked Example 33: Small aggregate

**Context**: Separate customer profile from orders. **Artifact**: [`example.py`](code/ex-33-small-aggregate/example.py). **Observable result**: order stores customer id. **Design consequence**: unrelated histories do not contend. **Key takeaway**: make roots as small as true invariants allow.

### Worked Example 34: Reference by identity

**Context**: Use `CustomerId`, not `Customer`. **Artifact**: [`example.py`](code/ex-34-reference-by-identity/example.py). **Observable result**: order exists without another root. **Design consequence**: aggregate loading stays local. **Key takeaway**: reference other aggregates by id.

### Worked Example 35: One aggregate per transaction

**Context**: Queue inventory work after placement. **Artifact**: [`example.py`](code/ex-35-one-aggregate-per-transaction/example.py). **Observable result**: placement returns a request. **Design consequence**: one commit protects one root. **Key takeaway**: defer cross-root work.

### Worked Example 36: Eventual consistency

**Context**: Inventory handles an order fact. **Artifact**: [`example.py`](code/ex-36-eventual-consistency-across-aggregates/example.py). **Observable result**: stock converges after handling. **Design consequence**: a cross-root rule is explicit about delay. **Key takeaway**: events coordinate independent roots.

### Worked Example 37: Repository port

**Context**: Define a persistence capability. **Artifact**: [`example.py`](code/ex-37-repository-port/example.py). **Observable result**: the Protocol names `add` and `get`. **Design consequence**: domain policy avoids storage imports. **Key takeaway**: a repository is a domain-facing port.

### Worked Example 38: In-memory adapter

**Context**: Implement the port with a dictionary. **Artifact**: [`example.py`](code/ex-38-repository-in-memory-adapter/example.py). **Observable result**: add/get round-trips. **Design consequence**: tests need no database. **Key takeaway**: adapters are replaceable details.

### Worked Example 39: One repository per root

**Context**: Keep order and customer collections distinct. **Artifact**: [`example.py`](code/ex-39-repository-one-per-root/example.py). **Observable result**: keys never overlap collections. **Design consequence**: lifecycle boundaries remain clear. **Key takeaway**: repositories manage aggregate roots.

### Worked Example 40: Collection illusion

**Context**: Use collection-like repository operations. **Artifact**: [`example.py`](code/ex-40-repository-collection-illusion/example.py). **Observable result**: callers index saved roots. **Design consequence**: storage remains hidden. **Key takeaway**: repositories express persistence as a collection.

### Worked Example 41: Swap adapter

**Context**: Persist through a `Store` protocol. **Artifact**: [`example.py`](code/ex-41-repository-swap-adapter/example.py). **Observable result**: the memory adapter receives the value. **Design consequence**: caller code survives an adapter swap. **Key takeaway**: depend on the port.

### Worked Example 42: Reconstitute aggregate

**Context**: Map storage data through the root constructor. **Artifact**: [`example.py`](code/ex-42-aggregate-reconstitution/example.py). **Observable result**: invalid totals cannot re-enter. **Design consequence**: persistence respects domain rules. **Key takeaway**: reconstitution is valid construction.

### Worked Example 43: Define a domain event

**Context**: Record `OrderPlaced`. **Artifact**: [`example.py`](code/ex-43-domain-event-define/example.py). **Observable result**: id and timestamp are captured. **Design consequence**: a past business fact becomes explicit. **Key takeaway**: events are facts, not commands.

### Worked Example 44: Raise a domain event

**Context**: Root records a placement fact. **Artifact**: [`example.py`](code/ex-44-domain-event-raise/example.py). **Observable result**: event enters `pending_events`. **Design consequence**: root reports a meaningful transition. **Key takeaway**: raise events after valid state change.

### Worked Example 45: Event payload

**Context**: Carry id and amount. **Artifact**: [`example.py`](code/ex-45-domain-event-payload/example.py). **Observable result**: payload matches transition data. **Design consequence**: consumers receive the fact they need. **Key takeaway**: design payloads as stable facts.

### Worked Example 46: Event dispatch

**Context**: Publish to a subscriber. **Artifact**: [`example.py`](code/ex-46-domain-event-dispatch/example.py). **Observable result**: handler sees the event. **Design consequence**: producer and consumer need no direct reference. **Key takeaway**: publish through a boundary.

### Worked Example 47: Event decoupling

**Context**: Root avoids an inventory dependency. **Artifact**: [`example.py`](code/ex-47-domain-event-decouple/example.py). **Observable result**: root records only its event. **Design consequence**: consumers evolve independently. **Key takeaway**: events decouple reactions.

### Worked Example 48: Cross-aggregate event

**Context**: Inventory reserves on placement. **Artifact**: [`example.py`](code/ex-48-domain-event-cross-aggregate/example.py). **Observable result**: inventory changes through handler. **Design consequence**: each root protects its own state. **Key takeaway**: never mutate a foreign root inline.

### Worked Example 49: Application service

**Context**: Coordinate place and save. **Artifact**: [`example.py`](code/ex-49-application-service-orchestrate/example.py). **Observable result**: placed root is saved. **Design consequence**: orchestration stays thin. **Key takeaway**: application services sequence domain operations.

### Worked Example 50: Application versus domain service

**Context**: Ask root to approve. **Artifact**: [`example.py`](code/ex-50-application-vs-domain-service/example.py). **Observable result**: policy remains on root. **Design consequence**: application layer does not become anemic-model glue. **Key takeaway**: orchestration is not business policy.

### Worked Example 51: Layered architecture

**Context**: Point dependencies inward. **Artifact**: [`example.py`](code/ex-51-layered-architecture/example.py). **Observable result**: domain imports nothing outer. **Design consequence**: infrastructure cannot dictate policy. **Key takeaway**: the domain core has no outer dependency.

### Worked Example 52: Domain core isolation

**Context**: Make an import rule executable. **Artifact**: [`example.py`](code/ex-52-domain-core-no-infra/example.py). **Observable result**: forbidden packages are absent. **Design consequence**: architectural intent is testable. **Key takeaway**: enforce the dependency rule.

### Worked Example 53: Root invariant guard

**Context**: Keep children private. **Artifact**: [`example.py`](code/ex-53-aggregate-root-invariant-guard/example.py). **Observable result**: only a valid add path exists. **Design consequence**: callers cannot tamper with invariants. **Key takeaway**: expose commands, not mutable internals.

### Worked Example 54: Collection encapsulation

**Context**: Return an immutable view. **Artifact**: [`example.py`](code/ex-54-aggregate-collection-encapsulation/example.py). **Observable result**: tuple has no append. **Design consequence**: children remain root-controlled. **Key takeaway**: protect aggregate collections.

### Worked Example 55: Factory versus constructor

**Context**: Contrast a simple value and complex root. **Artifact**: [`example.py`](code/ex-55-factory-vs-constructor/example.py). **Observable result**: root gets a valid default. **Design consequence**: construction complexity stays proportional. **Key takeaway**: factories earn their indirection.

### Worked Example 56: Specification in repository

**Context**: Pass a predicate to a collection. **Artifact**: [`example.py`](code/ex-56-specification-in-repository/example.py). **Observable result**: only matching totals return. **Design consequence**: query policy remains named. **Key takeaway**: repositories can apply domain specifications.
