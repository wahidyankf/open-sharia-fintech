# ERP Conceptual Data Model (Annotated-Concept)

**Course ID**: `erp-conceptual-data-model` · **Format**: Annotated-Concept.

**Scope note**: Models enterprise identities, documents, and facts; it excludes module-specific posting policy. License-aware.

**Short summary**: A durable conceptual model makes cross-module facts linkable and auditable.

## Why this exists · the big idea

- **The problem before the solution**: modules cannot agree without stable identities and relationships.
- **Keep-this-if-you-forget-everything**: model a business fact once, then reference it.

## Prerequisites

- **Prior courses**: `erp-foundations-and-history`.
- **Assumed knowledge**: entities and relationships.

## Accuracy notes

- [Repo-grounded, tech-docs.md] Concepts are original, vendor-neutral modelling guidance.

## Concepts

- **co-01 · business-identity** — a durable key for a party, item, document, or event.
- **co-02 · document-header** — shared context for a business document.
- **co-03 · document-line** — a measurable, attributable detail of that document.
- **co-04 · master-reference** — a controlled link to reusable master data.
- **co-05 · event-linkage** — traceability between intent, execution, and posting.
- **co-06 · effective-date** — temporal meaning attached to a fact.
- **co-07 · ownership-boundary** — the module accountable for a field's lifecycle.
- **co-08 · conceptual-invariant** — rule that survives physical-schema changes.

## In which paths

- `skills/conventional-erp` — Stage A · architecture base.
- `skills/sharia-erp` — Stage A · architecture base.
