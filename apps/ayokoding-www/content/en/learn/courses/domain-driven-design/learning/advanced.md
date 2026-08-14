---
title: "Advanced Examples"
date: 2026-08-14T00:00:00+07:00
draft: true
weight: 30
---

## Bounded contexts and integration

Each complete artifact is annotated and runnable with `python3 example.py`; its assertion records
the observable result. These examples favour explicit seams over a single enterprise-wide model.

### Worked Example 57: Define bounded contexts

**Context**: Sales and Shipping define different customers. **Artifact**: [`example.py`](code/ex-57-bounded-context-define/example.py). **Observable result**: each model has context-specific fields. **Design consequence**: one word need not carry every concern. **Key takeaway**: one model applies inside one bounded context.

### Worked Example 58: Model drift

**Context**: Product means price in Sales and weight in Shipping. **Artifact**: [`example.py`](code/ex-58-bounded-context-model-drift/example.py). **Observable result**: classes are unrelated. **Design consequence**: accidental sharing cannot blur meaning. **Key takeaway**: similarity is not a reason to share a model.

### Worked Example 59: Context-map relationships

**Context**: Type an upstream/downstream edge. **Artifact**: [`example.py`](code/ex-59-context-map-relationships/example.py). **Observable result**: edge includes relationship kind. **Design consequence**: teams discuss an explicit agreement. **Key takeaway**: map relationships, not only services.

### Worked Example 60: Anti-corruption layer

**Context**: Translate legacy client fields into Sales values. **Artifact**: [`example.py`](code/ex-60-anticorruption-layer/example.py). **Observable result**: Sales sees its own customer. **Design consequence**: legacy vocabulary stops at the edge. **Key takeaway**: ACLs protect downstream models.

### Worked Example 61: ACL isolation

**Context**: Check foreign symbols remain absent. **Artifact**: [`example.py`](code/ex-61-acl-isolation/example.py). **Observable result**: domain and legacy symbols are disjoint. **Design consequence**: integration cannot leak by accident. **Key takeaway**: make isolation verifiable.

### Worked Example 62: ACL translation map

**Context**: Translate field names and cents. **Artifact**: [`example.py`](code/ex-62-acl-translation-map/example.py). **Observable result**: sales gets ids and whole units. **Design consequence**: conversion logic has one explicit home. **Key takeaway**: map values, names, and units at the edge.

### Worked Example 63: Shared kernel

**Context**: Share a stable `Money` value. **Artifact**: [`example.py`](code/ex-63-shared-kernel/example.py). **Observable result**: billing and payroll agree on currency. **Design consequence**: the shared surface stays deliberately small. **Key takeaway**: share only what both teams can govern.

### Worked Example 64: Customer/supplier

**Context**: Orders publish shipping input. **Artifact**: [`example.py`](code/ex-64-customer-supplier/example.py). **Observable result**: Shipping consumes the agreed DTO. **Design consequence**: upstream serves an explicit downstream need. **Key takeaway**: negotiate the published contract.

### Worked Example 65: Conformist

**Context**: Adopt a provider payment model. **Artifact**: [`example.py`](code/ex-65-conformist/example.py). **Observable result**: downstream reads provider status directly. **Design consequence**: no translation cost is paid. **Key takeaway**: conform only when the upstream model is acceptable.

### Worked Example 66: Open host and published language

**Context**: Publish a versioned order DTO. **Artifact**: [`example.py`](code/ex-66-open-host-published-language/example.py). **Observable result**: consumers bind to V1. **Design consequence**: internal root changes need not break consumers. **Key takeaway**: publish an integration language, not your model.

### Worked Example 67: Core subdomain

**Context**: Identify pricing as differentiating. **Artifact**: [`example.py`](code/ex-67-subdomain-core/example.py). **Observable result**: pricing is classified core. **Design consequence**: modelling effort follows business advantage. **Key takeaway**: invest deeply in the core.

### Worked Example 68: Supporting and generic subdomains

