---
name: plan-creating-project-plans
description: Comprehensive project planning standards for plans/ directory including folder structure (ideas.md, backlog/, in-progress/, done/), stage-aware naming convention (backlog/done use YYYY-MM-DD__identifier/, in-progress uses identifier/ with no date prefix), five-document file organization (README.md, brd.md, prd.md, tech-docs.md, delivery.md for multi-file default; single README.md for trivially-small single-file exception), BRD/PRD content-placement rules, Gherkin acceptance criteria, and the mandatory structured multiple-choice grilling gates (pre-write and post-write) for resolving design decisions with the user. Essential for creating structured, executable project plans.
---

# Creating Project Plans

## Purpose

This Skill provides comprehensive guidance for creating **structured project plans** in the plans/ directory. Plans follow standardized organization, naming conventions, and acceptance criteria patterns for executable, traceable project work.

**When to use this Skill:**

- Creating new project plans
- Organizing backlog items
- Converting ideas to structured plans
- Writing Gherkin acceptance criteria
- Structuring multi-phase projects
- Moving plans through workflow stages

## Mandatory Pre-Write and Post-Write Grilling

Before writing any plan content, resolve all open design decisions with the user via structured
multiple-choice grilling (pre-write grill). After writing the plan, validate and stress-test it
with the user the same way (post-write grill). Neither gate is optional.

**HARD RULE — 2-4 options required**: Every grilling question MUST present **2-4 concrete,
mutually exclusive options**. Each option MUST state its trade-off in one sentence. Exactly one
option MUST be marked `(Recommended)` with a one-sentence rationale. Open-ended questions without
options are FORBIDDEN. Resolve one decision per question; tightly coupled decisions may be batched
in a single multi-question prompt.

**Mechanism**: use the `AskUserQuestion` tool (or the harness's native interactive multiple-choice
tool) first when available; fall back to inline markdown options when it is not.

**Explore before asking**: read the relevant repo artifacts before composing any question. Never
ask the user something a file read can answer — the repo is the ground truth; the user is the
tiebreaker for genuinely ambiguous decisions.

**Pre-write grill covers** (each as a structured multiple-choice question):

