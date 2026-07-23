# ADR-0004: CI pipeline gate, clean commit history, and product/delivery framing

**Status**: Accepted
**Date**: 2026-07-19

## Context

Pass 1's capstone shipped as a single, complete commit -- appropriate for a Pass-1 deliverable
demonstrating "a working application exists," but not a demonstration of the engineering
WORKFLOW around a change (topic 30): a lint -> test -> build gate, a clean conventional-commit
history distinct from the messy sequence real work produces, and the product/delivery framing
(32/33) that justifies why the change was worth making.

## Decision

- **CI gate**: `ci.yml` (a real, valid GitHub Actions workflow, syntax-checked with
  `actionlint` -- zero findings) defines three sequential jobs: `lint` (`ruff check` +
  `ruff format --check`), `test` (`pytest`), `build` (`python -m compileall app`), each gated on
  the previous (`needs:`) so a lint failure never reaches `test`, and a test failure never
  reaches `build` -- the SAME ordering `scripts/run_ci_locally.sh` runs locally, so a
  contributor sees the identical gate before ever opening a PR.
- **Commit history**: `scripts/build_commit_history_demo.sh` walks this capstone's OWN four
  ordered steps as a clean, Conventional-Commits history in a throwaway scratch repository (not
  nested inside this content tree, to avoid an embedded-git-repo hazard) -- `feat`, `refactor`,
  `perf`, `docs` commits, each independently green. It excerpts REAL, verbatim code from
  `app/domain.py`/`app/ports.py` at a distilled, self-contained scale (no network installs, no
  full FastAPI app) rather than replaying every file this capstone actually ships, so each
  commit is genuinely, quickly re-runnable rather than merely asserted -- the Step 3 commit
  even re-measures its own naive-vs-fast speedup live, each run (see
  `scripts/commit-history-demo-transcript.txt` for one real, captured run: 2.86x, with a
  2.63x-2.92x range observed across five consecutive runs on the same machine).
- **Product/delivery framing**: `docs/product-brief.md` + `docs/delivery-plan.md` state WHY this
  re-engineering was worth doing (topic 32 product judgment) and HOW it was staged and verified
  (topic 33 delivery discipline) -- the same judgment layer Pass 2's Topic 32/33 taught, applied
  to a technical (not product-facing) change.

## Consequences

- **Positive**: `scripts/run_ci_locally.sh`'s bad-commit demonstration (deliberately reintroduce
  a failing test, run the SAME local gate, watch it fail at the `test` stage and never reach
  `build`, then revert) is a genuinely executed transcript, not a described hypothetical --
  mirroring the precedent this plan already established in
  `software-engineering-practices/learning/capstone/code/ci-broken-commit-transcript.txt`: the
  `ruff`/`pytest` output is real; the job-status TABLE alongside it is explicitly a mocked,
  hand-constructed GitHub Actions summary (no live Actions run was triggered for this page).
- **Trade-off**: the "build" stage (`python -m compileall`) is intentionally minimal -- this app
  has no compiled-artifact packaging step; a syntax-compile check is the honest floor for a
  Python HTTP service, matching the same precedent's own choice.

## Verification

`scripts/run_ci_locally.sh` exits 0 against the shipped code (lint clean, 63/63 tests pass,
`compileall` clean); the same script, run against a deliberately reintroduced failing test,
exits non-zero at the `test` stage with `build` never invoked (see this page's Step 4
transcript for both real, captured runs).
