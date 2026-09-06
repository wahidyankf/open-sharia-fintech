# Lifecycle Delegation

In `rules-quality-gate`, remove every finding owned by an exact `delegated-gate-ids` entry or its
declared `verifies` relationship. Do not rerun its check to confirm the skip. Missing/stale evidence
is `pending`, not fixer work. After edits, intersect changed files with delegated scopes and return
a ledger invalidating only affected evidence. Standalone fixing retains the complete protocol.
