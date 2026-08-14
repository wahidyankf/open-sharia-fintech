---
title: "Beginner Examples"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 10
---

## Language, values, entities, and simple domain behaviour

Run each complete, annotated artifact with `python3 example.py` from its directory. The artifact
is the code portion of each example; its assertions provide the observable result.

### Worked Example 1: Ubiquitous language rename

**Context**: Replace generic workflow names with booking language. **Artifact**: [`example.py`](code/ex-01-ubiquitous-language-rename/example.py). **Observable result**: `confirm()` produces a confirmed booking. **Design consequence**: tests can read as business sentences. **Key takeaway**: name behaviour after the domain.

### Worked Example 2: Model versus table

**Context**: Give an order a placement rule. **Artifact**: [`example.py`](code/ex-02-model-vs-table/example.py). **Observable result**: a positive order can place. **Design consequence**: rules do not leak into SQL-shaped callers. **Key takeaway**: model behaviour, not rows.

### Worked Example 3: Value-object equality

**Context**: Compare money by amount and currency. **Artifact**: [`example.py`](code/ex-03-value-object-equality/example.py). **Observable result**: equal values compare equal. **Design consequence**: no synthetic identity is needed. **Key takeaway**: values are interchangeable by attributes.

### Worked Example 4: Value-object immutability

**Context**: Freeze a valid money value. **Artifact**: [`example.py`](code/ex-04-value-object-immutable/example.py). **Observable result**: assignment raises `FrozenInstanceError`. **Design consequence**: callers cannot corrupt a shared value. **Key takeaway**: replace values; do not mutate them.

### Worked Example 5: Value-object behaviour

**Context**: Add money without side effects. **Artifact**: [`example.py`](code/ex-05-value-object-behaviour/example.py). **Observable result**: addition returns a new value. **Design consequence**: the operands remain safe to share. **Key takeaway**: value behaviour is side-effect free.

### Worked Example 6: Entity identity

**Context**: Track a customer through a name change. **Artifact**: [`example.py`](code/ex-06-entity-identity/example.py). **Observable result**: matching ids compare as one customer. **Design consequence**: identity, not attributes, supplies continuity. **Key takeaway**: entities are defined by id.

### Worked Example 7: Entity mutable state

**Context**: Change a customer's email. **Artifact**: [`example.py`](code/ex-07-entity-mutable-state/example.py). **Observable result**: the id remains stable. **Design consequence**: a named transition documents why state changed. **Key takeaway**: entities can evolve without becoming new entities.

### Worked Example 8: Entity versus value choice

**Context**: Contrast `Customer` and `Address`. **Artifact**: [`example.py`](code/ex-08-entity-vs-value-choice/example.py). **Observable result**: addresses compare by value while customers expose ids. **Design consequence**: equality reflects domain meaning. **Key takeaway**: choose identity only when continuity matters.

### Worked Example 9: Constructor invariant

**Context**: Reject unsupported currencies. **Artifact**: [`example.py`](code/ex-09-invariant-in-constructor/example.py). **Observable result**: invalid construction raises. **Design consequence**: invalid money cannot travel. **Key takeaway**: make impossible values unconstructable.

### Worked Example 10: Guard method invariant

**Context**: Prevent an overdraft. **Artifact**: [`example.py`](code/ex-10-invariant-guard-method/example.py). **Observable result**: failed withdrawal preserves balance. **Design consequence**: callers cannot reach an invalid state. **Key takeaway**: validate before mutation.

### Worked Example 11: Full money value object

**Context**: Keep unit and arithmetic together. **Artifact**: [`example.py`](code/ex-11-money-value-object/example.py). **Observable result**: mixed currencies raise. **Design consequence**: arithmetic cannot discard its unit. **Key takeaway**: put value invariants beside value behaviour.

### Worked Example 12: Email value object

**Context**: Validate contact data at its boundary. **Artifact**: [`example.py`](code/ex-12-email-value-object/example.py). **Observable result**: malformed input raises. **Design consequence**: services receive a trustworthy type. **Key takeaway**: validate at construction.

### Worked Example 13: Quantity value object

**Context**: Forbid negative quantities. **Artifact**: [`example.py`](code/ex-13-quantity-value-object/example.py). **Observable result**: `Quantity(-1)` raises. **Design consequence**: stock code needs fewer defensive checks. **Key takeaway**: preserve domain units explicitly.

### Worked Example 14: Date range value object

