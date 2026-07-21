# Learnings: ayokoding-learning-path-04-course-authoring

Transient running log. The executor appends one entry per generalizable learning **during**
execution; the Knowledge Capture phase (Phase 15 of [`delivery.md`](./delivery.md)) triages every
entry to a durable home or an explicit discard before archival.

**Sanitize before writing.** Apply the secret/sensitivity gate at write time, not at triage time — a
secret written here is already in git history by the time triage runs. Replace any credential, token,
private hostname, or inventory detail with a `<placeholder>` token.

**Code learnings never land inline.** A learning whose home is `apps/`, `libs/`, or tests is ALWAYS
filed as a separate `plans/backlog/<slug>/` plan, never fixed inside this plan's own commits or PR.
This plan authors content only; a defect found in the `course-paths` feature code belongs to
[`ayokoding-learning-path-03-navigation-ui`](../ayokoding-learning-path-03-navigation-ui/README.md)
or to a new backlog plan — not here.

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

## Entries

<!-- Append entries below this line during execution. -->
