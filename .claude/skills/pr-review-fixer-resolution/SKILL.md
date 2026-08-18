---
name: pr-review-fixer-resolution
description: How pr-review-fixer enumerates unresolved GitHub PR review threads, triages each into fix/reject/defer/clarify, applies the outcome, and resolves only what was genuinely addressed. Use when resolving threads posted by pr-review-synthesis-maker's consolidated review.
when_to_use: When acting as pr-review-fixer in the PR-Review Maker→Fixer Cycle — enumerating unresolved review threads, deciding a triage outcome, posting a reply, or deciding whether to resolve a thread.
---

# PR Review Fixer Resolution

## Overview

`pr-review-fixer` is the fixer half of a fan-out→synthesize→fixer loop: it never discovers
findings itself, only resolves what the nine discipline specialists and
`pr-review-synthesis-maker` already posted as GitHub review threads.

## Reference Modules

- [01-thread-enumeration-and-api-gotchas.md](./reference/thread-enumeration-and-api-gotchas.md) —
  GraphQL enumeration query, and three confirmed live-API gotchas (pull_number requirement, `-F`
  vs `-f`, zsh 1-indexed loops)
- [02-four-way-triage.md](./reference/four-way-triage.md) — the fix / reject / defer / clarify
  decision table and each path's requirements
- [03-reply-resolve-discipline.md](./reference/reply-resolve-discipline.md) — hard rules for
  when a thread may actually be resolved, plus repeated-finding handling across cycles
- [04-identity-and-quality-gates.md](./reference/identity-and-quality-gates.md) — posting
  identity/write-scope stopgap, and the mandatory pre-push gate re-run

## Core Principles

1. **Reply to every unresolved thread** — zero threads may leave a fixer pass both unresolved and
   untouched.
2. **Resolving is a higher bar than replying** — only fixed threads (committed AND pushed,
   verified against the PR's own head) or well-founded rejections get resolved.
3. **A stale term/count fix requires a repo-wide grep**, not just the cited occurrence — this
   class of miss has recurred across dogfood cycles.
4. **Never push a fix that breaks a previously-green gate** — re-run relevant quality gates before
   every push.

## Related Agents

`pr-review-synthesis-maker` (posts the consolidated review this agent resolves),
`pr-review-scout-maker` (pipeline stage 0), the nine `pr-review-*-maker` discipline specialists.
