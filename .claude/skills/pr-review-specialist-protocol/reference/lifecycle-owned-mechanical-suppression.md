# Lifecycle-Owned Mechanical Suppression

## PR Quality-Gate Invocation

Consume `{step0.outputs.delegated-gate-ids}` and its lifecycle evidence ledger before reviewing.
Suppress only a predicate owned by an exact registry ID or its declared `verifies` relationship.
Do not rerun, tool-verify, or AI-rederive that predicate. Exact current repository/head and
applicable-base green aggregate PR CI is `verified`; missing, mismatched, or stale evidence is
`pending`, not a finding and not a fallback check. A relevant fixer edit invalidates only affected
evidence until current-head CI replaces it.

Continue semantic review, including behavioural correctness, architecture, security, test
integrity, performance, documentation meaning, instruction decay, and type soundness. Continue
surface-conditional runtime/manual tester gates; they are not substitutes for registered lifecycle
checks.

## Standalone Invocation

Without the quality-gate delegation handoff, retain each specialist's existing charter and
SUPPRESS block. Continue suppressing purely mechanical failures ordinarily caught by configured
compiler/build, lint/format, link/diagram/naming, spec-presence, or boundary gates; standalone
instructions may run read-only checks as evidence. Do not infer delegated ownership or weaken
semantic review from this module.