**Context**: Classify catalog and notifications. **Artifact**: [`example.py`](code/ex-68-subdomain-supporting-generic/example.py). **Observable result**: gateway remains thin. **Design consequence**: generic work does not consume core-model effort. **Key takeaway**: buy or adapt generic capability.

### Worked Example 69: Core-domain focus

**Context**: Put loyalty policy into pricing. **Artifact**: [`example.py`](code/ex-69-core-domain-focus/example.py). **Observable result**: gold price changes through a named rule. **Design consequence**: differentiation has a rich model. **Key takeaway**: make core rules explicit.

### Worked Example 70: When DDD is overkill

**Context**: Model an address book plainly. **Artifact**: [`example.py`](code/ex-70-when-ddd-overkill/example.py). **Observable result**: a data class suffices. **Design consequence**: ceremony is avoided where no complex invariant exists. **Key takeaway**: use DDD in complex core domains.

### Worked Example 71: CQRS read/write split

**Context**: Separate order commands from summaries. **Artifact**: [`example.py`](code/ex-71-cqrs-read-write-split/example.py). **Observable result**: root writes and projection reads. **Design consequence**: each model optimizes its responsibility. **Key takeaway**: separate only when the trade-off pays.

### Worked Example 72: CQRS read model

**Context**: Query a denormalised summary. **Artifact**: [`example.py`](code/ex-72-cqrs-read-model/example.py). **Observable result**: query needs no aggregate load. **Design consequence**: read shape follows query needs. **Key takeaway**: projections serve reads, not invariants.

### Worked Example 73: Event-sourcing append

**Context**: Append order facts. **Artifact**: [`example.py`](code/ex-73-event-sourcing-append/example.py). **Observable result**: history retains both changes. **Design consequence**: current state is derivable. **Key takeaway**: events can become the persistence model.

### Worked Example 74: Event-sourcing replay

**Context**: Fold facts into state. **Artifact**: [`example.py`](code/ex-74-event-sourcing-replay/example.py). **Observable result**: replay reaches paid. **Design consequence**: state reconstruction is explicit. **Key takeaway**: replay must understand event order.

### Worked Example 75: Event-sourcing audit

**Context**: Reconstruct actor and time. **Artifact**: [`example.py`](code/ex-75-event-sourcing-audit/example.py). **Observable result**: history answers the audit question. **Design consequence**: fact storage supports explainability. **Key takeaway**: immutable history has operational value.

### Worked Example 76: Domain to integration event

**Context**: Drop internal credit from a published fact. **Artifact**: [`example.py`](code/ex-76-domain-to-integration-event/example.py). **Observable result**: foreign event lacks internal detail. **Design consequence**: crossing contexts does not expose the root. **Key takeaway**: translate events at the boundary.

### Worked Example 77: Aggregate across contexts

**Context**: Shipping references a Sales order id. **Artifact**: [`example.py`](code/ex-77-aggregate-across-contexts/example.py). **Observable result**: shipment stores only foreign identity. **Design consequence**: contexts stay independently deployable. **Key takeaway**: never hold a foreign aggregate object.

### Worked Example 78: Language per context

**Context**: Compare identity and billing accounts. **Artifact**: [`example.py`](code/ex-78-ubiquitous-language-per-context/example.py). **Observable result**: each test asks its own question. **Design consequence**: overloaded words remain local. **Key takeaway**: ubiquitous language is bounded.

### Worked Example 79: Composite business specification

**Context**: Evaluate a discount policy. **Artifact**: [`example.py`](code/ex-79-specification-business-rule/example.py). **Observable result**: delinquency excludes a customer. **Design consequence**: policy is readable and composable. **Key takeaway**: specifications express business logic.

### Worked Example 80: Full DDD model

**Context**: Assemble a root, values, event, and ACL. **Artifact**: [`example.py`](code/ex-80-ddd-domain-model/example.py). **Observable result**: root preserves credit and ACL translates. **Design consequence**: tactical and strategic patterns meet at a protected seam. **Key takeaway**: model the rule first, then integrate across boundaries.
