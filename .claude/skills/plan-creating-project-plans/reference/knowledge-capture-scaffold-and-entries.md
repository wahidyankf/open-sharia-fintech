# Knowledge Capture — learnings.md Scaffold and Entry Shape

Every substantive plan's `delivery.md` MUST end with a **Knowledge Capture** phase — the final
substantive phase, positioned immediately before the Plan Archival section (see
[plan-archival.md](plan-archival.md)) — that triages the plan's transient `learnings.md`
running log to durable homes before archival. This Skill emits both the `learnings.md` scaffold
file (created empty in the plan folder alongside `delivery.md`) and the Knowledge Capture phase
itself into every new substantive plan by default.

**`learnings.md` scaffold** — create in the plan folder during Environment Setup, sibling to
`delivery.md`:

```markdown
<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: <plan-identifier>
```

The `# Learnings: <plan-identifier>` H1 is **mandatory**, not decorative: markdownlint MD041 requires
the first line of content to be a top-level heading, so a scaffold of bare HTML comments fails the
pre-commit markdown gate the moment the plan folder is first committed. Substitute the plan's own
folder slug for `<plan-identifier>`.

**Entry shape** (append during execution, the moment something generalizable is noticed — not
reconstructed from memory at the end):

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
```

See [knowledge-capture-phase-template.md](knowledge-capture-phase-template.md) for the phase
template that triages these entries, and the
[Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md)
for the authoritative triage rubric, litmus test, and worked examples.
