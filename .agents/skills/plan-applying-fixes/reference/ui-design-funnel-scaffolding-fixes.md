# UI-Design-Funnel Scaffolding Fixes

## UI-Design-Funnel Scaffolding Fixes (Step 5k Findings)

For a missing funnel artefact on a UI-bearing plan, remediate by **scaffolding** the missing
sections — never by inventing the design. Re-validate each finding before applying (confirm the plan
is genuinely UI-bearing and the artefact is actually absent), and re-read the scaffolded section
after editing. Artefact shape:
[UI Mockups in Plan Docs convention](../../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope).

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
