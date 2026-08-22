---
title: "PR-Review Quality Gate — Scope Guard: The Loop Never Widens the PR"
description: "Binds every pipeline stage to the PR's stated problem so review cycles cannot grow the change they review."
when_to_use: "Use when judging whether a finding, or the fix it asks for, belongs in this PR."
---

# Scope Guard: The Loop Never Widens the PR

A review cycle exists to make **this** change correct, never bigger. Left unbound, the loop grows
the PR it reviews: each cycle finds adjacent improvements, the fixer applies them, the next cycle
reviews the enlarged diff and finds more. The PR stops converging, and
[Bounding PR Size](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-pr-size.md)
is breached by the mechanism meant to protect quality.

## The Anchor

Scope is the **problem the PR body states**, together with the **non-goals it declares** — see
[What Every PR Body Must Carry](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-pr-body.md) —
plus the linked plan or issue when one exists. Both halves are mandatory precisely so this guard
has something falsifiable to test against. A PR with no stated problem has no defensible scope,
and a declared non-goal settles the question outright: a finding asking for it is out of scope by
the author's own record, not by the fixer's judgment.

**Asking is in charter.** When scope is absent, vague, or contradicted by the diff, any reviewer
may raise it — as a `clarify` finding against the body. It is answered by editing the body, and
the corrected statement binds the rest of the loop. Reviewers are never obliged to infer a
boundary the author did not draw.

**The test**: does fixing this finding serve the stated problem, or does it add a second one? The
second is scope creep, however worthwhile it is on its own.

## Binding at Three Stages

- **Specialists** — do not raise a finding whose only remedy is work the PR never set out to do.
  An adjacent improvement is not a defect in this PR.
- **`pr-review-synthesis-maker`** — drop scope-widening findings in the reasonableness filter. The
  coordinator never manufactures new scope during synthesis.
- **`pr-review-fixer`** — a fix that would widen the PR is `defer`, never `fix`, whatever its
  merit. Reply with the scope reason and file it as a follow-up.

**Fixing the whole class is not creep.** One defect stated in six files is one problem, and a fix
touching only the cited file leaves the rest contradicting it. Widening a fix to every site of the
*same* defect stays in scope; adding a *different* defect does not.

## The One Exception

**A defect this PR introduces is always in scope**, however far it sits from the stated problem.
The guard bounds *additions* to the problem, never *consequences* of the change under review.
Without this carve-out the guard becomes a shield: "out of scope" would excuse a regression the
PR itself caused.

## Enforcement

None automated. The guard binds the three agents above, and a violation is visible as a diff that
grew across cycles without a finding requiring it.