- What problem is this solving? What specific pain point?
- What are the acceptance criteria? How will we know it is done?
- What is the scope? What is explicitly out of scope?
- What are the constraints (performance, harness-neutrality, backwards compatibility)?
- Are there design decision forks where the user has a preference?
- **For UI-bearing plans only**: the UI-design-funnel questions — which low-fi alternatives, what
  prior art, which selection + why (see
  [the UI-design-funnel grilling questions](#design-funnel-grilling-questions-ui-bearing-plans)).

**Post-write grill covers** (each as a structured multiple-choice question):

- Does the plan structure match the user's intent? Are all acceptance criteria captured?
- Is Gherkin completeness sufficient (every acceptance criterion has a scenario)?
- Is checklist granularity correct (each item is one concrete action; TDD substeps separate)?
- Is the `## Worktree` section present?
- Is Phase 0 (Environment Setup and Baseline) the first phase in `delivery.md`?
- Does `delivery.md` open with the `[AI]`/`[HUMAN]` executor legend, and is every step that only a human can do tagged `[HUMAN]`?
- Does every phase end with a `### Phase N Gate` (must-pass verification) followed by a Pause Safety note?

**Do NOT proceed to writing until all pre-write branches are resolved.** Unresolved design
decisions force expensive rewrites.

See [Grilling-With-Options Convention](../../../repo-governance/development/workflow/grilling-with-options.md)
for the authoritative rule, validation checklist, and examples. Invoke via the `grill-me` skill.

## Plans Folder Structure

```
plans/
├── ideas.md                              # 1-3 line ideas (brainstorming)
├── backlog/                              # Future work
│   └── YYYY-MM-DD__project-name/        # Planned but not started
├── in-progress/                          # Active work
│   └── project-name/                    # Currently executing (no date prefix)
└── done/                                 # Completed work
    └── YYYY-MM-DD__project-name/        # Archived (completion date prefix)
```

## Plan Naming Convention

Naming is **stage-aware** — each lifecycle stage has its own rule:

| Stage          | Format                            | Date meaning    |
| -------------- | --------------------------------- | --------------- |
| `backlog/`     | `YYYY-MM-DD__project-identifier/` | Creation date   |
| `in-progress/` | `project-identifier/`             | No date prefix  |
| `done/`        | `YYYY-MM-DD__project-identifier/` | Completion date |

**Rules** (identifier part, all stages):

- Separator between date and identifier: Double underscore (`__`)
- Identifier: Lowercase, hyphen-separated, descriptive
- Trailing slash indicates directory
- Strip the date prefix when moving from `backlog/` → `in-progress/`
- Add the completion date prefix when moving from `in-progress/` → `done/`

## Mermaid Diagrams in Plans

Plans MUST include **extensive Mermaid diagrams where appropriate**: every distinct architectural concern the plan touches that a reader would otherwise reconstruct mentally from prose SHOULD receive its own diagram — one diagram per concern, not one diagram total.

Concerns that warrant their own diagram when present:

- **Component interactions** — service/agent/library call graph
- **Sequence or flow between agents or systems** — order-of-operations across processes
- **State transitions** — entity lifecycle with named states and triggers
- **Decision branches** — conditional logic with multiple outcomes
- **Dependency position** — upstream/downstream plan or system dependencies
- **Phase/delivery flow** — phased progression with gates and transition conditions

Prefer multiple focused diagrams over one overloaded diagram. Trivial/linear plans (single-file config bumps, renames, doc fixes) may skip diagrams — this is the "where appropriate" escape hatch.

**Authoritative rule**: [repo-governance/conventions/structure/plans.md §Diagrams in Plans](../../../repo-governance/conventions/structure/plans.md#diagrams-in-plans)

**Palette and accessibility**: use the `docs-creating-accessible-diagrams` skill for the verified WCAG-compliant hex codes and color-blind-friendly palette.

## UI Mockups in UI-Bearing Plans — the UI-design-funnel (HARD RULE)

A plan is **UI-bearing** when it adds or changes user-facing screens or components under `apps/` or
`libs/` (e.g. `libs/web-ui`). Pure refactors, no-UI plans, and governance-only plans are exempt —
exactly as with the specs/Gherkin binding.

Every UI-bearing plan MUST document its draft UI through the **UI-design-funnel**
(diverge → narrow → select → justify), authored per the
[UI Mockups in Plan Docs convention](../../../repo-governance/conventions/formatting/diagrams.md#ui-mockups-in-plan-docs).

**PLACEMENT HARD RULE**: ALL funnel artefacts MUST be placed in the plan's **`prd.md`** — not in
`README.md`, `brd.md`, `tech-docs.md`, or any separate file. Binary mockup image assets live
under the plan's `assets/` folder and are referenced from `prd.md` via `![]()` image embeds.
A UI-bearing plan whose `prd.md` does NOT contain the funnel record (all four stages plus embedded
mockup links) fails the plan quality gate. See
[UI Mockups in Plan Docs — Placement](../../../repo-governance/conventions/formatting/diagrams.md#placement--the-ui-lives-in-prdmd-hard-rule).

The funnel produces four kinds of artefact, all visible in the plan (`prd.md` + the plan's
`assets/`); no alternative is silently discarded:

- **Both tiers per screen** — each screen gets a **low-fidelity** ASCII/Unicode wireframe in a
  fenced code block AND a **high-fidelity** `.excalidraw.png` referenced via `![](./file)`, in
  separate labelled subsections. Never use inline HTML+CSS, MDX, Mermaid-as-wireframe, or
  `.excalidraw.svg` (GitHub strips/garbles them).
- **Diverge** — **≥ 2 (aim for 3) genuinely different** named low-fi alternatives (Option A / B / C).
- **Narrow** — the **2 strongest** carried forward as hi-fi `.excalidraw.png` finalists, with a
  one-line drop reason for each alternative cut.
- **Select** — the chosen design **named explicitly** (e.g. "Selected: Option A — Ranked Table").
- **Justify** — a short **rationale / decision record** (a small table is enough): why the winner
  won and why each runner-up lost.
- **Grounding note (R5)** — before drafting either tier, survey the existing UI of the related
  app(s) and lib(s) (`libs/web-ui` component inventory + tokens + Storybook, the target app's
  shell, sibling screens; reference the `swe-developing-frontend-ui` skill) and reuse what already
  exists; name any net-new component explicitly.
- **Prior-art citation (R7)** — consult prior art on how comparable tools solve the screen via the
  `web-researcher` agent, so the divergent alternatives are informed rather than invented.
- **Responsive design (mobile/tablet/desktop)** — the funnel MUST address **responsive** behaviour,
  **mobile-first**, across mobile (`< sm`), tablet (`md` ≥ 768 px), and desktop (`lg` ≥ 1024 px).
  The low-fi tier must show the mobile↔desktop reflow where it differs (e.g. table → stacked cards,
  side rail → top sheet); the selected design's record must state the **responsive strategy** per
  breakpoint; and each finalist is evaluated on its **mobile-first responsive behaviour**, not its
  desktop appearance alone. A desktop-only design is not a valid finalist.

`plan-maker` requires these artefacts and emits delivery steps that produce them; `plan-checker`
flags any missing artefact at HIGH criticality (its UI-design-funnel completeness step, sibling to
the specs/Gherkin Step 5j); `plan-fixer` scaffolds the missing funnel sections. This mirrors the
**Specs & Gherkin completeness (both paths)** binding: a UI-bearing plan never passes quality gates
without its design funnel.

### Design-funnel grilling questions (UI-bearing plans)

When grilling the user on a UI-bearing plan, the pre-write grill MUST cover the UI-design-funnel
decisions as structured multiple-choice questions (each with 2-4 concrete options plus the two
standing options — a free-form blank-state type and "chat about this"):

- **Which alternatives?** Present 2-4 candidate low-fi layouts for the screen (e.g. Ranked Table /
  Card Grid / Split Layout), each option stating its trade-off in one sentence, one marked
  `(Recommended)`. The author must produce ≥2 genuinely different named alternatives.
- **What prior art?** Present 2-4 ways to ground the alternatives (e.g. delegate a
  `web-researcher` survey of comparable tools / reuse a named sibling screen pattern / blend the
  web-ui kit only), so the diverge stage is informed rather than invented.
- **Which selection, and why?** Present the finalists as options (e.g. Option A / Option B) and ask
  which design wins and the one-sentence rationale, so the Select + Justify stages are explicit.
- **What responsive strategy?** Present 2-4 ways the selected layout reflows from **mobile** to
  **desktop** (e.g. table collapses to stacked cards / side rail moves into a top sheet / two-pane
  split becomes a single column), so the **responsive** behaviour across mobile/tablet/desktop is
  decided mobile-first rather than designed desktop-only.

See [Grilling-With-Options Convention](../../../repo-governance/development/workflow/grilling-with-options.md)
for the authoritative multiple-choice format.

## Plan Structure

### Multi-File Structure (default — five documents)

**For any plan with substantive business intent, product scope, and technical design:**

```
plans/in-progress/complex-feature/
├── README.md                 # Context, Scope, Approach Summary, navigation
├── brd.md                    # Business Requirements Document
├── prd.md                    # Product Requirements Document
├── tech-docs.md              # Architecture, design decisions, file impact
└── delivery.md               # Phased checklist (one checkbox = one action)
```

**Content-placement split** (authoritative — see [Content-Placement Rules](../../../repo-governance/conventions/structure/plans.md#content-placement-rules-brdmd-vs-prdmd)):

- **`brd.md`** — WHY: business goal, impact, affected roles, business-level success metrics, business-scope Non-Goals, business risks. Solo-maintainer repo — no sign-off / sponsor / stakeholder ceremony language.
- **`prd.md`** — WHAT: product overview, personas, user stories, Gherkin acceptance criteria, product scope (in + out), product risks.
- **`tech-docs.md`** — HOW: architecture, design decisions with rationale, file-impact, dependencies, rollback.
- **`delivery.md`** — DO: sequential `- [ ]` checklist organized by phase; one concrete action per checkbox. Opens with the `[AI]`/`[HUMAN]` executor legend; each phase ends with a `### Phase N Gate` (must-pass verification) followed by a Pause Safety note.

**Benefits**: narrow PR diff per concern (business PRs touch brd.md only; product PRs touch prd.md only), sharper agent validation (plan-checker asserts placement per file), industry-norm alignment (BRD + PRD are recognized doc types).

### Single-File Structure (exception, ≤1000 lines)

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

## Worktree Specification (Mandatory — Applies to ALL Plans)

Every plan MUST declare its worktree path before the delivery checklist begins. This is enforced by `plan-checker` (HIGH finding when missing) and the [plan-execution workflow Step 0 hard gate](../../../repo-governance/workflows/plan/plan-execution.md) — execution refuses to start if the section is absent. When the section is present, the executor enters the declared worktree by default: it auto-provisions from the latest `origin/main` when missing, syncs with `origin/main` before implementing, and prompts the user before deleting the worktree after the plan is archived and pushed.

**Where to declare**:

- **Multi-file plans**: top-level `## Worktree` section in `delivery.md`, placed before any phase heading.
- **Single-file plans**: top-level `## Worktree` section in `README.md`, placed before `## Delivery Checklist`.

**Path format**: `worktrees/<plan-identifier>/` where `<plan-identifier>` matches the plan-folder identifier (strip the `YYYY-MM-DD__` date prefix). Examples:

- Folder `2026-05-15__auth-rewrite/` → worktree path `worktrees/auth-rewrite/`
- Folder `2026-03-01__add-user-search/` → worktree path `worktrees/add-user-search/`

**Required template** (insert verbatim, replacing `<plan-identifier>`):

````markdown
## Worktree

Worktree path: `worktrees/<plan-identifier>/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree <plan-identifier>
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest `origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting the worktree after the plan is archived and pushed.

See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) and [Plans Organization Convention §Worktree Specification](../../../repo-governance/conventions/structure/plans.md#worktree-specification).
````

**This applies to ALL plans regardless of size** — pure-docs, single-file, and trivial plans included. No exceptions.

## Delivery Mode (Mandatory — Applies to ALL Plans)

Every plan resolves to exactly one **delivery mode** before execution begins, declared alongside the `## Worktree` / `## Worktree Specification` section above. Delivery mode is a sibling concern to the worktree declaration: the worktree fixes the **work location**; delivery mode additionally fixes the **integration target** and **merge authority**.

**The four modes** (full table and precedence algorithm: [Plans Organization Convention §Delivery Mode](../../../repo-governance/conventions/structure/plans.md#delivery-mode)):

- **`worktree-to-pr`** — **the default** when no mode is otherwise specified. Work in `worktrees/<plan-identifier>/`, draft PR opened against `main`, `[HUMAN]` merges when ready.
- **`worktree-to-origin-main`** — work in the worktree, direct push to `origin main`, `[AI]` pushes directly.
- **`main-to-origin-main`** — primary checkout (no worktree), direct push to `origin main`, `[AI]` pushes directly.
- **`main-to-pr`** — primary checkout (no worktree), PR opened against `main`, `[HUMAN]` merges when ready.

`worktree-to-pr` is the safest default absent a reason to pick another mode — it isolates work and routes it through review before it touches `main`.

**Declare it explicitly**: `## Delivery Mode: worktree-to-pr` (or one of the other three modes), placed immediately alongside the `## Worktree` declaration. An unmarked plan resolves to the tier-3 default (`worktree-to-pr`) per the three-tier precedence algorithm (invocation argument → plan field → default).

**`*-to-pr` modes run the PR-Review Maker→Fixer Cycle**: for `worktree-to-pr` and `main-to-pr`, the delivery checklist's finalization phase MUST emit the [PR-Review Maker→Fixer Cycle workflow](../../../repo-governance/workflows/pr/pr-review-quality-gate.md) (a fixed N-cycle, default 3, sequential `pr-review-maker` → `pr-review-fixer` loop with a hard CI-green gate between cycles) before the PR is considered done. The `[HUMAN]` merge itself sits outside this done-boundary — the plan hands off a green, fully-reviewed PR and the human merges on their own schedule.

**Invalid values are a finding, never silently coerced**: a delivery-mode value that is not one of the four modes above is a `plan-checker` HIGH finding, not a silent fallback to the default.

## Execution-Grade Clarity (HARD RULE)

Plans are executed by **execution-grade (sonnet-tier)** agents, not planning-grade (opus-tier) agents. Authoring-grade hand-waving is forbidden.

**Every checkbox MUST contain all of the following that apply**:

- **Explicit file path(s)** when the action touches a known file. When the path cannot be determined at authoring time, give the maximum-possible-detail target: parent directory + naming pattern + sibling reference (e.g., "new file under `apps/organiclever-www/src/lib/` following the pattern of sibling `auth.ts`").
- **Explicit shell command(s)** verbatim when applicable (e.g., `npx nx run ose-web:test:quick`), not "run the lint".
- **Concrete acceptance criterion** stating the observable change that proves done (e.g., "all assertions in `trpc.test.ts` pass", "`nx run ose-web:typecheck` exits 0"). No bare "implement X", "set up Y", "configure Z".

**`plan-checker` flags violations as HIGH severity. `plan-fixer` rewrites offending items with maximum detail.**

### Bad / Good Examples

**Bad** (missing path, missing command, missing criterion):

```markdown
- [ ] Add caching
```

**Good** (explicit path, explicit command, explicit criterion):

```markdown
- [ ] Edit `apps/ose-www/src/server/trpc.ts`: wrap the public router with
      `unstable_cache(..., { revalidate: 300 })`. Verify by running
      `npx nx run ose-web:test:quick` — all tests pass.
```

**Bad**:

```markdown
- [ ] Implement the rate-limit middleware
```

**Good**:

```markdown
- [ ] Create `apps/organiclever-be/src/Middleware/RateLimit.fs` (siblings: `Auth.fs`, `Cors.fs`)
      implementing token-bucket rate limiting per `tech-docs.md §Rate Limiting`. Verify by running
      `npx nx run organiclever-be:test:unit` — new test `RateLimit_RejectsExceedingRequests` passes.
```

**Bad**:

```markdown
- [ ] Run the lint
```

**Good**:

```markdown
- [ ] Run `npx nx affected -t lint` — exits 0 with no errors reported.
```

See [Plans Organization Convention §Execution-Grade Clarity](../../../repo-governance/conventions/structure/plans.md#execution-grade-clarity-hard-rule) for the authoritative rule.

## Executor Tagging — [AI] vs [HUMAN] (HARD RULE)

Every delivery checklist item MUST make clear **who can execute it**. Some work cannot be done by an AI agent at all — physical actions (unplug a power cable, swap a drive), out-of-band approvals (approve a production deploy, accept a contract), or actions needing real credentials or authority the agent must not hold. Tagging up front lets the executor hand off to the human cleanly instead of fabricating a completion.

**Tags** (placed at the START of the checkbox, right after `- [ ]`):

- **`[AI]`** — an agent can fully perform the step. **Default**: an unmarked checkbox is treated as `[AI]`.
- **`[HUMAN]`** — only a human can do it (physical action, out-of-band approval/sign-off, real-secret or privileged-credential handling, real-world authority).
- **`[AI+HUMAN]`** (optional) — agent prepares/drafts; human reviews, approves, or performs the irreversible final action.

**Required legend** — open `delivery.md` (or a single-file plan's Delivery Checklist section) with:

```markdown
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: only a human can do it (physical action, out-of-band approval, real-secret or
> privileged-credential handling). `[AI+HUMAN]`: agent prepares, human approves or finishes.
```

**Default bias (prefer `[AI]`, HARD RULE)**: use `[AI]` as much as possible and `[HUMAN]` as little as possible. Reserve `[HUMAN]` for what is genuinely inevitable — impossible or unsafe for an agent, or requiring real-world authority or credentials an agent must not hold — OR for steps the user or plan has explicitly asked to keep `[HUMAN]`. A sanctioned channel that lets an agent do something seemingly human-only (e.g. copying a real secret via an `[AI]`-authored script through the `guard-env-file-access` path) stays `[AI]` — document the channel inline. When both an `[AI]` and a `[HUMAN]` path would accomplish the step, choose `[AI]`.

**Git-mechanical steps are `[AI]` (HARD RULE)**: provision the worktree (`git worktree add …`), commit, push (to `origin main` for `*-to-origin-main` modes, or to the PR branch for `*-to-pr` modes), and remove the worktree (`git worktree remove …`) are git-mechanical steps the agent performs directly — always tag them `[AI]`, never `[HUMAN]`. For the default `worktree-to-pr` mode, do **not** author a `[HUMAN]` "review the diff and approve push" gate for the push itself — pushing to the PR branch is `[AI]`; only the final PR merge to `main` is `[HUMAN]` (per [Delivery Mode](#delivery-mode-mandatory--applies-to-all-plans) above), and only after the PR-Review Maker→Fixer Cycle has completed. See [Git Push Default Convention](../../../repo-governance/development/workflow/git-push-default.md).

**Execution semantics**: the [plan-execution workflow](../../../repo-governance/workflows/plan/plan-execution.md) STOPS at a `[HUMAN]` item, surfaces it with the acceptance criterion, and waits for the human to confirm before continuing. This is a legitimate stop that overrides "never stop between phases".

## Phases as Natural Pauses With Clear Gates (HARD RULE)

Every phase MUST be a **natural pause point** that ends with a **clear gate**. A reader (human or AI) must be able to stop after any phase and find the repository coherent — code compiles, tests pass, nothing half-applied, no known-red build carried forward.

- **Clear gate**: every phase ends with a `### Phase N Gate` subsection — a must-pass verification checklist naming exact commands and observable acceptance criteria. Phase N+1 MUST NOT begin while any gate check is failing.
- **Pause Safety note**: immediately after the gate, add a `> **Pause Safety**:` blockquote stating the safe-to-stop state and the single command to resume/re-verify.

**Template**:

```markdown
## Phase N: <name>

- [ ] [AI] <work item> — acceptance: <observable outcome>

### Phase N Gate

> All checks below must pass before starting Phase N+1.

- [ ] [AI] `<verification command>` — <acceptance>

> **Pause Safety**: <coherent state after this phase>. Safe to stop. To resume: `<re-verify command>`.
```

Phase 0 (Environment Setup and Baseline) already follows this shape — its gate is the recorded clean baseline. A gate MAY be a `[HUMAN]` approval, making the boundary an explicit hand-off point.

See [Plans Organization Convention §Executor Tagging](../../../repo-governance/conventions/structure/plans.md#executor-tagging--ai-vs-human-hard-rule) and [§Phases as Natural Pauses With Clear Gates](../../../repo-governance/conventions/structure/plans.md#phases-as-natural-pauses-with-clear-gates-hard-rule) for the authoritative rules.

## Pre-Write Verification (Anti-Hallucination — HARD)

Before writing any non-trivial factual claim into a plan, run the verification recipe for the claim's category. Hallucinated content (fabricated file paths, invented Nx targets, made-up versions, fictitious APIs, fabricated KPIs) turns a plan into broken work the moment execution begins. Verify at authoring time — it is the cheapest place to catch fabrication.

See [Plan Anti-Hallucination Convention](../../../repo-governance/development/quality/plan-anti-hallucination.md) for the authoritative rules.

### Verification Recipes

| Claim Category    | Verification Command                                                                   |
| ----------------- | -------------------------------------------------------------------------------------- |
| File path         | `Bash test -f <path>` or `Glob`; if NEW, mark inline as `_New file_`                   |
| Directory path    | `Bash test -d <path>`                                                                  |
| Symbol / function | `Grep` against the codebase                                                            |
| Nx target         | Read `apps/<project>/project.json` and confirm under `targets`                         |
| Package version   | `jq` the relevant manifest (`package.json`, `go.mod`, `Cargo.toml`, etc.)              |
| API signature     | Delegate to `web-researcher` with authoritative-doc URL                                |
| Command flag      | `<cmd> --help` OR repo-doc reference                                                   |
| Test name         | `Grep` test files; if NEW, mark `_New test_`                                           |
| Agent / skill     | `Bash test -f .claude/agents/<name>.md` or `.claude/skills/<name>/SKILL.md`            |
| External standard | Delegate to `web-researcher`; cite URL + access date + excerpt                         |
| Behavior claim    | `web-researcher` with cited official-doc excerpt                                       |
| Cross-link target | `Bash test -f` on the resolved relative path                                           |
| Numeric KPI       | Forbidden as bare fact; observable check / cited measurement / `_Judgment call:_` only |

### Confidence Labels (Inline)

Write one of the following next to each non-trivial claim:

- **`[Repo-grounded]`** — verified in current commit via `Glob` / `Grep` / `Bash` / `Read`
- **`[Web-cited]`** — verified externally; URL + access date + excerpt inline
- **`[Judgment call]`** — explicit subjective claim; numeric gut targets MUST use this label
- **`[Unverified]`** — flagged for follow-up; `plan-checker` reports as MEDIUM

Bare unlabeled claims default to `[Unverified]`. Label proactively.

### Refuse-on-Uncertainty

When verification fails or is impossible: REFUSE to write the claim as a fact. Acceptable refusals:

1. **Skip the claim** (preferred when omission keeps the plan coherent)
2. **Use `[Unverified]` label** (flagged for verification before execution)
3. **Use `[Judgment call]` label** (explicitly subjective)
4. **Use placeholder** — `_Unknown — verify before authoring_` under Open Questions

Forbidden: writing the claim without a label and hoping it is correct.

### Web-Research Delegation (Lower Threshold for Plan Content)

For plan content the threshold is LOWER than the universal convention:

> **Any external claim that is not already documented in the repo (`docs/`, `repo-governance/`, `apps/*/README.md`, `package.json`, `go.mod`, etc.) and that requires more than a single `WebFetch` against an already-known authoritative URL MUST be delegated to `web-researcher`.**

Concretely: most external claims require delegation. Single-shot fetches against a known URL are the only in-context exception. See [Plan Anti-Hallucination Convention §Web-Research Delegation](../../../repo-governance/development/quality/plan-anti-hallucination.md#web-research-delegation-lower-threshold-for-plans).

### Anti-Pattern Catalog (MUST NOT)

Reject these patterns at authoring time. `plan-checker` flags occurrences as HIGH:

- **AP-1** — citing a version without `Grep`'ing the manifest
- **AP-2** — inventing a file path that "should exist"
- **AP-3** — citing an Nx target that may not exist (read `project.json` first)
- **AP-4** — inventing a function or method name (delegate to `web-researcher`)
- **AP-5** — fabricating a numeric KPI presented as already-measured
- **AP-6** — inventing a test name (mark `_New test_` when applicable)
- **AP-7** — citing an agent or skill that does not exist
- **AP-8** — citing a CLI flag without `--help` or repo-doc reference
- **AP-9** — citing a behavior claim without a source
- **AP-10** — cross-linking to a file that does not exist

## Specialized-Executor Annotation

Domain-specialized agents hallucinate less than generic orchestration. When a delivery checkbox names a domain that maps cleanly to a specialized agent, annotate the checkbox with the suggested executor.

**Annotation format** (sub-bullet under the checkbox prose, before any implementation notes):

```markdown
- [ ] Edit `apps/organiclever-be/src/Domain/User.fs` [Repo-grounded]: add `email: string option` field
      with case-insensitive uniqueness. Verify by running `nx run organiclever-be:test:unit` — new test
      `User_RejectsDuplicateEmailIgnoringCase` passes.
  - _Suggested executor: `swe-fsharp-dev`_
```

**When to annotate**:

- Action touches a specific language file (`.fs`, `.go`, `.kt`, `.cs`, `.fsproj`, `.csproj`, etc.)
- Action touches a specific app context (`apps/ose-www/...` → `apps-ose-www-content-maker` for content)
- Action is content/documentation (`docs-maker`, `readme-maker`, `specs-maker`)
- Action is governance / repo rules (`repo-rules-maker`)
- Action is content-platform skill domain (`apps-ayokoding-www-by-example-maker`, `apps-ayokoding-www-in-the-field-maker`, etc.)

**When to skip annotation** (default plan-execution Agent Selection suffices):

- Single-line edit to a governance doc
- Mechanical operation (`mv`, `git mv`, `npm install`)
- Shell command without code edits

The plan-execution workflow respects the annotation as Priority 0 — the suggested executor wins over heuristic matches by file extension or content keyword. Citing a non-existent agent is treated as Anti-Pattern AP-7 (HIGH finding by `plan-checker`).

## Gherkin Acceptance Criteria

**All plans must have Gherkin-format acceptance criteria:**

```gherkin
Given [precondition]
When [action]
Then [expected outcome]
And [additional outcome]
```

**Example**:

```gherkin
Given the user is logged out
When they submit valid credentials
Then they are redirected to the dashboard
And their session is created with correct permissions
```

**Step-Keyword Cardinality (HARD Rule)**: Every `Scenario` MUST use exactly one primary `Given` line, exactly one primary `When` line, and exactly one primary `Then` line — chain every additional precondition, action, or outcome with `And`/`But`, never a repeated primary keyword. `Background` blocks and `Scenario Outline` `Examples` tables are exempt. See [Acceptance Criteria Convention §Step-Keyword Cardinality (HARD Rule)](../../../repo-governance/development/infra/acceptance-criteria.md#step-keyword-cardinality-hard-rule).

**Best Practices**:

- Use concrete, testable conditions
- Focus on behavior, not implementation
- One scenario per user story
- Make scenarios independent
- Use consistent language
- Exactly one primary `Given`/`When`/`Then` per scenario; extras chained with `And`/`But` (see HARD rule above)

## Git Workflow in Plans

**Trunk Based Development (Default)**:

- Work on `main` branch directly
- Small, frequent commits
- No feature branches (99% of plans)

**Branch-Based (Exceptional)**:

- Only for experiments, compliance, external contributions
- Must justify in Git Workflow section
- Requires explicit user approval

## Plan Lifecycle

### 1. Ideation (ideas.md)

**Format**: One-liner to 3-line description

**Example**:

```markdown
- **Rules Consolidation**: Fix Skills naming to gerund form, add References sections, create 7 new Skills for complete agent coverage
```

### 2. Planning (backlog/)

**Gate**: Resolve all open design decisions with the user via pre-write grilling before writing
any plan content. See [Mandatory Pre-Write and Post-Write Grilling](#mandatory-pre-write-and-post-write-grilling).

**Actions**:

- Create folder with date\_\_identifier
- Write requirements and acceptance criteria
- Define technical approach
- Outline delivery phases

**Status**: Not Started

### 3. Execution (in-progress/)

**Actions**:

- Move from backlog/ to in-progress/
- Update status to "In Progress"
- Execute delivery plan sequentially
- Update checklist with progress

**Status**: In Progress

### 4. Completion (done/)

**Gate**: Validate the finished plan with the user via post-write grilling before archiving. See
[Mandatory Pre-Write and Post-Write Grilling](#mandatory-pre-write-and-post-write-grilling).

**Actions**:

- Validate all acceptance criteria met
- Update status to "Completed"
- Move from in-progress/ to done/
- Archive for future reference

**Status**: Completed

## Delivery Plan Structure

### Implementation Steps (TDD Shape — MANDATORY for code-touching items)

Every delivery checklist item that touches production code MUST be expressed as a
Red→Green→Refactor cycle. Do not write "implement X, then write tests."

**TDD-shaped format** (each phase is its own checkbox):

```markdown
- [ ] [AI] **RED**: Write failing test for `[specific behavior]` in `[test file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: test fails with `[expected error message]`
  - _Suggested executor: `swe-[lang]-dev`_
- [ ] [AI] **GREEN**: Implement `[function/component]` in `[file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: test passes, no other tests broken
- [ ] [AI] **REFACTOR**: Clean up `[specific concern]` in `[file path]`
      — command: `nx run [project]:test:unit`
      — acceptance: all tests still pass, code is cleaner
```

**Multi-cycle format** (when a feature spans multiple mini-cycles):

```markdown
- [ ] [AI] TDD cycle: [feature name]
  - [ ] [AI] **RED**: write failing test for happy path
        — command: `nx run [project]:test:unit`
        — acceptance: test fails with `[expected error]`
  - [ ] [AI] **GREEN**: implement minimum code to pass
        — command: `nx run [project]:test:unit`
        — acceptance: test passes
  - [ ] [AI] **RED**: write failing test for error path
        — command: `nx run [project]:test:unit`
        — acceptance: test fails with `[expected error]`
  - [ ] [AI] **GREEN**: implement error handling
        — command: `nx run [project]:test:unit`
        — acceptance: both tests pass
  - [ ] [AI] **REFACTOR**: clean up, remove duplication
        — command: `nx run [project]:test:unit`
        — acceptance: all tests still pass
```

**HARD RULE**: Never combine RED, GREEN, and REFACTOR into a single checkbox. Each phase is its
own `- [ ]` item. `plan-checker` flags combined items (e.g., `- [ ] Implement X with TDD`) as
HIGH findings.

Non-code steps (doc edits, config, file creation) do NOT require Red→Green→Refactor. Use a
direct action + acceptance criterion instead.

**See**: [Test-Driven Development Convention](../../../repo-governance/development/workflow/test-driven-development.md) for the authoritative mandate, including how Gherkin scenarios map to first failing tests.

**Update after completion**:

```markdown
- [x] Step 1: Description
  - [x] Substep 1.1
  - [x] Substep 1.2
  - **Implementation Notes**: What was done, decisions made
  - **Date**: 2026-01-02
  - **Status**: Completed
  - **Files Changed**: List of modified files
```

### Validation Checklist

After implementation steps, add validation:

```markdown
### Validation Checklist

- [ ] All TDD cycles complete (RED→GREEN→REFACTOR for every code change)
- [ ] All tests pass (`nx affected -t test:quick`)
- [ ] Code meets quality standards
- [ ] Documentation updated
- [ ] Acceptance criteria verified
```

## Operational Readiness (Mandatory Delivery Sections)

Every delivery plan MUST include these operational readiness sections. Plans missing them are considered incomplete regardless of other quality.

### Local Quality Gates (Before Push)

Every plan must include steps for running affected quality checks locally before pushing:

```markdown
### Local Quality Gates (Before Push)

- [ ] Run affected typecheck: `nx affected -t typecheck`
- [ ] Run affected linting: `nx affected -t lint`
- [ ] Run affected quick tests: `nx affected -t test:quick`
- [ ] Run affected spec coverage: `nx affected -t specs:coverage`
- [ ] Fix ALL failures found — including preexisting issues not caused by your changes
- [ ] Verify all checks pass before pushing
```

Adapt targets to the plan's affected projects (add `test:integration`, `test:e2e` if applicable).

### Post-Push CI/CD Verification

Every plan must include steps to verify CI after pushing:

```markdown
### Post-Push Verification

- [ ] Push changes to `main`
- [ ] Monitor GitHub Actions workflows for the push
- [ ] Verify all CI checks pass
- [ ] If any CI check fails, fix immediately and push a follow-up commit
- [ ] Do NOT proceed to next delivery phase until CI is green
```

### Development Environment Setup

Every plan must start with environment setup steps:

```markdown
### Environment Setup

- [ ] Provision worktree: `claude --worktree <plan-identifier>` (creates `worktrees/<plan-identifier>/` in repo root; see [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md))
- [ ] Initialize toolchain in the root worktree (not the new worktree): `npm install && npm run doctor -- --fix` (see [Worktree Toolchain Initialization](../../../repo-governance/development/workflow/worktree-setup.md))
- [ ] [Add project-specific setup: env vars, DB, Docker, etc.]
- [ ] Verify dev server starts: `nx dev [project-name]`
- [ ] Verify existing tests pass before making changes
```

> **Note**: Worktrees are created at `worktrees/<name>/` in the repo root (not `.claude/worktrees/<name>/`). This is enforced by the `WorktreeCreate` hook. See [Worktree Path Convention](../../../repo-governance/conventions/structure/worktree-path.md) for rationale.

### Fix-All-Issues Instruction

Every plan must include this instruction in quality gate sections:

> **Important**: Fix ALL failures found during quality gates, not just those caused by your
> changes. This follows the root cause orientation principle — proactively fix preexisting
> errors encountered during work.

### Thematic Commit Guidance

Every plan must include commit guidance:

```markdown
### Commit Guidelines

- [ ] Commit changes thematically — group related changes into logically cohesive commits
- [ ] Follow Conventional Commits format: `<type>(<scope>): <description>`
- [ ] Split different domains/concerns into separate commits
- [ ] Do NOT bundle unrelated fixes into a single commit
```

## Manual Behavioral Assertions (Conditional — UI/API Plans)

When the plan touches web UI or API code, delivery plans MUST include manual assertion sections.
**Two hard requirements bind every manual-assertion section:**

1. **Locale coverage** — for a **multi-locale** app, every UI-verification step runs across ALL
   supported locales (e.g. `en` AND `id`), never just the default. Discover the locale set from
   `apps/<app>/src/features/i18n/` or `next.config.ts`. Single-locale verification on a bilingual app
   is INCOMPLETE.
2. **Evidence capture** — every manual-verification step produces a committed artifact: screenshots
   in the plan's `evidence/` subfolder (named `phase-N-<description>-<locale>-<breakpoint>px.png`),
   curl responses inlined in `delivery.md`. See the
   [Evidence Capture Convention](../../../repo-governance/development/quality/evidence-capture.md).

### For Web UI Plans — Playwright MCP

```markdown
### Manual UI Verification (Playwright MCP) — all locales × all breakpoints

- [ ] [AI] Discover supported locales: read `apps/[app]/src/features/i18n/` or `next.config.ts`
- [ ] [AI] Start dev server: `nx dev [project-name]`
- [ ] [AI] For EACH locale × EACH breakpoint (375 / 768 / 1280 px): navigate to the locale-prefixed
      URL (`/en/...`, `/id/...`) via `browser_navigate` + `browser_resize`
- [ ] [AI] Inspect DOM via `browser_snapshot` — verify `html[lang]` matches the locale, no untranslated strings
- [ ] [AI] Test interactive flows via `browser_click` / `browser_fill_form`
- [ ] [AI] Check for JS errors via `browser_console_messages` — must be zero errors per locale
- [ ] [AI] Verify API integration via `browser_network_requests`
- [ ] [AI] Capture one screenshot per locale per breakpoint via `browser_take_screenshot`, saved to
      `evidence/phase-N-[feature]-[locale]-[breakpoint]px.png`
- [ ] [AI] Document evidence in this checklist: reference each screenshot (`![alt](./evidence/...)`)
```

### For API Plans — curl

```markdown
### Manual API Verification (curl)

- [ ] [AI] Start backend server: `nx dev [project-name]`
- [ ] [AI] Verify health endpoint: `curl -s http://localhost:[port]/api/health | jq .` — paste response inline
- [ ] [AI] Verify affected endpoints return expected responses — paste command + status + body inline
- [ ] [AI] Test error cases with invalid payloads — verify proper error responses
- [ ] [AI] For locale-sensitive responses, verify each locale via `Accept-Language` header
- [ ] [AI] Document evidence: inline curl command + status + body (or save responses > 20 lines to `evidence/`)
```

### For Full-Stack Plans — Both + End-to-End

Include both sections above plus an end-to-end flow verification step (per locale).

### For Web-UI Feature-Change Plans — Rule-15 Three-Tester Retest

Near the end of the checklist, before archival: run the three live-site testers (the
`web-ux-test-fixing-planning` workflow: `web-exploratory-tester` + `web-usability-tester` +
`web-design-tester`) against the running target across ALL supported locales; append each finding as
a new unchecked checkbox, source-attributed (`EWT-###`/`UWT-###`/`DWT-###`), and fix (or explicitly
defer) before archival. See
[User-Facing Delivery Hardening Convention](../../../repo-governance/development/quality/user-facing-delivery-hardening.md) Rule 15.

**Not applicable** for plans touching only documentation, governance, CLI/text output, or non-code files.

### For API Feature-Change Plans — Rule-16 API Exploratory Retest

Near the end of the checklist, before archival: run `api-exploratory-tester` (`output-mode: delivery`,
the plan's `plan-path`) against the running REST or GraphQL endpoint(s), with the contract
(OpenAPI 3.x / GraphQL SDL) as ground truth; append each finding as a new unchecked checkbox,
source-attributed (`AET-###`), and — exactly as with the rule-15 web-triad findings — fix every defect
during execution before archival (deferral requires explicit user permission, only when genuinely
impossible; `SG-###` spec-gap proposals may be triaged). The API counterpart is a single specialist
tester (no triad, no dedicated workflow), HTTP/curl-driven, never a browser; a plan changing both a web
UI and its API carries both retest sections. See
[User-Facing Delivery Hardening Convention](../../../repo-governance/development/quality/user-facing-delivery-hardening.md) Rule 16.

**Not applicable** for frontend-only, documentation, governance, CLI/text output, or non-code plans.

## Knowledge Capture (Mandatory Final Phase)

Every substantive plan's `delivery.md` MUST end with a **Knowledge Capture** phase — the final
substantive phase, positioned immediately before the Plan Archival section below — that triages the
plan's transient `learnings.md` running log to durable homes before archival. This Skill emits both
the `learnings.md` scaffold file (created empty in the plan folder alongside `delivery.md`) and the
Knowledge Capture phase itself into every new substantive plan by default.

**`learnings.md` scaffold** — create in the plan folder during Environment Setup, sibling to
`delivery.md`:

```markdown
<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->
```

**Entry shape** (append during execution, the moment something generalizable is noticed — not
reconstructed from memory at the end):

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
```

**Knowledge Capture phase template** (insert as the last substantive phase, immediately before
Plan Archival):

```markdown
## Phase N: Knowledge Capture

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only entries where a durable
      surface would catch this automatically next time; discard the rest with a one-line reason.
- [ ] [AI] Apply the **secret/sensitivity gate** to every surviving entry — sanitize to
      `<placeholder>` tokens or discard if the entry cannot be sanitized without losing its meaning.
- [ ] [AI] Apply the **repo-relevance gate** to every surviving entry — infra-private content stays
      in `ose-infra` only; public-governance content may route to `ose-public`/`ose-primer`; never
      cross-route private content into a public repo.
- [ ] [AI] Route each surviving entry to exactly one durable home. The rubric is open-ended —
      route to whichever surface owns that kind of knowledge (`repo-governance/`, `docs/`,
      `.claude/agents/`, `.claude/skills/`, a post-mortem, or any other durable home), landing a
      small non-code edit inline or filing a `plans/backlog/YYYY-MM-DD__<slug>/` follow-up plan for
      larger non-code work.
- [ ] [AI] **Code-routing rule**: if a learning's home is `apps/`, `libs/`, or tests, file it as a
      separate `plans/backlog/` plan — NEVER land it inline in this plan's commits/PR. The sole
      carve-out is a bug/lint/test failure that blocks THIS plan's own scope — that is fixed inline
      as ordinary Root Cause Orientation work, not routed as a deferred learning.
- [ ] [AI] Record the terminal state of every entry (routed inline / filed as backlog at `<path>` /
      discarded with reason) directly in `learnings.md`.
- [ ] [AI] If execution genuinely surfaced no generalizable learning, record the explicit escape
      `No generalizable learnings — <one-line reason>` instead of individual entries.

### Phase N Gate

> All checks below must pass before starting Plan Archival.

- [ ] [AI] Verify every `learnings.md` entry has reached a terminal state (routed / filed /
      discarded) or the explicit "none" escape is present — no entry left open.
- [ ] [AI] Verify no code-homed learning landed inline — every code-routed learning has a
      corresponding `plans/backlog/` folder.

> **Pause Safety**: all learnings are triaged to durable homes or explicitly discarded; nothing is
> left dangling in `learnings.md`. Safe to stop. To resume: re-check `learnings.md` for any entry
> without a terminal-state marker.
```

**Exemptions**: pure-docs and trivial plans (a one-line rename, a single broken-link fix) MAY skip a
populated `learnings.md` — the explicit "none" escape (or an equivalent note in `delivery.md`)
satisfies the requirement without inventing insight from a change that had none to offer.

See [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
for the authoritative triage rubric, the full candidate-durable-homes table, the litmus test, both
safety gates, and worked PASS/FAIL examples.

## Plan Archival (Mandatory Final Section)

Every delivery plan MUST end with a plan archival section:

```markdown
### Plan Archival

- [ ] Verify ALL delivery checklist items are ticked
- [ ] Verify ALL quality gates pass (local + CI)
- [ ] Verify ALL manual assertions pass with committed evidence in `evidence/` (screenshots + curl output)
- [ ] Verify ALL supported locales were exercised in UI verification (not just the default)
- [ ] Verify every rule-15 EWT/UWT/DWT defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible)
      for EWT/UWT/DWT defect findings; SG-### proposals and USS-### suggestions may be triaged or deferred
- [ ] Verify every rule-16 AET defect finding is fixed (ticked) — deferral requires explicit user permission (only when genuinely impossible)
      for AET defect findings; SG-### spec-gap proposals may be triaged or deferred
- [ ] Move plan folder from `plans/in-progress/` to `plans/done/` via `git mv` (the `evidence/` subfolder moves with it)
- [ ] Update `plans/in-progress/README.md` — remove the plan entry
- [ ] Update `plans/done/README.md` — add the plan entry with completion date
- [ ] Update any other READMEs that reference this plan
- [ ] Commit: `chore(plans): move [plan-name] to done`
```

## Common Mistakes

### Mistake 1: Missing acceptance criteria

**Wrong**: Plan without Gherkin scenarios
**Right**: Every plan has concrete acceptance criteria

### Mistake 2: Vague requirements

**Wrong**: "Improve system performance"
**Right**: "Reduce API response time to <200ms for 95th percentile"

### Mistake 3: No progress tracking

**Wrong**: Never updating delivery checklist
**Right**: Mark items complete with implementation notes

### Mistake 4: Wrong folder placement

**Wrong**: Active work in backlog/
**Right**: Move to in-progress/ when starting work

### Mistake 5: Code delivery items without TDD shape

**Wrong**: Combining implementation and test into one checkbox

```markdown
- [ ] Implement email validation with tests
```

**Right**: Separate RED, GREEN, REFACTOR phases as independent checkboxes

```markdown
- [ ] **RED**: Write failing test for email validation in `libs/ts-utils/src/validation.test.ts`
      — command: `nx run ts-utils:test:unit`
      — acceptance: test fails with "validateEmail is not defined"
- [ ] **GREEN**: Implement `validateEmail` in `libs/ts-utils/src/validation.ts`
      — command: `nx run ts-utils:test:unit`
      — acceptance: test passes, no other tests broken
- [ ] **REFACTOR**: Extract regex constant, improve naming
      — command: `nx run ts-utils:test:unit`
      — acceptance: all tests still pass
```

`plan-checker` flags combined TDD items as HIGH severity findings.

## References

**Primary Convention**: [Plans Organization Convention](../../../repo-governance/conventions/structure/plans.md)

**Related Conventions**:

- [No Secrets in Git Convention](../../../repo-governance/conventions/security/no-secrets-in-committed-files.md) - Hard iron rule: no system secret (keys, passwords, tokens, connection strings, etc.) may appear in any committed plan file. Use placeholders or env-var references instead.
- [Grilling-With-Options Convention](../../../repo-governance/development/workflow/grilling-with-options.md) - Every grill question MUST present 2-4 concrete options; open-ended questions are FORBIDDEN; one option marked recommended; interactive multiple-choice tool preferred
- [Test-Driven Development Convention](../../../repo-governance/development/workflow/test-driven-development.md) - Mandates TDD (Red→Green→Refactor) for all code changes; defines the required RED/GREEN/REFACTOR three-substep shape for delivery checklists; includes HARD RULE against combining phases into one checkbox
- [Plan Anti-Hallucination Convention](../../../repo-governance/development/quality/plan-anti-hallucination.md) - Pre-write verification recipes, repo-grounding rule, refuse-on-uncertainty, anti-pattern catalog (AP-1 through AP-10), specialized-executor annotation
- [Trunk Based Development](../../../repo-governance/development/workflow/trunk-based-development.md) - Git workflow (all development targets `main`; see [Delivery Mode](#delivery-mode-mandatory--applies-to-all-plans) above for how a plan reaches `main` — `worktree-to-pr` is the default, direct push is one of the other three modes)
- [PR Merge Protocol](../../../repo-governance/development/workflow/pr-merge-protocol.md) - Explicit approval required, all quality gates must pass
- [Feature Change Completeness](../../../repo-governance/development/quality/feature-change-completeness.md) - Specs, contracts, and tests must update with every feature change
- [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md) - The mandatory final `learnings.md` triage phase: open-ended principle-based routing rubric, the code-routing rule (code-homed learnings always become a separate `plans/backlog/` plan), and the two safety gates (secret/sensitivity, repo-relevance)
- [Manual Behavioral Verification](../../../repo-governance/development/quality/manual-behavioral-verification.md) - Playwright MCP for UI, curl for API; ALL locales for multi-locale apps
- [Evidence Capture Convention](../../../repo-governance/development/quality/evidence-capture.md) - Screenshots to the plan's `evidence/` subfolder (named by phase/locale/breakpoint), curl responses inlined in `delivery.md`, ALL supported locales covered
- [CI Blocker Resolution](../../../repo-governance/development/quality/ci-blocker-resolution.md) - Preexisting CI failures must be fixed, never bypassed
- [Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria.md) - Gherkin format details
- [File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md) - Naming standards

**Related Skills**:

- `grill-me` - Mandatory pre-write and post-write grilling; every question presents 2-4 concrete options
- `plan-writing-gherkin-criteria` - Detailed Gherkin guidance
- `repo-practicing-trunk-based-development` - Git workflow
- `docs-applying-content-quality` - Universal content standards

---

This Skill packages project planning standards for creating structured, executable plans with clear acceptance criteria. For comprehensive details, consult the primary convention document.
