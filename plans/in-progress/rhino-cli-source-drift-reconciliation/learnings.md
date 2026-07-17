# Learnings — rhino-cli Source-Drift Reconciliation

> Scaffold per the [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md).
> Capture learnings as they surface during execution; triage each to a home (convention, doc,
> `plans/ideas.md`) or discard in Phase 5.

## Per-file canonical decisions (Phase 1)

_(populate during Phase 1 — one entry per drifted file: canonical form summary + classification as
union-surface gap or hardcoded per-repo value moved to `repo-config.yml`)_

- `docs/naming.rs`: _(pending)_
- `doctor/checker.rs`: _(pending)_
- `doctor/tools.rs`: _(pending)_
- `repo_governance/instruction_size.rs`: _(pending)_
- `tests/doctor.rs`: _(pending)_

## Candidate learnings (populate during execution)

- **Per-file canonical decisions** — for each drifted file, record whether it was a union-surface gap
  or a value moved to `repo-config.yml`, and why.
- **Standing tri-repo src-diff gate** — evaluate whether a periodic/CI tri-repo `diff` over the
  rhino-cli boundary should be added so this class of drift is caught automatically rather than by
  manual audit. Candidate `plans/ideas.md` entry if adopted.
- **`tests/doctor.rs` boundary question** — whether `tests/` should be pulled into the codified
  byte-identity boundary alongside `src/`.

## Triage log (Phase 5)

- _(to be completed)_
