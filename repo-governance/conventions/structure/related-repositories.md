---
title: "Related Repositories Convention"
description: Defines the OSE parity pair, independent-repository boundaries, required awareness surfaces, and propagation scope.
when_to_use: Use when adding or changing a cross-repository reference, shared boundary, consumer integration, or propagation obligation.
category: explanation
subcategory: conventions
tags:
  - cross-repository
  - parity
  - structure
  - governance
---

# Related Repositories Convention

Repository awareness helps contributors route work without turning every named repository into a
sync target. This convention separates parity, consumption, and knowledge-sharing relationships.
The descriptive catalogue is [Related Repositories](../../../docs/reference/related-repositories.md).

## OSE parity pair

The OSE parity set contains exactly `ose-public` and `ose-private`. Public is the canonical source
for portable governance, agent, skill, workflow, and Rhino changes; private receives those changes
through an explicit sibling obligation in its own delivery. Private-only operations, licensing
exceptions, and CI constraints remain local and must be recorded as divergences.

The `apps/rhino-cli` implementation and shared Rhino Gherkin boundary stay byte-identical across the
pair. Each repository's parity manifest proves only its own tracked boundary, so convergence also
requires a direct byte comparison between repositories. A green local manifest never proves sibling
equality by itself.

## Independent repositories

[HIPPO](https://github.com/wahidyankf/hippo) is an independent MIT-licensed upstream tool. OSE may
consume a checksum-pinned HIPPO release and maintain consumer-specific configuration, mappings, and
tests. HIPPO source, behavior specifications, generic tests, and release automation remain upstream;
they must not be copied, vendored, or forked into an OSE repository.

[BeaverNest](https://github.com/wahidyankf/beaver-nest) is an independent MIT-licensed product.
Useful learnings may inform OSE, but neither repository automatically receives the other's product,
governance, agent, skill, workflow, or tool changes.

Naming an independent repository creates navigation, not parity. No OSE parity gate, propagation
workflow, or byte-identity manifest may silently widen to include one.

## Required awareness surfaces

Both OSE repositories maintain these touchpoints:

- `AGENTS.md` names the parity sibling and independent repositories that contributors must know
  before routing work.
- `README.md` gives readers a short relationship summary and links to the descriptive catalogue.
- `docs/reference/related-repositories.md` records each named repository's visibility, license,
  role, ownership boundary, and correct starting point.
- This convention owns normative parity, propagation, and consumer-boundary rules. Descriptive
  documents link here instead of creating another canonical rule.

Catalogue only relationships OSE contributors need for durable routing. A one-off compatibility
test or shared tool invocation does not, by itself, create an OSE repository relationship.

## Change and validation procedure

When a relationship changes:

1. Classify it as parity, upstream consumption, knowledge sharing, or no durable relationship.
2. Update the canonical convention before its instruction and descriptive touchpoints.
3. Record a sibling obligation only for portable public-to-private propagation.
4. Validate instruction budgets, annotated indexes, Markdown links, and governance consistency.
5. For Rhino changes, validate both local manifests and compare the two tracked boundaries directly.

Structural placement is covered by repository-rules, index, link, and parity checks. Routing a novel
work item remains **unenforced by decision** because it requires human product and ownership
judgment; the catalogue supplies the evidence for that decision.

## Principles Implemented/Respected

- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) — parity,
  upstream ownership, and independent-product boundaries are stated directly.
- [Documentation First](../../principles/content/documentation-first.md) — contributors can discover
  repository relationships from committed entry points.
- [Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md) — one canonical
  convention owns the rules while one reference catalogue serves readers.
