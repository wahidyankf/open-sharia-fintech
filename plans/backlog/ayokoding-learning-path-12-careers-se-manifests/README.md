# Learning Path Manifests — the three `software-engineer`-role `careers/` manifests

## Delivery amendment — one final PR and Plan 13 handoff

This plan uses one branch and its sole PR in Phase 10, after verification and Knowledge Capture; the
archival move, review cycle, CI, merge, and deploy are all in that final delivery. The former
intermediate Plan 12→13 merge handoff is removed. Plan 13 may deliver its independent manifest
first, then Plan 12 consumes that merged state for its four-manifest check before its final PR.
Earlier per-manifest or delivery-boundary PR wording is superseded.

> **Successor plan.** This plan and its sibling
> [`ayokoding-learning-path-13-careers-ai-manifest`](../ayokoding-learning-path-13-careers-ai-manifest/README.md)
> together replace the single prior plan that authored, published, grew, and verified all four
> `careers/` path manifests. That prior plan covered `interview-ready`, `immediately-effective`
> (both `software-engineer` and `ai-engineer`), and `fundamentally-strong` in one folder. It is split
> here into **3 + 1**: this plan owns the **three `software-engineer`-role manifests**
> (`interview-ready`, `immediately-effective/software-engineer`, `fundamentally-strong/software-engineer`);
> the sibling plan owns the **one `ai-engineer` manifest**
> (`immediately-effective/ai-engineer`) alone. See [§Why 3 + 1, not 2 + 2](#why-3--1-not-2--2) below
> for why the split is not symmetric.
>
> **Programme decisions** — this plan cites the shared `R*`/`A*` decision ids `R2`, `R4`, `R9`, `A2`,
> `A8`, `A10`, `A11`, and `A12`; their definitions are folded into
> [tech-docs §Programme decisions](./tech-docs.md#programme-decisions). `A8` (programme-wide
> clean-room licensing) governs every landing-prose authoring step in this plan — Phases 1.2, 2.2, and
> 3.2 — and is invoked there explicitly rather than assumed.

**Category scope.** The paths hub serves two categories at different URL depths:
`careers/<arc>/<role>` (3 segments, 4 paths total, split across this plan and its sibling) and
`skills/<subject>` (2 segments, 4 paths, owned by a separate accounting/ERP split — see
[§Depends-on](#depends-on)). This plan is **`careers/`-software-engineer-role-only**; "three
manifests" in this plan always means the three `software-engineer`-role manifests, never the whole
four-path `careers/` category and never the eight-path programme.

Three manifests ship here, in the DD-27 build order:

1. `careers/interview-ready/software-engineer` — the architecture smoke test, published over
   already-live re-homed content. **Ships first** — its delivery unit merging is what unblocks the
   sibling AI-manifest plan's own start (see [§The plan-12 / plan-13 coupling](#the-plan-12--plan-13-coupling-non-circular-by-construction)
   below).
2. `careers/immediately-effective/software-engineer` — the build-app-first arc.
3. `careers/fundamentally-strong/software-engineer` — the university-style theory-first arc.

The fourth `careers/` manifest, `careers/immediately-effective/ai-engineer`, is authored entirely by
the sibling plan `ayokoding-learning-path-13-careers-ai-manifest` — this plan never touches it.

## Why 3 + 1, not 2 + 2

Splitting the original single plan's four manifests into two equal-sized folders (2+2) looks like the
natural cut, but the manifests do not divide that way. Three cross-manifest checks bind specifically
across the **three `software-engineer`-role manifests** — never the AI-engineer manifest:

- **"No forked body" check.** `Given a course appears in all three of the interview-ready,
immediately-effective/software-engineer, and fundamentally-strong/software-engineer manifests ...
Then exactly one canonical path-neutral body exists` — first satisfiable only once all three
  software-engineer manifests exist, which happens entirely inside this plan.
- **Band-9 growth.** The five interview-technique course IDs land in **two** of the three
  software-engineer manifests only (`interview-ready` and `fundamentally-strong`;
  `immediately-effective/software-engineer` omits them by design — see
  [tech-docs DD-41](./tech-docs.md#design-decisions)) — a genuine same-plan, multi-manifest atomic
  operation.
- **Ownership-boundary sweep** ("no forked body across the three software-engineer paths") at this
  plan's own verification phase.

The AI-engineer manifest has its own independent growth track (the nine-course AI/harness cluster) and
is not part of any of the three checks above. So the split is **3 + 1**: this plan owns the three
software-engineer manifests and every 3-way cross-manifest check; the sibling plan owns the
AI-engineer manifest alone. **One check spans all four manifests** — see below.

## The plan-12 / plan-13 coupling (non-circular by construction)

One cross-manifest check — "a shared course names every path that includes it" — spans **all four**
`careers/` manifests, so it cannot live entirely in either plan. It belongs in whichever plan finishes
**last**. Per DD-27's locked build order (interview-ready ships first → the AI-engineer path is
authoring priority #1 → immediately-effective/software-engineer → fundamentally-strong/software-engineer),
this plan's fundamentally-strong phase is the last **manifest-authoring** phase to ship, and this
plan's growth phase runs longest — so this plan finishes the whole four-manifest product last. **The
four-manifest check therefore lives in this plan, as its own final phase**, run only after **both**
this plan's own three manifests **and** the sibling AI-manifest plan are fully merged.

Plan 13 starts independently because the manifest file subtrees are disjoint. It merges its sole
final PR first. This plan's Phase 8 is then `blockedBy` that whole merged Plan 13 delivery, allowing
the all-four-manifest check to run before this plan's own sole final PR. There is no partial
intermediate-PR handoff and therefore no cycle.

```mermaid
%% The plan-12 / plan-13 coupling, shown as a sequence to make the non-circularity explicit.
%% Time flows top to bottom. Every arrow points forward in time — there is no arrow pointing backward.
sequenceDiagram
    autonumber
    participant P12 as Plan 12 (this plan)<br/>3 SE manifests
    participant P13 as Plan 13 (sibling)<br/>1 AI manifest

    Note over P13: Phases 0-6 — author, grow, verify, retest
    P13->>P13: Phase 7 — archive, sole PR, merge
    P13-->>P12: merged AI-engineer manifest unblocks Phase 8
    Note over P12: Phases 1-7 — author and verify three SE manifests
    P12->>P12: Phase 8 — four-manifest cross-check
    P12->>P12: Phases 9-10 — Knowledge Capture, archive, sole PR, merge
```

**Accessibility note.** The diagram is a `sequenceDiagram`, whose reading order (top to bottom, arrows
always pointing down or to a later point in time) is itself the accessibility device — there is no
color-coding to substitute for reading order, and no arrow in this diagram points upward, which is the
structural proof of non-circularity a reader can verify by inspection.

## The manifest ownership invariant (now scoped per plan, within the `careers/` category)

_Binding — and the reason this plan and its sibling exist as separate units from course-authoring._

**This plan owns every file under `apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/`,
`.../careers/immediately-effective/software-engineer.yaml`, and
`.../careers/fundamentally-strong/software-engineer.yaml`, plus every step that creates, appends to,
reorders, or re-verifies one of those three manifests.**
`ayokoding-learning-path-13-careers-ai-manifest` owns exactly
`.../careers/immediately-effective/ai-engineer.yaml` under the identical invariant, scoped to its own
one manifest. Neither plan touches the other's manifest file. The seven course-authoring successor
plans (`ayokoding-learning-path-04` through `-11`, per the mapping in
[tech-docs §Growth signal routing](./tech-docs.md#growth-signal-routing-from-the-seven-course-authoring-successor-plans))
own course **bodies only** and never edit a manifest under either plan's scope.

A genuine dependency cycle existed between course-authoring and manifest-authoring before this
invariant was ruled (in the plan this split replaces): course-authoring's backfill phases grow
manifests the manifest plan(s) author, while the manifest plan's AI-path phase publishes a manifest
over courses course-authoring writes. No wave ordering satisfies both directions — only the ownership
invariant breaks it, which is why this plan's hard prerequisite includes both Wave-2 plans
(`ayokoding-learning-path-03-navigation-ui` and, transitively via growth, the seven course-authoring
successor plans) rather than the navigation plan alone.

Its mechanical consequence: growth steps that the original single course-authoring plan would have
performed are instead recorded as **band-completion signals** in each of the seven course-authoring
successor plans' own `delivery.md` files, and this plan's [Phase 4](./delivery.md#phase-4-manifest-growth-as-backfill-lands)
performs the growth for its own three manifests as each signal arrives.

## Scope

**In scope**

- Three `careers/`-`software-engineer`-role `PathManifest` YAML data files under
  `apps/ayokoding-www/src/features/course-paths/manifests/careers/`.
- Three thin content landing anchors under
  `apps/ayokoding-www/content/en/learn/paths/careers/<arc>/software-engineer/_index.md` (prose/SEO
  only — no `courseOrder`).
- **This plan's slice** of the paths-hub card population — three cards, one per manifest as it ships,
  inside the category-grouped hub layout `ayokoding-learning-path-03-navigation-ui` owns. The fourth
  `careers/` card (`ai-engineer`) is the sibling plan's own addition to the same shared file.
- Manifest integrity + prerequisite-consistency + no-forked-body verification at every phase gate,
  scoped to this plan's three manifests (plus, at the final phase only, the full four-manifest check
  once the sibling plan has merged).
- Per-path progression-smoothness audits for all three manifests, including the interview-ready
  refresh-register re-audit deferred by the smoke-test phase.
- All growth of these three manifests as the seven course-authoring successor plans land their bands.
- The **four-manifest** "a shared course names every path" check and the terminal 127-course catalog
  assertion — both run at this plan's own final phase, since this plan is the last of the two to
  finish (see [§The plan-12 / plan-13 coupling](#the-plan-12--plan-13-coupling-non-circular-by-construction)).

**Out of scope**

- The `careers/immediately-effective/ai-engineer` manifest, its landing, and its hub card — owned
  entirely by `ayokoding-learning-path-13-careers-ai-manifest`.
- Any course **body** — authored by the seven course-authoring successor plans.
- The `PathManifest` zod schema, the pure `course-paths` core modules, the `<MANIFESTS>` directory
  itself, and the `syllabus/` detail layer — owned by
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- Every rendering component (`path-landing.tsx`, `path-card.tsx`, `path-rail.tsx`,
  `manifest-repository.ts`, `?path=` wiring) — owned by `ayokoding-learning-path-03-navigation-ui`.
- The flat `courses/` namespace, the `legacy/` bucket, and both redirect modules — owned by
  `ayokoding-learning-path-01-url-restructure`.
- The `skills/` category's four manifests — owned end-to-end by the accounting/ERP split plans (see
  [§Depends-on](#depends-on)).
- The `apps/ayokoding-www` root-layout dynamic-API removal, middleware deletion, and static-conversion
  work — owned by `vercel-function-cost-reduction` (see [§Depends-on](#depends-on)); this plan's
  landing pages and hub cards land on top of that app once it has merged.

## Where this plan sits

```mermaid
%% Dependency position of this plan and its sibling within the programme.
%% Node SHAPE encodes kind: rectangle = foundational/infra plan, stadium = course-authoring successor,
%% hexagon = this split's two manifest plans.
%% Edge STYLE encodes strength: solid = hard blocking edge, dotted = partial/staged edge.
flowchart LR
    subgraph F["Foundational (done)"]
        P1["url-restructure"]:::done
        P2["schema-and-prerequisite-dag"]:::done
        P3["navigation-ui"]:::done
    end
    subgraph CA["Seven course-authoring successor plans (04-11, in flight)"]
        CA1["04 · Band 1,2 + 6 AI courses"]:::ca
        CA2["05 · platform-and-concurrency"]:::ca
        CA3["06 · architecture-<br/>and-ai-harness"]:::ca
        CA4["07 · low-level-systems"]:::ca
        CA5["08 · security-and-ops"]:::ca
        CA6["09 · interview-technique"]:::ca
        CA7["10 · jvm-and-build-your-own"]:::ca
        CA8["11 · capstones"]:::ca
    end
    subgraph THIS["This split"]
        P12{{"12 · careers-se-manifests<br/>THIS PLAN"}}:::this
        P13{{"13 · careers-ai-manifest"}}:::sibling
    end
    VFC["vercel-function-cost-reduction"]:::infra

    P1 --> P12
    P2 --> P12
    P3 --> P12
    CA1 -.->|"growth signals"| P12
    CA2 -.->|"growth signals"| P12
    CA3 -.->|"growth signals"| P12
    CA4 -.->|"growth signals"| P12
    CA5 -.->|"growth signals"| P12
    CA6 -.->|"growth signals"| P12
    CA7 -.->|"growth signals"| P12
    CA8 -.->|"growth signals"| P12
    CA1 -.->|"growth signals"| P13
    CA3 -.->|"growth signals"| P13
    CA8 -.->|"growth signals"| P13
    VFC --> P12
    VFC --> P13
    P13 -.->|"whole plan merged"| P12

    classDef done fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef ca fill:#DE8F05,stroke:#000000,color:#000000
    classDef this fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:4px
    classDef sibling fill:#029E73,stroke:#000000,color:#FFFFFF
    classDef infra fill:#CC78BC,stroke:#000000,color:#000000
```

**Accessibility note.** Group membership is carried by the four labelled subgraph containers and by
node shape (rectangle = foundational, stadium = course-authoring successor, hexagon = this split's two
manifest plans) as well as by fill; this plan's node additionally carries a thicker border. Edge kind
is carried by line style (solid = hard blocking edge; dotted = partial/staged or signal-only edge) and
by edge labels. Fills use the verified accessible palette (`#0173B2` blue, `#DE8F05` orange, `#029E73`
teal, `#CC78BC` purple) with black borders and WCAG-AA-contrasting text, per the
[Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md).

## Delivery flow

```mermaid
%% Delivery stages for this plan. Node SHAPE encodes kind: rectangle = setup,
%% stadium = publishing/growth, hexagon = terminal/archival. Colours are redundant with shape.
%% TD required: the chain is 6 nodes deep, so LR depth would exceed MaxWidth=4.
flowchart TD
    S0["Stage A<br/>Phase 0<br/>baseline"]:::setup
    S1(["Stage B<br/>Phases 1-3<br/>publish 3 manifests"]):::manifest
    S2(["Stage C<br/>Phase 4<br/>grow to full arcs"]):::manifest
    S3(["Stage D<br/>Phases 5-7<br/>verify, retest, integrate"]):::verify
    S4{{"Stage E<br/>Phase 8<br/>four-manifest cross-check"}}:::cross
    S5{{"Stage F<br/>Phases 9-10<br/>capture, archive"}}:::archive

    S0 -->|"gate: baseline green"| S1
    S1 -->|"gate: 3 manifests, 3 hub cards"| S2
    S2 -->|"gate: full 3-manifest arcs"| S3
    S3 -->|"gate: automated + Rule-15 green"| S4
    S4 -->|"gate: plan 13 fully merged, 4-manifest check green"| S5

    classDef setup fill:#56B4E9,stroke:#000000,color:#000000
    classDef manifest fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef verify fill:#DE8F05,stroke:#000000,color:#000000
    classDef cross fill:#CC78BC,stroke:#000000,color:#000000
    classDef archive fill:#029E73,stroke:#000000,color:#FFFFFF
```

Inside Stage B the three manifest phases are **strictly serial**, in DD-27's locked order.

| Phase | Manifest published                                | Closing gate                                                                                   |
| ----- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| 1     | `careers/interview-ready/software-engineer`       | architecture proven; 1 manifest, 1 hub card; unblocks plan 13                                  |
| 2     | `careers/immediately-effective/software-engineer` | 2 manifests, 2 hub cards; arcs provably distinct                                               |
| 3     | `careers/fundamentally-strong/software-engineer`  | 3 manifests, 3 hub cards; no forked body across the three                                      |
| 4     | _(growth only)_                                   | full three-manifest arcs; this plan's own catalog contribution resolves                        |
| 5     | —                                                 | all automated sweeps green; ownership boundary intact                                          |
| 6     | —                                                 | 9 screenshots committed (3 landings + hub slice); zero open defects                            |
| 7     | —                                                 | CI green on `main`; production serving this plan's 3 paths                                     |
| 8     | —                                                 | plan 13 fully merged; all four manifests live; four-manifest check green; 127-catalog resolves |
| 9     | —                                                 | every `learnings.md` entry terminal                                                            |
| 10    | —                                                 | archived                                                                                       |

**Stage groupings above describe verification, not delivery boundaries.** See
[delivery.md §Delivery Boundaries](./delivery.md#delivery-boundaries) for the authoritative mapping of
phases to delivery units, branches, and PRs.

## Depends-on

| Direction   | Plan (full folder name)                                                   | Relationship                                                                                                                       |
| ----------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `blockedBy` | `ayokoding-learning-path-03-navigation-ui`                                | hard — merged to `origin/main` first (done)                                                                                        |
| `blockedBy` | `ayokoding-learning-path-01-url-restructure`                              | transitive, via the navigation plan (done)                                                                                         |
| `blockedBy` | `ayokoding-learning-path-02-schema-and-prerequisite-dag`                  | transitive, via the navigation plan (done)                                                                                         |
| `blockedBy` | `ayokoding-learning-path-04-course-authoring` (Bands 1,2 + Phase 1)       | hard for this plan's own growth — Bands 1,2 must land before Phase 4.1 processes them                                              |
| `blockedBy` | `ayokoding-learning-path-05-course-authoring-platform-and-concurrency`    | hard for growth — old Band 3+4                                                                                                     |
| `blockedBy` | `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` | hard for growth — old Band 5 (this plan's SE-manifest slice only; the AI-manifest slice is plan 13's)                              |
| `blockedBy` | `ayokoding-learning-path-07-course-authoring-low-level-systems`           | hard for growth — old Band 6 (half)                                                                                                |
| `blockedBy` | `ayokoding-learning-path-08-course-authoring-security-and-ops`            | hard for growth — old Band 7                                                                                                       |
| `blockedBy` | `ayokoding-learning-path-09-course-authoring-interview-technique`         | hard for growth — old Band 9 (two-of-three growth into this plan's manifests)                                                      |
| `blockedBy` | `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`      | hard for growth — old Band 6 (other half)                                                                                          |
| `blockedBy` | `ayokoding-learning-path-11-course-authoring-capstones`                   | hard for growth — old Band 8 (this plan's SE-manifest slice; also grows plan 13's AI manifest independently)                       |
| `blockedBy` | `vercel-function-cost-reduction`                                          | hard, new — see [§Vercel cost-reduction dependency](#vercel-cost-reduction-dependency-hard-both-plans) below                       |
| `blockedBy` | `ayokoding-learning-path-13-careers-ai-manifest` (**whole-plan**)         | Phase 8's four-manifest cross-check begins only after Plan 13's sole final PR merges; Plan 13 has no start dependency on this plan |
| _(no edge)_ | `ayokoding-learning-path-14`/`-15`/`-16` (the `skills/`-accounting split) | **disjoint category subtree** — `careers/` vs `skills/`; no shared file. Confirmed explicitly, not merely absent from this table.  |
| _(no edge)_ | `ayokoding-learning-path-17`/`-18` (the `skills/`-ERP split)              | **disjoint category subtree** — same confirmation as above.                                                                        |

### Vercel cost-reduction dependency (hard, both plans)

[`plans/done/2026-08-02__vercel-function-cost-reduction/`](../../done/2026-08-02__vercel-function-cost-reduction/README.md)
fixes `apps/ayokoding-www`'s root layout (removes the `await headers()` call that opts every route
into dynamic rendering) and its content route (`?path=` reading moves client-side), then deletes the
now-purposeless middleware and converts static-eligible routes. **Treated here as already merged/done,
per explicit direction** — this plan's landing pages and hub cards land in the same app whose
layout and middleware that plan changes, so authoring against a pre-fix tree would mean every page
this plan adds inherits the dynamic-rendering cost the other plan is actively removing, and a
mid-flight merge of that plan underneath this one would silently change every route's rendering mode
without this plan's own gates re-verifying it.

**Concrete checkable signal**:
`gh pr list --search "vercel-function-cost-reduction" --state merged --json number --jq 'length'`
returns a value ≥ 1 (its `ayokoding-www` delivery unit, Phases 1-4, specifically). Falsifiable both
ways: returns `0` while that plan's `ayokoding-www` unit is still open.

### Disjoint-subtree confirmation

`careers/` and `skills/` are separate first-URL-segments under
`apps/ayokoding-www/src/features/course-paths/manifests/` and separate first-URL-segments under
`apps/ayokoding-www/content/en/learn/paths/`. The only file the two category subtrees share is the
paths-hub's `<PATHS>_index.md`, and even there each plan's edits are additive to a **different**
category group inside a category-grouped layout (never the same sub-group). Neither this plan nor its
sibling reads, writes, or asserts anything about a `skills/*.yaml` manifest or a `skills/` landing.
This is stated explicitly here, rather than left as a silent absence from the table above, because a
shared top-level file (`<PATHS>_index.md`) is exactly the kind of surface a future reader might
mistake for a hidden coupling.

## Recorded judgment calls

### JC-3: numbering continuity, not renumbering, across the split

The prior single plan this split replaces was folder-named `ayokoding-learning-path-05-manifests`.
That numeral is now occupied by a course-authoring successor plan
(`ayokoding-learning-path-05-course-authoring-platform-and-concurrency`), so this split could not reuse
`05`. **Choice**: this plan and its sibling take the next free numerals in sequence, `12` and `13`,
rather than renumbering any already-in-flight sibling plan to make room. **Reason**: renumbering a
plan folder that other in-flight plans already cite by name (band-completion signals, cross-links)
would break every existing cross-reference at once; taking the next free numerals costs nothing and
disturbs no sibling plan's own text.

### JC-4: the Band-9 two-of-three correction is adopted, not re-derived

The plan this split replaces contained an internal inconsistency: its own `delivery.md` Phase 5.2 grew
Band 9's five interview-technique courses into **all three** software-engineer manifests, while its
sibling course-authoring plan's README summary table described the same growth as landing in
**`interview-ready` + `fundamentally-strong` only**. This split adopts the **two-of-three** reading as
authoritative — see [tech-docs DD-41](./tech-docs.md#design-decisions) for the full resolution and the
falsifiable check that makes the correction auditable rather than asserted.

## Delivery Mode: worktree-to-pr

This plan has exactly one dedicated worktree, one persistent final-delivery branch, and one PR.
All authoring, verification, and Knowledge Capture phases commit on that branch without a push, PR,
review cycle, merge, or deployment. In Phase 10, the executor commits the archival move and
any index updates, opens the sole draft PR, completes the PR-Review Maker→Fixer Cycle and CI gates,
marks it ready, and performs the normal AI merge/deploy after the hardened preconditions hold.
No per-course, cohort, stage, or phase worktree/branch/PR is permitted.

## Navigation

- [Business Requirements (brd.md)](./brd.md) — WHY the three software-engineer manifests are their own
  deliverable and who they serve.
- [Product Requirements (prd.md)](./prd.md) — the personas, user stories, Gherkin acceptance criteria,
  and product scope.
- [Technical Docs (tech-docs.md)](./tech-docs.md) — the ownership invariant, the manifest format and
  integrity invariants, the design decisions (including the new DD-40/DD-41/DD-42 this split adds),
  the growth-signal routing table, and the architecture diagrams.
- [Delivery Checklist (delivery.md)](./delivery.md) — the phased executable checklist.
- [Learnings (learnings.md)](./learnings.md) — knowledge-capture running log.
- [Sibling plan — `ayokoding-learning-path-13-careers-ai-manifest`](../ayokoding-learning-path-13-careers-ai-manifest/README.md)
  — the fourth `careers/` manifest, coupled to this plan as described above.
- [Syllabus (cross-plan, read-only)](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md) —
  the per-course and per-path detail layer. The three `paths/` manifest mirrors this plan transcribes
  from are
  [`manifest-interview-ready-software-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-interview-ready-software-engineer.md),
  [`manifest-immediately-effective-software-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-software-engineer.md),
  and
  [`manifest-fundamentally-strong-software-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-fundamentally-strong-software-engineer.md).
