# PR-review bot identity (restore `REQUEST_CHANGES`)

One-line summary: give `pr-review-synthesis-maker` a dedicated posting identity so blocking reviews
land with a real `REQUEST_CHANGES` STATE instead of a plain `COMMENT`.

> De-promoted 2026-07-21 from a full backlog plan (full detail preserved in git history).

## Problem / context

`pr-review-synthesis-maker` structurally cannot post a `REQUEST_CHANGES` review: `gh` authenticates as the PR
author under the repo's current identity posture, and GitHub rejects `REQUEST_CHANGES` on one's own
pull request. So every blocking review — even one carrying a CRITICAL finding — lands with GitHub
review STATE `COMMENT`, and GitHub's own "changes requested" signal never fires. Any consumer that
gates on review STATE (branch-protection rules, dashboards, future automation) reads a blocked PR as
unblocked while a CRITICAL finding sits open on it. The current mitigation is documentation-only:
blocking status is carried in the finding's severity label in the comment body, and consumers are told
to parse severity from text rather than trust STATE — recorded in `pr-review-quality-gate.md` and
`.claude/agents/pr-review-synthesis-maker.md`. A documented workaround is not a fixed gate. Surfaced
during the
`parallel-orchestration-shared-machine-governance` Knowledge Capture phase.

## Why now

The review cycle is the default gate for every `*-to-pr` delivery, so this blind spot is exercised
on every PR. The longer STATE stays untrustworthy, the more automation gets built to parse severity
from comment text — accreting workaround dependence that a later fix then has to unwind.

## Prior art / precedents

- **GitHub Apps** — first-class bot identities that authenticate with least-privilege scopes, the
  mechanism for giving the reviewer its own posting identity.
  [github apps](https://docs.github.com/en/apps/overview)
- **PR-Review Quality Gate workflow** — the maker→fixer cycle where the untrustworthy review STATE
  is currently worked around in text.
  [pr-review-quality-gate](../../repo-governance/workflows/pr/pr-review-quality-gate.md)
- **pr-review-synthesis-maker agent** — the coordinator that posts the consolidated review and
  structurally cannot post `REQUEST_CHANGES` today; would be rewired to the new identity.
  [pr-review-synthesis-maker](../../.claude/agents/pr-review-synthesis-maker.md)
- **Git Identity Guardrail** — the repo rule scoping this to `gh`/API posting identity, distinct
  from commit-push identity. [AGENTS.md](../../AGENTS.md)

## Proposed direction (sketch)

- Provision a dedicated GitHub App or CI-scoped bot identity with minimal write scope: create review,
  reply to review comment, resolve review thread — nothing broader.
- Wire `pr-review-synthesis-maker` to authenticate as that identity so `REQUEST_CHANGES` becomes
  available for blocking findings.
- Reinstate `REQUEST_CHANGES` in the workflow and agent definitions and remove the
  parse-severity-from-text workaround language once STATE is trustworthy.
- Decide whether the AI-attribution footer stays once a distinct identity makes authorship
  self-evident.

## Rough scope & non-goals

In scope: the posting identity, the coordinator rewiring, and the workaround removal.

Out of scope (for now): `pr-review-fixer`'s commit-push identity — governed by the Git Identity
Guardrail and a separate concern from `gh`/GitHub-API posting identity.

## Risks & open questions

- Requires an org-level GitHub App installation or a CI-scoped token — an infrastructure action
  outside the code repos. Confirm availability before scheduling. (blocking dependency)
- The identity must be scope-minimal: an identity provisioned with broad repo-write would satisfy the
  `REQUEST_CHANGES` requirement while quietly granting far more than review posting — a push attempt
  with its token must be rejected.

## What success looks like + promotion signal

Success: a review containing a CRITICAL/HIGH finding submits with STATE `REQUEST_CHANGES`, a
findings-only-MEDIUM/LOW review stays `COMMENT`, and the identity's token cannot push to a branch.
Ready to re-promote to a `backlog/` plan once the org confirms a GitHub App installation or CI-scoped
token is available — the infrastructure dependency is the gate, not the wiring.
