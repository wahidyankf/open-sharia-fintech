---
description: How the cost/benefit bar scales with a change's blast radius, and the enforcement disposition for the code-as-liability practice.
when_to_use: Use when judging how much justification a specific addition needs, or when asking how this practice is enforced.
---

# Scrutiny and Enforcement

## Scrutiny Scales With Blast Radius

The bar rises with how many projects depend on the code and how long it will live.

| Blast radius                                   | Bar                                          |
| ---------------------------------------------- | -------------------------------------------- |
| A script used once and deleted                 | Nearly free; a sentence is plenty            |
| Code inside one project, called from one place | Ordinary; the three answers, briefly         |
| A shared library other projects import         | High; name the callers that will inherit it  |
| Tooling every project's gates run through      | Highest; justify against not doing it at all |

The current highest-scrutiny surface is the repository's shared CLI tooling, because every project's
quality gates run through it — every line added there is a line all of them now depend on. That is
an observation about today's dependency graph, not a fixed list; the bar follows the blast radius
wherever it moves.

Scrutiny scales the _depth_ of the answer, never whether one is owed. A one-line addition to shared
tooling still owes all three answers.

## Enforcement Disposition

**Gated, pending implementation.**

The pull request template carries the section, so the prompt is unavoidable and review-time
enforcement has something concrete to point at. Governance-conformance review already reads
documented practices in `repo-governance/`, so this practice is picked up without a new reviewer
charter.

A mechanical check — the section present and non-empty whenever a diff adds non-test lines under
`apps/`, `libs/`, or `scripts/` — is possible and filed as tooling work. Building it is itself an
addition governed by this practice, and waits until review-time enforcement is shown to be
insufficient.

## Related Documents

- [The Obligation](./the-obligation.md) — the three answers whose depth this scales.
- [What Counts as Code](./what-counts-as-code.md) — the in-scope surfaces.
