# UI-Design-Funnel, Learning-Bearing Syllabus, and Diagram Format Fixes

## UI-Design-Funnel Scaffolding Fixes (Step 5k Findings)

For a missing funnel artefact on a UI-bearing plan, remediate by **scaffolding** the missing
sections — never by inventing the design. Re-validate each finding before applying (confirm the plan
is genuinely UI-bearing and the artefact is actually absent), and re-read the scaffolded section
after editing. Artefact shape:
[UI Mockups in Plan Docs convention](../../../../repo-governance/conventions/formatting/diagrams/42-ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope).

**Confidence**: **HIGH** — the plan is UI-bearing and a funnel section is completely absent from
`prd.md` (scaffold with stub placeholders), or funnel content exists but in the wrong file (move to
`prd.md` mechanically — placement is unambiguous). **MEDIUM** — a stage exists but is thin (one
low-fi alternative, no drop reasons, unnamed selection) — add the missing skeleton, flag for author
completion, never fabricate alternatives or rationale. **FALSE_POSITIVE** — pure refactor, non-UI, or
governance-only plan — exempt.

**How to scaffold**: insert into the plan's `prd.md` (mandatory placement; binary image assets under
`assets/`, referenced via `![]()`). Use placeholders the author must replace; never invent design
content:

````markdown
## UI Design Funnel — <Screen Name>

> _Scaffolded by plan-fixer — fill each placeholder. See the UI Mockups in Plan Docs convention._

### Stage 1 — Diverge (Low-Fidelity Alternatives)

#### Option A — <name>

```
<low-fi ASCII/Unicode wireframe — author to fill>
```

#### Option B — <name>

```
<second genuinely-different low-fi alternative — author to fill>
```

### Stage 2 — Narrow (Hi-Fi Finalists)

<one-line drop reason for each alternative cut here>

#### Finalist 1 — Option <X>

![<alt text>](./assets/ui-<screen>-option-x.excalidraw.png)

#### Finalist 2 — Option <Y>

![<alt text>](./assets/ui-<screen>-option-y.excalidraw.png)

### Stage 3 — Selection

**Selected: Option <X> — <name>.** _(author: name the chosen design)_

### Stage 4 — Rationale

| Option | Outcome             | Why                   |
| ------ | ------------------- | --------------------- |
| <X>    | Chosen              | <author: why it won>  |
| <Y>    | Runner-up / Dropped | <author: why it lost> |

### Stage 5 — Responsive Strategy (mobile/tablet/desktop, mobile-first)

| Breakpoint            | Layout behaviour for the selected design                         |
| --------------------- | ---------------------------------------------------------------- |
| Mobile (`< sm`)       | <author: how it stacks/collapses — the mobile-first base layout> |
| Tablet (`md` ≥ 768)   | <author: what changes vs mobile>                                 |
| Desktop (`lg` ≥ 1024) | <author: full layout — what expands/splits>                      |
````

When the responsive strategy is flagged missing (rule 17 item 8), scaffold the Stage 5 stub above
and ensure the low-fi tier shows the mobile↔desktop reflow. Also scaffold the grounding note (R5) and
prior-art citation (R7) when missing — add a stub delivery step delegating the survey to
`web-researcher` (prior art) and the `swe-developing-frontend-ui` skill / `libs/web-ui` inventory
(internal grounding), naming any net-new component.

## Learning-Bearing Syllabus-Record Scaffolding Fixes (Step 5n Findings)

For a missing syllabus artefact on a learning-bearing plan, scaffold the missing sections — never
invent corpus content. Re-validate first; re-read after editing. Artefact shape:
[Learning-Plan `syllabus/` Folder Convention](../../../../repo-governance/conventions/structure/learning-plan-syllabus.md).

**Confidence**: **HIGH** — folder layout completely absent (scaffold `syllabus/README.md`,
`syllabus/courses/README.md`, `syllabus/paths/README.md` with stubs), or the `## Corpus Disposition`/
`## Corpus Custody`/Custodian line is absent (scaffold with a placeholder for the author to choose).
**MEDIUM** — a course file exists but missing a REQUIRED template section — add the header with a
placeholder, never fabricate concepts/prose. **FALSE_POSITIVE** — the plan only reads/links/lightly
corrects an existing corpus — exempt.

**How to scaffold**: insert stubs directly under the plan's `syllabus/` folder.

`syllabus/README.md`:

```markdown
# <Corpus Name> — Syllabus

> _Scaffolded by plan-fixer — fill each placeholder. See the Learning-Plan `syllabus/` Folder
> Convention._

**Custodian**: `<plan-id>` <!-- author: name the owning plan -->

<one-paragraph corpus overview — author to fill>
```

`tech-docs.md` — Corpus Disposition (owning/custodian plan only):

```markdown
## Corpus Disposition

`<archive-with-plan|promote-to:<path>>` <!-- author: choose exactly one -->
```

`tech-docs.md` — Corpus Custody echo (consumer plan only; a plan carries exactly one of the two):

```markdown
## Corpus Custody

`custodied-by:<plan-id>` <!-- author: name the corpus's owning plan -->
```

For a missing course file's REQUIRED skeleton, point the author at the copy-paste template in
[Learning-Plan `syllabus/` Folder Convention §Copy-Paste Course Template](../../../../repo-governance/conventions/structure/learning-plan-syllabus/09-copy-paste-course-template.md#copy-paste-course-template)
rather than reproducing it inline.

## Diagram Format Fixes

Covers two finding types from the Diagram Format Check: (1) ASCII art that should be Mermaid, (2)
under-diagrammed plans.

### Finding Type 1: ASCII Art Should Be Mermaid

**Confidence**: **HIGH** — ASCII art clearly depicts a flow/sequence/state machine/component
interaction, the Mermaid equivalent is unambiguous — auto-convert. **MEDIUM** — ambiguous (hybrid
table/diagram) — flag for review. **FALSE_POSITIVE** — a simple directory tree or file listing —
exempt.

**How to convert**: follow
[repo-governance/conventions/formatting/diagrams.md](../../../../repo-governance/conventions/formatting/diagrams.md).
Choose the right type (component interactions/decision branches → `flowchart LR`; order-of-operations
→ `sequenceDiagram`; entity lifecycle → `stateDiagram-v2`; database schema → `erDiagram`). Default to
`flowchart LR` unless top-down is semantically required, with a `%%` comment explaining why. Follow
the color-blind-friendly palette and `%%` comment syntax from `docs-creating-accessible-diagrams`.

**Do not convert**: simple directory trees, or tables/matrices where Mermaid would reduce
readability.

### Finding Type 2: Under-Diagrammed Plan

**Confidence**: **HIGH** — the concern is unambiguous and the diagram type is deterministic —
auto-add. **MEDIUM** — the concern is present but plan prose is too sparse to derive a correct
diagram without invention — flag for review, never fabricate nodes/edges. **FALSE_POSITIVE** — the
plan is genuinely trivial/linear — exempt.

**How to add**: identify the concern from the finding; choose the diagram type (component
interactions/dependency position/decision branches → `flowchart LR`; sequence/flow →
`sequenceDiagram`; state transitions/phase flow → `stateDiagram-v2` or `flowchart LR`); derive nodes
and edges from plan prose only; apply the color-blind-friendly palette (verified hex codes, black
borders, white text on dark fills); place the diagram where the concern is first described. After
adding, re-read the containing section and confirm the diagram nodes match the surrounding prose.
