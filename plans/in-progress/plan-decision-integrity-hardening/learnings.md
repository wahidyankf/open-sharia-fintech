<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: plan-decision-integrity-hardening

Append one entry per generalizable learning **as it surfaces** — not reconstructed from memory at the
end. Sanitize per the secret/sensitivity gate before writing anything down.

Entry shape:

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to `<path>` / filed as `plans/backlog/<slug>/` / discarded — `<reason>`
```

Phase 8 (Knowledge Capture) triages every entry to a durable home or an explicit discard. Code-homed
learnings (`apps/`, `libs/`, tests) are **always** filed as a separate `plans/backlog/<slug>/` plan and
never landed inline in this plan's commits or PR.

Phase 8 additionally applies this plan's own subject to itself: any routing that lands in `ose-public`
must also reach `ose-primer` and `ose-private`, or carry a written reason why it is `ose-public`-only.
An `ose-public`-only routing with no reason is the exact drift recorded as contributing factor C4.

If execution genuinely surfaces nothing generalizable, replace this file's body with the explicit
escape line: `No generalizable learnings — <one-line reason>`.

<!-- ── entries below ── -->

## Learning: the repo topology recorded in working memory had gone stale

- **Context**: planning-time survey of the parity set, before authoring any document.
- **Observation**: `ose-primer` and `ose-private` were both recorded as bare repositories driven
  through worktrees. `git -C <repo> rev-parse --is-bare-repository` returned `false` for both, and
  `git -C <repo> worktree list` showed a single normal checkout on `main` in each. The recorded
  topology was correct when written and had since changed. Had it been trusted, the plan would have
  carried an unnecessary bare-repo landing method, a deviation-matrix row for a deviation that does
  not exist, and a delivery-mode restriction (`main-to-*` unavailable) that no longer applies.
- **Why it might generalize**: repository topology is a per-invocation property, not a fixed
  attribute of a repository's name. The multi-repo parity workflow already says this twice and
  instructs verification with `git worktree list` rather than assumption — this run is a live
  instance of that instruction paying off, and a candidate worked example for the workflow's own
  text.
- **Terminal state**: pending Phase 8 triage.
