# Plan Structure — Multi-File and Single-File

## Multi-File Structure (default — five documents)

**For any plan with substantive business intent, product scope, and technical design:**

```
plans/in-progress/complex-feature/
├── README.md                 # Context, Scope, Approach Summary, navigation
├── brd.md                    # Business Requirements Document
├── prd.md                    # Product Requirements Document
├── tech-docs.md              # Architecture, design decisions, file impact
└── delivery.md               # Phased checklist (one checkbox = one action)
```

**Content-placement split** (authoritative — see [Content-Placement Rules](../../../../repo-governance/conventions/structure/plans/content-placement-rules.md#content-placement-rules-brdmd-vs-prdmd)):

- **`brd.md`** — WHY: business goal, impact, affected roles, business-level success metrics, business-scope Non-Goals, business risks. Solo-maintainer repo — no sign-off / sponsor / stakeholder ceremony language.
- **`prd.md`** — WHAT: product overview, personas, user stories, Gherkin acceptance criteria, product scope (in + out), product risks.
- **`tech-docs.md`** — HOW: architecture, design decisions with rationale, an annotated file-impact tree,
  dependencies, rollback. Its `## File-Impact Analysis` is a root-relative fenced `text` tree with
  `[E]`/`[N]`/`[D]`/`[G]` markers as the primary scope view. Add `### More Detail` directly below it
  only for non-obvious mechanics, ordering, discovery criteria, or archival follow-up; it never
  replaces the tree or contains delivery checkboxes. See [Plans Organization Convention §File-Impact
  Analysis Format](../../../../repo-governance/conventions/structure/plans/file-impact-analysis-format.md#file-impact-analysis-format-hard-rule).
- **`delivery.md`** — DO: sequential `- [ ]` checklist organized by phase; one concrete action per checkbox. Opens with the `[AI]`/`[HUMAN]` executor legend; each phase ends with a `### Phase N Gate` (must-pass verification) followed by a Pause Safety note.

**Benefits**: narrow PR diff per concern (business PRs touch brd.md only; product PRs touch prd.md only), sharper agent validation (plan-checker asserts placement per file), industry-norm alignment (BRD + PRD are recognized doc types).

## Single-File Structure (exception, ≤1000 lines)

**Only for trivially small plans** where both condensed BRD and condensed PRD fit without crowding the technical sections:

```
plans/in-progress/simple-feature/
└── README.md                 # All content in one file
```

**README.md mandatory sections (in order)**:

1. **Context** — background, non-technical framing
2. **Scope** — in-scope + out-of-scope; affected apps named
3. **Business Rationale (condensed BRD)** — why + affected roles + success metrics (gut-based reasoning OK when logic supports it; fabricated KPIs forbidden)
4. **Product Requirements (condensed PRD)** — user stories + Gherkin acceptance criteria + product scope
5. **Technical Approach** — architecture, design decisions
6. **Delivery Checklist** — phased `- [ ]` items; opens with the `[AI]`/`[HUMAN]` executor legend; every phase ends with a `### Phase N Gate` and a Pause Safety note
7. **Quality Gates** — local + CI gates
8. **Verification** — how to confirm done

If the plan grows past 1000 lines or authoring feels crowded, promote to the five-document multi-file layout before execution begins.