**Context**: Require start before end. **Artifact**: [`example.py`](code/ex-14-daterange-value-object/example.py). **Observable result**: inverted ranges raise. **Design consequence**: later scheduling rules rely on a valid interval. **Key takeaway**: encode relational invariants in the value.

### Worked Example 15: Value-object composition

**Context**: Build a line from meaningful values. **Artifact**: [`example.py`](code/ex-15-value-object-composition/example.py). **Observable result**: a line calculates its total. **Design consequence**: primitive parameters no longer obscure intent. **Key takeaway**: compose values into richer domain expressions.

### Worked Example 16: Entity lifecycle

**Context**: Restrict order status transitions. **Artifact**: [`example.py`](code/ex-16-entity-lifecycle/example.py). **Observable result**: draft becomes placed then shipped. **Design consequence**: illegal paths have no operation. **Key takeaway**: model state transitions by domain verbs.

### Worked Example 17: Self-validating entity

**Context**: Reject shipping before placement. **Artifact**: [`example.py`](code/ex-17-self-validating-entity/example.py). **Observable result**: the command raises. **Design consequence**: callers cannot bypass lifecycle policy. **Key takeaway**: the entity owns its transition preconditions.

### Worked Example 18: Ubiquitous-language test

**Context**: Make a test name state a credit rule. **Artifact**: [`example.py`](code/ex-18-ubiquitous-language-test/example.py). **Observable result**: over-limit spending fails. **Design consequence**: domain experts can review intent. **Key takeaway**: tests are part of the shared language.

### Worked Example 19: No primitive obsession

**Context**: Replace a bare string with `CustomerEmail`. **Artifact**: [`example.py`](code/ex-19-no-primitive-obsession/example.py). **Observable result**: invalid emails fail at input. **Design consequence**: deeper logic receives valid concepts. **Key takeaway**: a type can carry meaning and rules.

### Worked Example 20: Simple factory

**Context**: Register a valid customer. **Artifact**: [`example.py`](code/ex-20-factory-simple/example.py). **Observable result**: the factory returns a usable entity. **Design consequence**: creation policy has one home. **Key takeaway**: use a factory when creation has a domain rule.

### Worked Example 21: Aggregate factory

**Context**: Create an order with an initial line. **Artifact**: [`example.py`](code/ex-21-factory-aggregate/example.py). **Observable result**: no empty aggregate escapes. **Design consequence**: callers cannot forget required children. **Key takeaway**: factories assemble valid aggregate starts.

### Worked Example 22: Domain-service transfer

**Context**: Move funds between accounts. **Artifact**: [`example.py`](code/ex-22-domain-service-transfer/example.py). **Observable result**: both balances change only after validation. **Design consequence**: neither root pretends to own a two-root rule. **Key takeaway**: use a stateless service for cross-entity logic.

### Worked Example 23: Domain service versus method

**Context**: Check shared ownership of two accounts. **Artifact**: [`example.py`](code/ex-23-domain-service-vs-method/example.py). **Observable result**: the service uses both identities. **Design consequence**: no arbitrary object receives foreign responsibility. **Key takeaway**: put rules where their information naturally meets.

### Worked Example 24: Anemic versus rich model

**Context**: Let `RichOrder` total its own lines. **Artifact**: [`example.py`](code/ex-24-anemic-vs-rich/example.py). **Observable result**: the root returns its total. **Design consequence**: services do not pull raw data to recompute rules. **Key takeaway**: keep behaviour with the data it needs.

### Worked Example 25: Fix an anemic model

**Context**: Move line validation into `Order`. **Artifact**: [`example.py`](code/ex-25-anemic-antipattern-fix/example.py). **Observable result**: nonpositive prices raise. **Design consequence**: application code only coordinates. **Key takeaway**: move leaked policy back to the root.

### Worked Example 26: Specification predicate

**Context**: Name a premium-customer rule. **Artifact**: [`example.py`](code/ex-26-specification-predicate/example.py). **Observable result**: sample spends pass or fail. **Design consequence**: a rule becomes reusable. **Key takeaway**: reify important predicates.

### Worked Example 27: Specification composition

**Context**: Combine premium and active rules. **Artifact**: [`example.py`](code/ex-27-specification-compose/example.py). **Observable result**: both conditions must hold. **Design consequence**: policy remains readable as logic. **Key takeaway**: compose rules instead of duplicating branches.

### Worked Example 28: Specification selection

**Context**: Select premium spends. **Artifact**: [`example.py`](code/ex-28-specification-select/example.py). **Observable result**: qualifying values remain. **Design consequence**: selection depends on a domain predicate. **Key takeaway**: pass named policy into collection operations.
