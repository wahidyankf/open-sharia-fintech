---
description: "Provides a complete copy-paste example of a UI design funnel record formatted for prd.md."
when_to_use: "Use when you need a ready-to-copy template for recording a plan's UI design funnel in prd.md."
---

# Placement — the UI Lives in prd.md (HARD RULE): Copy-Paste Example

**Copy-paste example — funnel record (place in plan's `prd.md`)**:

```markdown
## UI Design Funnel — Compare-All Screen

### Stage 1 — Diverge (Low-Fidelity Alternatives)

#### Option A — Ranked Table

\`\`\`
┌────────────────────────────────────────────────────────────┐
│ ┏ Compare All ┓ ( Single City ) │
│ Salary [ 4,000 USD/mo ] Household [ Single ▼ ] (•)Rural │
├────────────────────────────────────────────────────────────┤
│ City Savings/mo % of salary ⇅ │
│ Jakarta $2,100 52% ███████ │
│ Kuala Lumpur $1,800 45% ██████ │
│ Singapore $1,200 30% ████ │
└────────────────────────────────────────────────────────────┘
\`\`\`

#### Option B — Card Grid

\`\`\`
┌────────────────────────────────────────────────────────────┐
│ ┏ Compare All ┓ ( Single City ) │
│ ┌── Jakarta ───────┐ ┌── Kuala Lumpur ──┐ │
│ │ Save $2,100/mo │ │ Save $1,800/mo │ │
│ └──────────────────┘ └──────────────────┘ │
└────────────────────────────────────────────────────────────┘
\`\`\`

### Stage 2 — Narrow (Hi-Fi Finalists)

Option B dropped here: shows few cities per screen, weak for side-by-side number comparison.

#### Finalist 1 — Option A (Ranked Table)

![Option A — Ranked Table, hi-fi mockup](./assets/ui-compare-all-option-a.excalidraw.png)

#### Finalist 2 — Option C (Split Layout)

![Option C — Split layout, hi-fi mockup](./assets/ui-compare-all-option-c.excalidraw.png)

### Stage 3 — Selection

**Selected: Option A — Ranked Table.**

### Stage 4 — Rationale

| Option         | Outcome           | Why                                                                          |
| -------------- | ----------------- | ---------------------------------------------------------------------------- |
| A — Ranked Tbl | **Chosen**        | Densest scan; native sort; reuses web-ui Table; collapses cleanly on mobile. |
| C — Split      | Runner-up         | Left rail wastes space on mobile; no advantage over A for compare task.      |
| B — Card Grid  | Dropped (Stage 2) | Weak for precise side-by-side number comparison.                             |
```
