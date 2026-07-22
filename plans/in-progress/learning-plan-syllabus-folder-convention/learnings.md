# Learnings: learning-plan-syllabus-folder-convention

<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

Entry shape:

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
```

## Learning: A format transmitted only by example forks silently and no gate notices

- **Context**: authoring this plan, while measuring the three existing `syllabus/` corpora to derive
  the course template.
- **Observation**: 17 of plan 02's 120 course files render `co-NN`/`ex-NN` as an ordered list rather
  than bullets, and **all 17** of those same files also omit the `**Short summary**` header line — a
  perfect two-marker correlation identifying them as a distinct authoring cohort. Plans 06 and 07 are
  uniformly bullets. The fork is therefore inside the canonical corpus, not between plans, and
  nothing in the repo failed when it landed.
- **Why it might generalize**: this is the empirical case for the plan itself — wherever a repo
  transmits a rich artifact shape by "go read an existing one", divergence is the expected outcome,
  not the exception. Route on completion: the durable home is the convention this plan creates.
