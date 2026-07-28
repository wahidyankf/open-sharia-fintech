# Learnings: ayokoding-www-tools-ai-benchmark

<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

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

Phase 11 (Knowledge Capture) triages every entry to a durable home or an explicit discard. Code-homed
learnings (`apps/`, `libs/`, tests) are **always** filed as a separate `plans/backlog/<slug>/` plan and
never landed inline in this plan's commits or PR.

If execution genuinely surfaces nothing generalizable, replace this file's body with the explicit
escape line: `No generalizable learnings — <one-line reason>`.

<!-- ── entries below ── -->
