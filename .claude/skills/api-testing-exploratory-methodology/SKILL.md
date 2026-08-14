---
name: api-testing-exploratory-methodology
description: Complete methodology for spec-aware, contract-aware session-based exploratory testing of a live REST or GraphQL API — inputs, relationships, non-destructive constraint, charter/tour/SFDIPOT methodology, test dimensions, mandatory systematic sweeps, driving the API, contract-and-specs ground truth, defect anatomy, and output modes. Backs the api-exploratory-tester agent.
---

# API Testing: Exploratory Methodology

Methodology for hunting contract-conformance, functional, edge-case, auth, and consistency defects on
a **running** REST or GraphQL API — the API-surface counterpart to the web tester triad.

## Reference Modules

1. [Why, Inputs, Relationships, Non-Destructive](reference/01-why-inputs-relationships-nondestructive.md)
2. [Session-Based Methodology](reference/02-session-based-methodology.md) — charters, tours, SFDIPOT,
   CRUSSPIC STMPL.
3. [Test Dimensions Checklist](reference/03-test-dimensions-checklist.md) — contract conformance,
   status codes, error envelopes, edge cases, auth, consistency, pagination, idempotency, GraphQL,
   performance, security.
4. [Mandatory Systematic Sweeps](reference/04-mandatory-sweeps.md) — operation × property matrix,
   convention round-trip, declared-invariant conformance, self-completeness check.
5. [Driving the API and Ground Truth](reference/05-driving-and-ground-truth.md) — how to drive curl/
   GraphQL, contract-and-specs comparison, spec-gap detection.
6. [Defect Anatomy and Severity](reference/06-defect-anatomy-and-severity.md) — `AET-###` anatomy,
   severity/priority scales.
7. [Output Modes and Procedure](reference/07-output-modes-and-procedure.md) — the three output modes,
   procedure summary, quality guidelines, constraints.

## Core Principles

- **Enumerate, never sample** — the mandatory sweeps cover every operation, not a spot check.
- **Cite the contract or spec, never a vibe** — every "expected" quotes an OpenAPI clause, SDL type,
  or `.feature` scenario.
- **Non-destructive by default** — read-only unless per-run authorized; redact every credential.

## Related Skills

- `web-testing-exploratory-methodology` — rendered-UI counterpart (disjoint surface).
- `plan-creating-project-plans`, `plan-writing-gherkin-criteria`, `docs-applying-content-quality`.
