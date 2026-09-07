---
description: Why the post-mortem convention exists, the core principles it implements, and what it covers versus what it explicitly does not cover
when_to_use: Read this when you need the rationale for post-mortems, or to confirm whether a topic falls inside or outside this convention's scope.
---

# Principles, Purpose, and Scope

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Documentation First](../../../principles/content/documentation-first.md)**: Post-mortems are
  mandatory permanent documentation. Writing them promptly while details are fresh treats
  documentation as a first-class deliverable, not an afterthought.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: The blameless
  framing, "second story" questions, and explicit root cause / contributing factors structure keep
  analysis focused on systemic conditions rather than individual missteps. Each action item must
  address a root cause, not just the proximate trigger.

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**:
  Structured timelines, quantified impact, and severity classification demand that authors
  understand what actually happened before proposing fixes. The retrospective process favors
  reversible, targeted interventions over reflexive procedural changes.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Mandatory frontmatter status, an explicit severity tier, absolute timestamps with stated
  timezone, and typed detection categories make every incident's state and context unambiguous.

## Purpose

Post-mortems serve two purposes:

1. **Learning** — document what actually happened and why decisions made sense at the time, so the
   team builds accurate mental models of its systems.
2. **Improvement** — convert that learning into concrete, owned, prioritized action items that
   reduce the probability or impact of similar incidents.

A post-mortem is not a punishment mechanism. It is a systems-thinking tool applied retrospectively.

## Scope

### What This Convention Covers

- Location and filename rules for post-mortem documents
- The blameless culture standard
- Mandatory and optional sections (in order)
- Severity scale definition (authoritative)
- Action-item table structure and tracking
- `doc_status` lifecycle
- Timing expectation
- Security constraints (no secrets)
- Diagram guidance

### What This Convention Does NOT Cover

- Incident response procedures during an active outage (those belong in operational runbooks)
- On-call rotation or escalation policies
- Post-mortem review meeting facilitation
- Plan content structure (see [Plans Organization](../plans.md))
- **The decision of WHEN a plan-execution learning becomes a post-mortem** — that routing decision
  belongs to the [Knowledge Capture Convention](../../../development/quality/knowledge-capture.md)'s
  open-ended triage matrix, which routes a failure/incident learning here by cross-reference. This
  convention remains the single source of truth for post-mortem structure and content once a learning
  is routed; it does not duplicate the triage rubric.
