# Product brief: re-engineer the Habit Tracker into a professional core

**Author**: capstone-solid-core (Pass-2 boundary)
**Date**: 2026-07-19

## Problem

Pass 1's Habit Tracker works, is tested, and is hardened -- but it was built to prove "a small
working application," which is a different bar than "a codebase a team could keep growing for a
year without it rotting." Two concrete symptoms, found by reading the Pass-1 code with a
professional eye rather than a "does it work" eye:

- The database module (`repository.py`) is the ONLY thing standing between `HabitService`-shaped
  business rules and SQLite -- but there IS no `HabitService`; route handlers call the database
  module directly, so a business rule (e.g., "a check-in needs an owned habit") is only
  discoverable by reading a route handler, not a named, independently testable unit.
- A genuinely useful feature -- "show me my recent activity across every habit" -- would, if
  added the same way Pass 1's endpoints were added, require an unindexed join-plus-sort that
  gets slower as check-in history grows, with no plan to catch that before it ships.

## Who this is for

Any engineer who inherits this codebase next: the reader of this capstone, standing in for a
teammate six months from now who needs to add a feature without first reverse-engineering which
module owns which rule.

## What "done" looks like

- The Pass-1 app's existing behavior is UNCHANGED (same endpoints, same responses, same
  security properties) -- a re-engineering, not a rewrite. Verified by the full inherited test
  suite passing unmodified in spirit.
- A NEW variation (an alternate `HabitRepository`) can be added without editing any existing
  shipped class -- verified directly by `tests/test_services.py`.
- One genuinely slow path is now provably faster, with the "provably" backed by a repeatable
  benchmark script, not a one-time claim.
- A contributor opening a PR against this code sees the exact same lint -> test -> build gate CI
  would enforce, before they ever push.

## What this explicitly does NOT do

- Does not add new user-facing features beyond the one activity-feed endpoint the SQL-tuning
  story needed to be genuine (topic 26 requires a REAL slow-query story, not a synthetic one).
- Does not migrate the database engine (stays SQLite, matching Pass 1's zero-manual-steps
  follow-along design -- DD-30) -- the EXPLAIN-guided-index technique is applied to this app's
  actual engine, documented explicitly where it differs from topic 26's PostgreSQL teaching
  engine (see ADR-0003).

## Success metric

Every claim on this capstone's page is independently reproducible by a reader on a clean
machine: the test suite, the three benchmark scripts, and the CI-gate demonstration all produce
the SAME shape of result the page shows (exact timing numbers will vary by machine; the
DIRECTION of each result -- OCP holds, the O(n) algorithm variant is faster once tuned, the
denormalized query plan drops the temp b-tree, the CI gate blocks a bad commit -- should not).
