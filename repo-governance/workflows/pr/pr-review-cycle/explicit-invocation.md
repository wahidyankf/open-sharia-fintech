---
description: "Defines the only signals that may start the optional iterative review cycle."
when_to_use: "Use before starting pr-review-cycle."
---

# Explicit Invocation

Start this workflow only when one of these conditions is true:

- The user directly requests `pr-review-cycle` or unmistakably asks for iterative semantic PR
  review with fixing and repetition.
- A plan contains a `pr-review-cycle` step that records the user's explicit request as its source.

No other signal is sufficient. Do not infer invocation from a PR's risk, changed paths, size,
executable behaviour, plans, delivery mode, author, age, or failed/green CI state. Ordinary PRs use
the repository's default exact-head/base PR quality gate without cycle evidence.

Phase 0 still opens no PR, so it cannot run either optional PR-review workflow. At a later delivery
boundary, an explicit request applies to the boundary's complete PR diff. Absence of this workflow
or its records is valid and never blocks plan completion, archival, promotion, or merge.
