# Learnings: ayokoding-learning-path-07-course-authoring-low-level-systems

Transient running log. The executor appends one entry per generalizable learning **during**
execution; the Knowledge Capture phase (Phase 6 of [`delivery.md`](./delivery.md)) triages every
entry to a durable home or an explicit discard before archival.

**Sanitize before writing.** Apply the secret/sensitivity gate at write time, not at triage time — a
secret written here is already in git history by the time triage runs. Replace any credential, token,
private hostname, or inventory detail with a `<placeholder>` token.

**Code learnings never land inline.** A learning whose home is `apps/`, `libs/`, or tests is ALWAYS
filed as a separate `plans/backlog/<slug>/` plan, never fixed inside this plan's own commits or PR.
This plan authors content only; a defect found in the `course-paths` feature code belongs to
`ayokoding-learning-path-03-navigation-ui` or to a new backlog plan — not here.

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

## Rule-15 exemption record

The three live-site testers are exempt because this plan ships content bundles rather than a screen
or component, its rendering surface was already retested by the navigation-UI plan, and dedicated
course-content checkers cover the authored output more directly. Running the triad would retest a
surface this plan does not own. This record is terminal: no reusable process or code change follows.

No generalizable learnings — the remaining observations were course-specific content corrections
already covered by Markdown, link, and course-structure validation.
