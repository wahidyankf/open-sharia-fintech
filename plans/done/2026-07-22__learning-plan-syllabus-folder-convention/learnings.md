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
- **Triage (terminal — routed inline, docs)**: KEEP. Routed to two durable homes, both already
  landed by this plan: (1) the descriptive home — the convention's `## Corpus Census and Section
Tiering` and `### Grandfathered Format Cohort` sections in
  [`repo-governance/conventions/structure/learning-plan-syllabus.md`](../../../repo-governance/conventions/structure/learning-plan-syllabus.md)
  record this exact 17-file ordered-list / omitted-`Short summary` cohort and freeze the census that
  exposed it; (2) the automated-catch home — a deterministic `rhino-cli md syllabus validate` is the
  surface that would catch a future silent fork, deliberately deferred until the format settles and
  filed as the two-pager [`plans/ideas/syllabus-conformance-validator.md`](../../ideas/q2-not-urgent-important/syllabus-conformance-validator.md).
  No code home is landed inline (the validator is future work behind a promotion signal, not part of
  this docs/governance plan). Secret gate: no secret present. Repo-relevance gate: ose-public corpus
  content, not infra-private — no cross-routing.

## Learning: `custodied-by:` is a custody echo, not a disposition value (surfaced in PR review)

- **Context**: PR-review cycle 2 on the `ose-public` delivering PR flagged that the convention's first
  draft listed `custodied-by:<plan-id>` as a `## Corpus Disposition` value "every learning-bearing
  plan declares," but a plan that only _consumes_ another corpus is by definition not learning-bearing
  and files that echo under its own `## Corpus Custody` heading instead.
- **Observation**: the owner-vs-consumer split was conflated across four surfaces at once — the
  convention, `tech-docs.md` DD-07/DD-08, the three `plan-*` agents, and the skill — so a single
  framing error had fanned out to every enforcement copy before review caught it.
- **Why it might generalize**: this is already caught for next time — the fix reconciled all surfaces
  in the same PR and the corrected convention text is now the single normative source enforcement
  cites; no separate durable home is needed beyond the shipped convention. Terminal: routed inline to
  the convention (already landed); discard as a standalone follow-up.
