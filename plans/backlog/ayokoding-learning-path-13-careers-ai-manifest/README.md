# Learning Path Manifest — the `careers/immediately-effective/ai-engineer` manifest

## Delivery amendment — one final PR and independent start

This plan uses one branch and its sole PR in Phase 7, after verification and Knowledge Capture; the
archival move, secret scan, local quality checks, PR quality gate, merge, and deploy are all in that final delivery. It no longer waits
for an intermediate Plan 12 merge: its manifest ownership is disjoint, and Plan 12 consumes this
plan only after this final PR merges. Earlier delivery-boundary wording is superseded.

> **Successor plan.** This plan and its sibling
> [`ayokoding-learning-path-12-careers-se-manifests`](../ayokoding-learning-path-12-careers-se-manifests/README.md)
> together replace the single prior plan that authored, published, grew, and verified all four
> `careers/` path manifests. The sibling owns the three `software-engineer`-role manifests
> (`interview-ready`, `immediately-effective/software-engineer`, `fundamentally-strong/software-engineer`).
> **This plan owns exactly one manifest**: `careers/immediately-effective/ai-engineer`. See
> [the sibling's README §Why 3 + 1, not 2 + 2](../ayokoding-learning-path-12-careers-se-manifests/README.md#why-3--1-not-2--2)
> for why the split is not symmetric.
>
> **Programme decisions** — this plan cites the shared `R*`/`A*` decision ids `R2`, `R4`, `R9`, `A8`;
> their definitions are folded into
> [tech-docs §Programme decisions](./tech-docs.md#programme-decisions). `A8` (programme-wide
> clean-room licensing) governs this plan's one landing-prose authoring step (Phase 1.2).

**Category scope.** The paths hub serves two categories: `careers/<arc>/<role>` (3 segments, 4 paths —
3 owned by the sibling plan, 1 owned here) and `skills/<subject>` (2 segments, 4 paths, owned by a
separate accounting/ERP split, disjoint subtree — see [§Depends-on](#depends-on)). This plan is
**one manifest only** — the sole `careers/` product with a distinct, non-software-engineering
endpoint.

The `careers/immediately-effective/ai-engineer` path is a genuine **from-scratch** AI-engineering path
(renamed and re-scoped 2026-07-21 from an earlier role-transition framing): it assumes **no** prior
software-engineering competence, **includes** the shared SWE-fundamentals prerequisite courses at the
head of `courseOrder` rather than linking them out, and teaches **building** AI systems (models,
agents, evals, inference serving) — not driving them (`agentic-coding` stays a separate, unrelated
axis). It **walks** (includes, never links) the nine-course AI/harness cluster.

Per DD-27's locked build order, authoring this path is **priority #1** for all authoring effort,
immediately behind the sibling plan's architecture-smoke-test-only interview-ready MVP.

## The plan-12 / plan-13 coupling (non-circular by construction)

One check — "a shared course names every path that includes it" — spans **all four** `careers/`
manifests and cannot resolve inside either plan alone. It lives in the sibling plan's own **final**
phase, since the sibling plan finishes the whole four-manifest product last (its fundamentally-strong
phase is the last manifest-authoring step in DD-27's build order, and its growth phase runs longest).
Plan 13 begins only after plan 12's merged delivery. Its manifest remains in a disjoint file subtree, but that ownership boundary does not remove the linear execution prerequisite. It finishes and merges its sole final PR first. Plan 12's Phase 8 then
performs the all-four-manifest check against that merged state before Plan 12 opens its own final PR.
The relationship is therefore one ordered handoff, not a two-way staged dependency.

```mermaid
%% The plan-12 / plan-13 coupling, from this plan's (plan 13's) point of view.
%% Time flows top to bottom. Every arrow points forward in time.
sequenceDiagram
    autonumber
    participant P12 as Plan 12 (sibling)<br/>3 SE manifests
    participant P13 as Plan 13 (this plan)<br/>1 AI manifest

    Note over P13: Phases 0-6 — author, grow, verify, retest
    P13->>P13: Phase 7 — archive, sole PR, merge
    P13-->>P12: merged AI-engineer manifest unblocks Phase 8
    Note over P12: Phases 1-7 — author and verify three SE manifests
    P12->>P12: Phase 8 — four-manifest cross-check
    P12->>P12: Phases 9-10 — Knowledge Capture, archive, sole PR, merge
```

**Accessibility note.** As in the sibling's copy of this diagram, reading order (top to bottom, every
arrow pointing forward in time) is the accessibility device — no arrow points upward, which is the
structural proof of non-circularity.

## The manifest ownership invariant (scoped to this plan's one file)

_Binding._ **This plan owns exactly**
`apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/ai-engineer.json`,
plus every step that creates, appends to, reorders, or re-verifies it. The sibling plan owns exactly its
three software-engineer-role files under the identical invariant. Neither plan edits the other's
manifest. The seven course-authoring successor plans own course **bodies only** and never edit either
plan's manifest.

## Scope

**In scope**

- The one `careers/immediately-effective/ai-engineer` `PathManifest` JSON manifest data file under
  `apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/`.
- Its thin content landing anchor at
  `apps/ayokoding-www/content/en/learn/paths/careers/immediately-effective/ai-engineer/_index.md`
  (prose/SEO only — no `courseOrder`).
- This plan's **one-card** slice of the paths-hub card population, inside the category-grouped hub
  layout `ayokoding-learning-path-03-navigation-ui` owns.
- Manifest integrity + prerequisite-consistency verification at every phase gate, scoped to this one
  manifest.
- The from-scratch progression-smoothness audit.
- All growth of this one manifest as the AI/harness cluster lands (from `ayokoding-learning-path-06`
  and `-11`'s own signals).

**Out of scope**

- The three `software-engineer`-role manifests, their landings, and their hub cards — owned entirely by
  `ayokoding-learning-path-12-careers-se-manifests`.
- The four-manifest "a shared course names every path" check and the terminal 127-course catalog
  assertion — both are the sibling plan's own final-phase responsibility (this plan's own manifest
  merely needs to exist for that check to run, but this plan does not perform the check itself).
- Any course **body** — authored by the seven course-authoring successor plans.
- The `PathManifest` zod schema, the pure `course-paths` core modules, the `<MANIFESTS>` directory
  itself, and the `syllabus/` detail layer — owned by
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- Every rendering component — owned by `ayokoding-learning-path-03-navigation-ui`.
- The flat `courses/` namespace, the `legacy/` bucket, and both redirect modules — owned by
  `ayokoding-learning-path-01-url-restructure`.
- The `skills/` category's four manifests — disjoint category subtree, no shared file.
- The `apps/ayokoding-www` root-layout dynamic-API removal, middleware deletion, and static-conversion
  work — owned by `vercel-function-cost-reduction`.

## Where this plan sits

```mermaid
%% Dependency position of this plan and its sibling within the programme.
%% Node SHAPE encodes kind: rectangle = foundational/infra plan, stadium = course-authoring successor,
%% hexagon = this split's two manifest plans.
flowchart LR
    subgraph F["Foundational (done)"]
        P1["url-restructure"]:::done
        P2["schema-and-prerequisite-dag"]:::done
        P3["navigation-ui"]:::done
    end
    subgraph CA["Completed baseline and successor plans feeding THIS plan"]
        CA1["04 · Phase 1<br/>6 AI courses — done"]:::done
        CA3["06 · architecture-<br/>and-ai-harness<br/>(8 of 9 harness courses)"]:::ca
        CA8["11 · capstones<br/>(9th harness-cluster course)"]:::ca
    end
    subgraph THIS["This split"]
        P12{{"12 · careers-se-manifests<br/>sibling"}}:::sibling
        P13{{"13 · careers-ai-manifest<br/>THIS PLAN"}}:::this
    end
    VFC["vercel-function-cost-reduction"]:::infra

    P1 --> P13
    P2 --> P13
    P3 --> P13
    CA1 -.->|"6 AI-engineer-role courses"| P13
    CA3 -.->|"8 harness-cluster courses"| P13
    CA8 -.->|"9th harness-cluster course"| P13
    VFC --> P13
    P13 -.->|"whole plan merged"| P12

    classDef done fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef ca fill:#DE8F05,stroke:#000000,color:#000000
    classDef this fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:4px
    classDef sibling fill:#029E73,stroke:#000000,color:#FFFFFF
    classDef infra fill:#CC78BC,stroke:#000000,color:#000000
```

**Accessibility note.** Group membership is carried by the labelled subgraph containers and by node
shape as well as by fill; this plan's node carries a thicker border. Edge kind is carried by line style
(solid = hard blocking, dotted = partial/staged or signal-only) and by edge labels. Fills use the
verified accessible palette (`#0173B2` blue, `#DE8F05` orange, `#029E73` teal, `#CC78BC` purple) with
black borders and WCAG-AA-contrasting text, per the
[Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md).

## Delivery flow

```mermaid
%% TD required: the chain is 5 nodes deep, so LR depth would exceed MaxWidth=4.
flowchart TD
    S0["Stage A<br/>Phase 0<br/>baseline"]:::setup
    S1(["Stage B<br/>Phase 1<br/>publish manifest"]):::manifest
    S2(["Stage C<br/>Phase 2<br/>grow to full composition"]):::manifest
    S3(["Stage D<br/>Phases 3-5<br/>verify, retest, integrate"]):::verify
    S4{{"Stage E<br/>Phases 6-7<br/>capture, archive"}}:::archive

    S0 -->|"gate: baseline green"| S1
    S1 -->|"gate: manifest live, 1 hub card"| S2
    S2 -->|"gate: full harness-cluster composition"| S3
    S3 -->|"gate: automated + Rule-15 green"| S4

    classDef setup fill:#56B4E9,stroke:#000000,color:#000000
    classDef manifest fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef verify fill:#DE8F05,stroke:#000000,color:#000000
    classDef archive fill:#029E73,stroke:#000000,color:#FFFFFF
```

| Phase | What ships                       | Closing gate                                                       |
| ----- | -------------------------------- | ------------------------------------------------------------------ |
| 1     | `ai-engineer` manifest + landing | manifest live, 1 hub card, from-scratch persona framing confirmed  |
| 2     | _(growth only)_                  | full 9-course harness-cluster walk landed                          |
| 3     | —                                | all automated sweeps green                                         |
| 4     | —                                | 6 screenshots committed (1 landing + hub slice); zero open defects |
| 5     | —                                | CI green on `main`; production serving this path                   |
| 6     | —                                | every `learnings.md` entry terminal                                |
| 7     | —                                | archived                                                           |

## Depends-on

| Relation | Plan (full folder name) | Nature |
| -------- | ----------------------- | ------ |
| **blockedBy** | `ayokoding-learning-path-12-careers-se-manifests` | **Hard; sole direct execution prerequisite.** It must be fully merged and archived on `origin/main` before Phase 0. All earlier completion and repository-baseline facts are transitive context, not extra plan prerequisites. |

**Phase 0 start check:** `git ls-tree -r --name-only origin/main plans/done | rg -q "__ayokoding-learning-path-12-careers-se-manifests/README\.md$"` exits 0. This is this plan's only plan-level start gate.

## Recorded judgment calls

### JC-5: this plan does not perform its own four-manifest check

Even though this plan's own manifest is one of the four referenced by the "a shared course names every
path" scenario, this plan does **not** implement or run that check itself. **Choice**: the check lives
entirely in the sibling plan's own final phase. **Reason**: the check needs all four manifests to
exist, and the sibling plan is provably the one that finishes last (per DD-27's build order); placing
it in this plan would require this plan to somehow know when the sibling's other two manifests have
also shipped, which this plan has no dependency edge on at all. Placing the check in the plan that
already has the coupling edge back to this one is the only placement that adds no new edge.

## Delivery Mode: worktree-to-pr

This plan has exactly one dedicated worktree, one persistent final-delivery branch, and one PR.
All authoring, verification, and Knowledge Capture phases commit on that branch without a push, PR, merge, or deployment. In Phase 7, the executor commits the archival move and
any index updates, opens the sole draft PR, completes the secret scan, local quality checks, and PR quality-gate verification and CI gates,
marks it ready, and performs the normal AI merge/deploy after the hardened preconditions hold.
No per-course, cohort, stage, or phase worktree/branch/PR is permitted.

## Navigation

- [Business Requirements (brd.md)](./brd.md) — WHY the AI-engineer manifest is its own deliverable.
- [Product Requirements (prd.md)](./prd.md) — the persona, user stories, Gherkin acceptance criteria,
  and product scope.
- [Technical Docs (tech-docs.md)](./tech-docs.md) — the ownership invariant, the manifest format, the
  design decisions (DD-21 through DD-35, all reproduced here since they govern this plan's one
  manifest), and the growth-signal routing.
- [Delivery Checklist (delivery.md)](./delivery.md) — the phased executable checklist.
- [Learnings (learnings.md)](./learnings.md) — knowledge-capture running log.
- [Sibling plan — `ayokoding-learning-path-12-careers-se-manifests`](../ayokoding-learning-path-12-careers-se-manifests/README.md)
  — the three `software-engineer`-role manifests, coupled to this plan as described above.
- [Syllabus (cross-plan, read-only)](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md) —
  this plan's manifest mirror is
  [`manifest-immediately-effective-ai-engineer.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/paths/manifest-immediately-effective-ai-engineer.md).
