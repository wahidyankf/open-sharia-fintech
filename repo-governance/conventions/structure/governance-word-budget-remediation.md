---
title: "Governance Word-Budget Remediation"
description: Enforcement-point detail, the progressive-disclosure fix, and forbidden anti-fixes for the word-budget gate
when_to_use: Use when a file fails the word-budget gate and you need the remediation steps.
category: explanation
subcategory: conventions
tags:
  - instruction-files
  - word-budget
  - governance
  - progressive-disclosure
created: 2026-08-13
---

# Governance Word-Budget Remediation

Detail split out of the
[Governance Word-Budget Convention](./governance-word-budget.md) so that doc fits its own
word ceiling (progressive disclosure applied to itself).

## Enforcement Points

1. **Pre-push (primary)**: `.husky/pre-push` runs `governance word-budget validate`, gated on
   changed paths touching a monitored surface.
2. **PR quality gate (CI)**: `npx nx run rhino-cli:governance-word-budget:validation` runs on every
   PR and push to `main`.
3. **Deterministic preflight**: `rhino-cli repo-governance audit` includes the category alongside
   `layer-coherence`, `traceability-audit`, and `vendor-audit`, so `repo-rules-checker` consumes the
   findings rather than re-deriving them.

No pre-commit surface is declared for this gate (FR-1.14): a whole-tree scan on every commit buys
no additional coverage over the pre-push/CI enforcement points above, and
`rhino-cli convention audit` (`apps/rhino-cli/src/commands/convention_audit.rs`) does not include a
word-budget member.

## When the Gate Fails

**The only sanctioned remediation is progressive disclosure.** Replace inline-expanded content with
a one-line summary and a `See` link to its canonical home. The detail stays fully reachable, just
no longer inlined.

**Naming the shards.** A shard is not a step, so its filename carries **no** ordinal; the parent
index carries order. See [Ordinal Filename Prefixes](./ordinal-filename-prefixes.md).

### Forbidden Anti-Fixes

1. **Delete a rule** — removes coverage; rules must stay reachable.
2. **Compress to dense prose** — stripping line breaks hurts both agent and human readability.
3. **Split into another auto-loaded file** — moves words without shrinking the resolved-tree total,
   and may exceed a per-file harness limit.
4. **Point at an incomplete target** — a `See` link to a table or section that omits cases the
   inline text covered is rule deletion in disguise. Diff the target against ground truth before
   replacing an enumeration with a link — text search cannot find omissions. When the target is
   incomplete: complete it first, or restate the inline rule as a **pattern** rather than an
   enumeration (e.g. "every `prod-*`/`stag-*` ref is a deploy target" instead of listing them),
   which is both shorter and immune to new entries appearing. See
   [Anti-Pattern 10: Enumeration-Based Guards](../../development/agents/anti-patterns/07-anti-pattern-10-enumeration-based-guards.md#anti-pattern-10-enumeration-based-guards-denylist-guards-that-fail-open).

**Never compress a safety guardrail to save words.** Secrets/`.env` rules, the Git Identity
Guardrail, and environment-branch rules trim **last and only via a complete target** — never by
dropping cases or dense-prose compression.

If none of the above applies, open a plan requesting a threshold adjustment with a documented
rationale and harness-source citation.

## Vision Supported

Serves the [Open Sharia Enterprise Vision](../../vision/open-sharia-enterprise.md) the same way its
parent convention does: reliable instruction delivery across the multi-harness agent ecosystem.

## Principles Implemented/Respected

- **[Progressive Disclosure](../../principles/content/progressive-disclosure.md)**: this document
  is itself an application of the principle — detail split from its parent to respect a word
  ceiling.

## Related Conventions

- [Governance Word-Budget Convention](./governance-word-budget.md) — thresholds and monitored
  surfaces
- [Ordinal Filename Prefixes](./ordinal-filename-prefixes.md) — naming split shards
