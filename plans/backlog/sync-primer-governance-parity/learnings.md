# Learnings: sync-primer-governance-parity

Transient running log. The executor appends one entry per generalizable learning **during**
execution; the Knowledge Capture phase (Phase 5 of [`delivery.md`](./delivery.md)) triages every
entry to a durable home or an explicit discard before archival.

**Sanitize before writing.** Apply the secret/sensitivity gate at write time, not at triage time — a
secret written here is already in git history by the time triage runs. Replace any credential, token,
private hostname, or inventory detail with a `<placeholder>` token.

**Code learnings never land inline.** A learning whose home is `apps/`, `libs/`, or tests in
`ose-public`, `ose-primer`, or `ose-private` is ALWAYS filed as a separate `plans/backlog/<slug>/`
plan in the owning repo, never fixed inside this plan's own commits or PRs. This plan syncs
governance content and rhino-cli boundary state; a defect found in unrelated product code belongs
to its own backlog plan, not here.

**Never empty.** If no generalizable learning surfaced, record the explicit escape below:
`No generalizable learnings — <one-line reason>`.

## Entry template

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning — would a durable surface catch this
  automatically next time?
```

<!-- Entries accumulate below during execution. This plan has not begun execution yet. -->
