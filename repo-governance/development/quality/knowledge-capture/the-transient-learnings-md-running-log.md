---
description: "How the transient learnings.md log works."
when_to_use: "Use when maintaining a plan's learnings.md log."
---

# The Transient `learnings.md` Running Log

`learnings.md` is a plan-folder file, sibling to `delivery.md`, `prd.md`, and the selected
`tech-docs.md` or `tech-docs/` form:

```
plans/
├── in-progress/
│   └── my-plan/
│       ├── README.md
│       ├── brd.md
│       ├── prd.md
│       ├── tech-docs.md
│       ├── delivery.md
│       └── learnings.md          ← running log, accrued during execution
└── done/
    └── 2026-07-05__my-plan/
        ├── delivery.md
        └── learnings.md          ← moves with the plan; MAY be deleted later
```

**When it is written**: while executing delivery steps (the plan-execution workflow's execution
loop), not reconstructed from memory at the end. The moment an executor notices something
generalizable — a rule that should have been enforced, a fact that surprised them, a bug pattern, a
gap in a skill's instructions — they append a sanitized entry to `learnings.md` and keep working.
This is cheap in-the-moment capture, not a separate research task.

**Entry shape** (minimal, not a formal template):

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
```

**What it is NOT**: `learnings.md` is not a decision log, not a design-rationale document (that is
the chosen technical form's job), and not a status report. It exists solely to stage candidate learnings for the
triage pass described below.
