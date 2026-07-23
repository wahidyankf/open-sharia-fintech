# ADR-0001: Import the Pass-1 baseline under a green suite; re-engineering goals

**Status**: Accepted
**Date**: 2026-07-19

## Context

Pass 1's `capstone-first-working-software` shipped a working, tested, hardened Habit Tracker
API. It is functionally complete but was built to prove Pass 1's promise (a small working
application), not to demonstrate Pass 2's promise (professional-grade internal structure,
performance discipline, and delivery workflow). Pass 2 taught SOLID + patterns (topic 21),
deliberate paradigm choice + functional core (22/23), safe concurrency (24), algorithmic
complexity (25), `EXPLAIN`-driven SQL tuning (26), and engineering workflow discipline (30),
framed by product/delivery judgment (32/33). This capstone re-engineers the Pass-1 app to
apply all of it, without changing its externally observable behavior.

## Decision

Import the Pass-1 app's baseline (`domain.py`, `models.py`, `auth.py`, `middleware.py`,
`schema_v1.sql`, `migration_v2.sql`) largely unchanged, confirm its test suite is green against
the imported baseline, then evolve it in three further ordered steps (SOLID/functional-core
refactor; concurrency + SQL tuning; workflow wrapping), each verified independently before the
next begins.

## Consequences

- **Positive**: every step has an independently green checkpoint (TDD-style: refactor, verify,
  proceed), so a regression is caught at the step that introduced it, not at the end.
- **Positive**: `auth.py` and `middleware.py` ship byte-identical to Pass 1 -- their correctness
  was already proven there; re-deriving them here would add risk for no benefit.
- **Trade-off**: this ADR set documents DECISIONS, not a full design document -- it is scoped to
  what changed and why, matching topic 30's "ADRs record a decision and its context, not an
  exhaustive spec."

## Verification

The Pass-1 app's OWN, unmodified test suite runs green against the imported baseline before any
Step-2 refactor begins: 34 tests passed (9 unit, 2 property, 23 integration -- the same count
Pass 1's own page documents), `ruff check`/`ruff format --check` clean, `pyright --strict` 0
errors, `pip-audit -l` clean (see this page's Step 1 transcript). The suite grows to 63 tests
only later, as Step 2 adds `test_services.py` and Step 3 adds concurrency/recent-activity
coverage -- this ADR's own scope is the baseline import alone, not the finished suite.
