# Fix the Class, Not the Sites the Finding Names

A finding cites the occurrences its author happened to read. That is evidence, not an inventory.
How wide the fix goes is the fixer's call, and this is the rule for making it.

A finding naming a stale count or term (e.g. "eight" → "nine") is fixed by a repo-wide grep for
the **old** term, not only the cited files. Fixing just the named occurrences reliably leaves a
contradicting instance in a file the citing specialist never read in full — this has recurred
across cycles. Grep before replying `Fixed`, not after a later cycle rediscovers the miss.

## Why This Is Not Scope Creep

Widening a fix to every site of the **same** defect stays inside the PR — one defect stated in six
files is one problem, and fixing only the cited file leaves the other five contradicting it. Adding
a **different** defect is creep. See
[Scope Guard](../../../../repo-governance/workflows/pr/pr-review-quality-gate/scope-guard-no-scope-creep.md).

## What the Reply Must Say

A reply claiming `Fixed` after a class-wide fix states the grep that was run and how many sites it
touched, so a later cycle can tell a complete fix from a partial one without re-deriving it.
