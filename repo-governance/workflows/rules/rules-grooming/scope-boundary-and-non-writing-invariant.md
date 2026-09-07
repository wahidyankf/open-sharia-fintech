---
title: "Scope Boundary and the Non-Writing Invariant"
description: The three admitted candidate classes, the reductions explicitly refused, and why this workflow hands every edit to rules-propagation instead of writing.
when_to_use: Use when checking whether a proposed reduction is in scope, or why this workflow does not write.
---

# Scope Boundary and the Non-Writing Invariant

## The Three Admitted Classes

A candidate is admissible only as one of these. The class determines its semantic risk, and
therefore its ranking and its approval path.

1. **Fragmentation overhead** — representation cost created by splitting, not by content. A shard
   whose parent has budget headroom to reabsorb it; a shard folder holding a single child; an index
   entry longer than the document it points at; frontmatter keys beyond those a consumer actually
   reads. Merging these changes no obligation, so the class carries **zero** semantic risk.
2. **Cross-surface duplication** — one obligation stated on two or more surfaces without a recorded
   keep rationale. The reduction keeps the canonical home and replaces the rest with `See` links.
   Risk is **low but non-zero**: the link target must already cover every case the removed text
   covered, per forbidden anti-fix 4.
3. **Retirement** — a rule whose subject no longer exists, that a later rule supersedes in fact but
   not in text, or that no surface reaches. This is the only class that removes an obligation, so
   it is opt-in via the `classes` input and gated per item at Step 5.

## Refused Reductions

These are out of scope permanently, not merely deprioritized:

- **Rewriting prose to save words.** Forbidden anti-fix 2. Grooming never paraphrases, tightens, or
  densifies a rule's wording.
- **Weakening a qualifier.** Propagation's semantic-preservation hard gate binds every hand-off:
  audience qualifiers, scope boundaries, exceptions, pass conditions, and violation conditions
  survive verbatim enough to remain unambiguous.
- **Trimming a safety guardrail.** Secrets and `.env` rules, the Git Identity Guardrail, and
  environment-branch rules are never candidates in any class.
- **Raising a word budget.** Never, for any reason, in any class.
- **Deleting a rule to make room.** Forbidden anti-fix 1. Retirement removes a rule that no longer
  binds; it is never a capacity measure.

## The Non-Writing Invariant

Propagation is the sole writer of every rule edit, and grooming does not become an exception to
that by having found the edit itself. Grooming produces a manifest; propagation writes.

Three things follow, and each is a reason the split is worth its cost:

- **Conflict scanning stays pre-write.** Propagation scans for contradictions under layer-aware
  precedence before it writes. A grooming merge that would collide with a higher-layer rule is
  caught by the same scan that catches an authored one, rather than by a second mechanism that
  would have to be kept in step with it.
- **Enforcement dispositions stay recorded.** Every rule edit carries one of propagation's three
  dispositions. Reductions are rule edits, so they carry one too.
- **The workflow graph stays acyclic.** Grooming calls propagation; propagation never calls
  grooming. Neither calls the quality gate.

The cost is real — a large sweep becomes many propagation deliveries rather than one — and Step 6
batches by subject to contain it. The invariant is not traded away for that convenience.
