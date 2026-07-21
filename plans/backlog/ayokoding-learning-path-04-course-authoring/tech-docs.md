# Technical Docs — Learning Path Course Authoring

## Overview

This plan produces **content artefacts only**: 90 page bundles under
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`. It writes no TypeScript, no YAML data
file, no route, no component, and no redirect rule. Its "architecture" is therefore an **authoring
architecture**: where each body's authoritative spec lives, what shape the produced bundle takes, how
scope contracts are locked before their target bodies exist, and how a landed band is handed to the
plan that composes it.

## The manifest ownership invariant (binding)

> **This plan never edits a manifest file.** Every file under
> `apps/ayokoding-www/src/features/course-paths/manifests/` is owned by
> [`ayokoding-learning-path-05-manifests`](../ayokoding-learning-path-05-manifests/README.md). A
> step here that creates, appends to, reorders, or re-verifies a `.yaml` manifest is a **boundary
> violation**, not a convenience.

### Why the invariant exists (and why no wave ordering replaces it)

The two plans have a genuine mutual need:

- The manifest plan needs **this plan's bodies** — `checkManifestIntegrity` fails on any `courseOrder`
  ID with no resolving bundle under `<COURSES>`.
- This plan's bands would, in the source plan's shape, have **grown that plan's manifests** as they
  landed.

Neither ordering satisfies both directions. Put this plan last and its bands grow manifests that were
already published narrow, so the composed paths are permanently truncated in a way that looks correct
because integrity passes over the narrowed set. Put the manifest plan last — which is what the split
does — and this plan's growth steps would have to mutate `.yaml` files that do not exist yet, with
acceptance clauses referencing files no plan has created. **The cycle is not a scheduling problem; it
is an ownership problem, and only an ownership rule resolves it.**

```mermaid
%% Why the course-authoring/manifests dependency is resolved by ownership, not by ordering.
%% Node SHAPE encodes verdict: rectangle = the cycle, hexagon = a rejected fix, stadium = the adopted fix.
%% Edge LABELS state the concrete failure each rejected ordering produces.
flowchart LR
    CYCLE["Cycle:<br/>manifests need bodies<br/>bodies grow manifests"]:::cycle
    ORD1{{"Rejected fix A:<br/>author bodies last"}}:::rejected
    ORD2{{"Rejected fix B:<br/>compose manifests last,<br/>keep growth steps here"}}:::rejected
    OWN(["Adopted fix:<br/>ownership invariant<br/>+ band-completion signal"]):::adopted

    CYCLE --> ORD1
    CYCLE --> ORD2
    CYCLE --> OWN
    ORD1 -->|"manifests ship narrow and<br/>never grow — silently truncated paths"| FAIL1["FAILS"]:::fail
    ORD2 -->|"growth steps mutate .yaml files<br/>no plan has created yet"| FAIL2["FAILS"]:::fail
    OWN -->|"this plan only adds bodies;<br/>the other plan only composes IDs"| OK["SCHEDULABLE"]:::ok

    classDef cycle fill:#DE8F05,stroke:#000000,color:#000000
    classDef rejected fill:#CA9161,stroke:#000000,color:#000000
    classDef adopted fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef fail fill:#808080,stroke:#000000,color:#FFFFFF
    classDef ok fill:#029E73,stroke:#000000,color:#FFFFFF
```

**Accessibility note.** Verdict is carried by node **shape** (hexagon = rejected, stadium = adopted)
and by literal terminal labels (`FAILS` / `SCHEDULABLE`), never by fill colour alone. Fills use the
verified accessible palette per the
[Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md).

### What the invariant permits and forbids, concretely

| Action                                                              | Permitted here?                                                      |
| ------------------------------------------------------------------- | -------------------------------------------------------------------- |
| Create `<COURSES><course-id>/` and author its bundle                | **Yes**                                                              |
| Declare `prerequisites` in a course's own `_index.md`               | **Yes**                                                              |
| Add a course's row to the Course Library Catalog in this file       | **Yes**                                                              |
| List a course in `<COURSES>_index.md`                               | **Yes**                                                              |
| Record a band-completion signal in this plan's `delivery.md`        | **Yes**                                                              |
| Read a `.yaml` manifest to check what a path expects                | **Yes** (read-only)                                                  |
| Append a course ID to any `<MANIFESTS>**/*.yaml`                    | **No**                                                               |
| Re-order any `courseOrder`                                          | **No**                                                               |
| Re-run manifest integrity / prerequisite-consistency as a gate here | **No** — the manifest plan re-verifies its own artefacts             |
| Assert the 127-course catalog total                                 | **No** — that is the catalog total; this plan asserts its own **90** |

## Cross-plan `syllabus/` reference rule (binding)

The 128-file `syllabus/` detail layer lives **only** in
[`ayokoding-learning-path-02-schema-and-prerequisite-dag`](../ayokoding-learning-path-02-schema-and-prerequisite-dag/README.md).
This plan is its single largest consumer and **never copies it**.

- Every reference uses the **full cross-plan relative path**:
  `../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/<rest>`. The source plan's
  `./syllabus/...` form resolves to nothing after the split.
- **Copying is forbidden.** A copy forks the source of truth for 121 course specs and four manifest
  orderings, so a later spec correction lands in one copy only — and this plan's authoring passes read
  the stale one.
- The schema plan is Wave 1 and archives to `plans/done/YYYY-MM-DD__…` while this plan is still
  running. It carries a reciprocal repoint step in its own archival phase, executed in the same commit
  as its `git mv`. This plan carries a pre-archival gate check that catches a broken reference in its
  own files.

**Link-validation mechanics (verified against the binary — do not substitute a simpler form).**
`md links validate` accepts **no positional path**; passing one fails with
`error: unexpected argument '<path>' found`. It also cannot be scoped by `cd`-ing into a folder — it
always walks the repo. So "run it in this plan's folder" is **not expressible**. Separately, the bare
repo-wide invocation is **unsatisfiable**: the repo carries 93 pre-existing broken links, all under
`plans/done/`, unrelated to this work. Use the repo-wide form with the pre-push hook's own excludes
and filter to this plan's own paths:

```bash
cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- md links validate \
  --exclude plans/done \
  --exclude apps/ayokoding-www/content \
  --exclude apps/ose-www/content 2>&1 | grep -F "ayokoding-learning-path-04-course-authoring"
```

Acceptance: the `grep` finds **no** matching line (exits 1). Falsifiable the other way too —
introduce one bad `../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/` link and the
same command prints that file and exits 0.

## Authoring architecture

### The course page bundle

Every authored course is a page bundle at `<COURSES><course-id>/` with a fixed anatomy, mirroring the
sibling bundle shape already on disk:

```text
<COURSES><course-id>/
├── _index.md                 declares `prerequisites: [course-id, ...]` (contracted shape)
├── overview.md               purpose + `## Prerequisites` (earlier library courses only)
│                             + register + the explicit scope boundary against confusable siblings
├── learning/
│   ├── _index.md
│   ├── <concept + example pages, exhaustive `co-NN` / `ex-NN` coverage>
│   ├── code/                 colocated runnable examples (code-bearing courses only)
│   └── capstone/             the course's own intra-course capstone
└── drilling/
    ├── _index.md
    ├── overview.md
    └── <course-id>.md        the fixed five-section drilling order
```

The `course-id` slug, the prerequisite chain, the concept-coverage floor, and the worked-example
volume are all **settled** in the matching `syllabus/courses/<course-id>.md` spec. Authoring
transcribes them; it does not re-decide them.

### The per-course authoring convention (maker-checker-fixer, not code TDD)

```mermaid
%% The seven-step per-course authoring pipeline. Applied identically to every one of the 90 bodies.
%% Node SHAPE encodes stage kind: rectangle = produce, hexagon = verify, stadium = terminal.
%% The loop edge is labelled, so the retry path reads without colour.
%% TD required: the pipeline is an 8-step chain, so LR depth would exceed MaxWidth=4.
flowchart TD
    V{{"1 · V — accuracy pre-verify<br/>web-researcher"}}:::verify
    SK["2 · Skeleton<br/>bundle + prerequisites"]:::make
    LT["3 · Author learning track<br/>from co-NN / ex-NN spec"]:::make
    DT["4 · Author drilling track<br/>fixed five sections"]:::make
    CK{{"5 · Run content checkers<br/>learning + facts + link"}}:::verify
    FX["6 · Apply content fixers"]:::make
    RV{{"7 · Re-verify<br/>checkers + build + lint:md"}}:::verify
    DONE(["Course complete<br/>zero CRITICAL/HIGH/MEDIUM"]):::done

    V --> SK --> LT --> DT --> CK --> FX --> RV --> DONE
    RV -->|"any finding remains"| FX

    classDef make fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef verify fill:#DE8F05,stroke:#000000,color:#000000
    classDef done fill:#029E73,stroke:#000000,color:#FFFFFF
```

**Accessibility note.** Stage kind is carried by node **shape** (hexagon = verify, rectangle =
produce, stadium = terminal) and by the numbered step labels; the retry edge carries an explicit
label. Colour is redundant throughout.

**This is deliberately not a Red→Green→Refactor cycle.** Content authoring is a maker-checker-fixer
workflow: there is no failing test to write first, because the artefact under production is prose and
worked examples validated by domain checkers, not application behaviour validated by assertions. The
source plan states this explicitly and this plan preserves the ruling. See
[§TDD exemption](#tdd-exemption-this-plan-ships-no-application-code) below.

### The `prerequisites` frontmatter contract (consumed, not owned)

Every authored `_index.md` declares:

```yaml
prerequisites: [course-id, course-id, ...]
```

The canonical statement of this field's shape is owned by
[`ayokoding-learning-path-02-schema-and-prerequisite-dag`](../ayokoding-learning-path-02-schema-and-prerequisite-dag/tech-docs.md).
This plan **consumes** it. If this document and the schema plan's ever disagree, **the schema plan's
wins**. The list's contents are transcribed from the course's own spec file, never re-derived — an
invented edge adds a false edge to the library DAG whose failure surfaces far downstream in the
manifest plan with no trace back to the authoring pass that caused it.

### Course surgery — the four-path blast-radius rule

Courses are shared. Any edit, split, or merge to a course ripples to every manifest carrying that
course ID. DD-28 permits surgery and binds it to a blast-radius statement.

```mermaid
%% Decision branches for a proposed course change.
%% Node SHAPE encodes kind: diamond = decision, rectangle = action, stadium = terminal outcome.
%% TD required: the surgery branch is a 6-step chain, so LR depth would exceed MaxWidth=4.
flowchart TD
    START["Proposed change<br/>to library content"]:::action
    Q1{"Does a course<br/>already own it?"}:::decide
    Q2{"Is the change<br/>concept-level only?"}:::decide
    NEW(["Create a NEW course<br/>— but the net-new list is<br/>LOCKED at 6 (DD-32)"]):::locked
    CONCEPT(["Add as a co-NN inside<br/>the owning course (DD-31)"]):::ok
    SURGERY["Course surgery:<br/>update / merge / split"]:::action
    BLAST["State blast radius across<br/>ALL FOUR manifests<br/>BEFORE applying"]:::gate
    SIGNAL(["Record in delivery.md;<br/>the manifest plan re-verifies<br/>every affected manifest"]):::ok

    START --> Q1
    Q1 -->|"no"| NEW
    Q1 -->|"yes"| Q2
    Q2 -->|"yes"| CONCEPT
    Q2 -->|"no"| SURGERY
    SURGERY --> BLAST --> SIGNAL

    classDef action fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef decide fill:#DE8F05,stroke:#000000,color:#000000
    classDef gate fill:#CC78BC,stroke:#000000,color:#000000
    classDef ok fill:#029E73,stroke:#000000,color:#FFFFFF
    classDef locked fill:#808080,stroke:#000000,color:#FFFFFF
```

**Accessibility note.** Node kind is carried by **shape** (diamond = decision, rectangle = action,
stadium = terminal) and every edge carries an explicit `yes` / `no` label. The locked outcome states
its own constraint in its label rather than relying on its grey fill.

**A body fork is never an outcome of this tree.** DD-7's surviving half stands: per-path framing is a
lightweight intro/outro callout around the one shared body, never a copy. DD-28 supersedes only the
"create-only, never modify existing" half.

### Band-completion signal (the handoff to the manifest plan)

```mermaid
%% Order of operations across the two plans when a band lands.
sequenceDiagram
    autonumber
    participant CA as course-authoring (this plan, Wave 2)
    participant Main as origin/main
    participant MF as manifests (Wave 3)

    CA->>CA: Author every body in Band N from its syllabus spec
    CA->>CA: Run content checkers, apply fixers, re-verify
    CA->>Main: Push band branch, open draft PR, 3-cycle review, [AI] merge
    CA->>CA: Record five-field band-completion signal in delivery.md
    Note over CA,MF: Signal fields: BAND, PLAN, LANDED_COURSE_IDS,<br/>GROW_MANIFESTS (full paths), MERGED_COMMIT
    CA->>MF: Hand off the signal (via this plan's merged delivery.md)
    MF->>Main: Read LANDED_COURSE_IDS, confirm each resolves under COURSES
    MF->>MF: Append IDs to exactly the manifests named in GROW_MANIFESTS
    MF->>MF: Re-run checkManifestIntegrity + checkPrerequisiteConsistency
    Note over MF: If a signal is incomplete, the manifest plan REJECTS it<br/>rather than guessing which manifests to grow
```

The signal's five fields and the per-band `GROW_MANIFESTS` routing are specified in
[README §Band-completion signal contract](./README.md#band-completion-signal-contract). The routing
is not uniform — Band 9 grows two manifests, Bands 5 and 8 grow four, and Bands 1–4/6/7 grow three.

### Delivery flow across bands

```mermaid
%% Phase progression. Each band is its own phase with its own gate and its own safe stopping point.
%% Node SHAPE encodes kind: rectangle = authoring phase, hexagon = contract phase, stadium = finalization.
%% TD required: the plan is a 14-phase chain, so LR depth would far exceed MaxWidth=4.
flowchart TD
    P0["Phase 0<br/>Baseline +<br/>collision check"]:::setup
    P1["Phase 1<br/>Six net-new AI courses<br/>(authoring priority #1)"]:::author
    P2{{"Phase 2<br/>Course-surgery<br/>contracts locked"}}:::contract
    B1["P3 · Band 1<br/>Data depth"]:::author
    B2["P4 · Band 2<br/>Web + platform"]:::author
    B3["P5 · Band 3<br/>Mobile + desktop"]:::author
    B4["P6 · Band 4<br/>Concurrency langs"]:::author
    B5["P7 · Band 5<br/>Arch + AI/harness<br/>applies contracts"]:::author
    B6["P8 · Band 6<br/>Low-level + JVM"]:::author
    B7["P9 · Band 7<br/>Security + ops"]:::author
    B8["P10 · Band 8<br/>Capstones"]:::author
    B9["P11 · Band 9<br/>Interview technique"]:::author
    FIN(["Phases 12-16<br/>Verify · Manual · CI ·<br/>Knowledge · Archive"]):::final

    P0 --> P1 --> P2 --> B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> B7 --> B8 --> B9 --> FIN

    classDef setup fill:#CA9161,stroke:#000000,color:#000000
    classDef author fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef contract fill:#DE8F05,stroke:#000000,color:#000000
    classDef final fill:#029E73,stroke:#000000,color:#FFFFFF
```

**Accessibility note.** Phase kind is carried by node **shape** (hexagon = contract, stadium =
finalization, rectangle = authoring) and by explicit phase numbers in every label. Colour is
redundant.

**Band ordering rationale.** Band 5 must follow Phase 2 because it is the band whose bodies the three
course-surgery contracts target — the contracts are applied **by construction** at authoring time
rather than retrofitted across six bodies afterwards. Band 8's `capstone-build-your-own-coding-agent`
must follow Band 5 because it assembles the harness cluster Band 5 authors. Bands 1–4, 6, and 7 are
mutually content-independent and their relative order is a convenience, not a constraint; each body
writes only its own subtree, so they pipeline concurrently through review bounded by the in-force cap.

## Design Decisions

This plan owns **sixteen** design decisions and carries **two** cross-cutting ones verbatim.

> **Numbering note.** `DD-34`, `DD-35`, and `DD-39` are **not** this split's decisions — they are
> FS-SE-inherited tokens used throughout `syllabus/courses/**` with different meanings (concept
> enumeration, primary-source citation policy, typed-Python policy) and travel with `syllabus/` into
> the schema plan. `DD-36`, `DD-37`, and `DD-38` are unused. **Do not renumber to close the apparent
> gap.**

### Owned by this plan

- **DD-8 · Variant policy — separate course only when pedagogy must differ.** Default is one shared,
  path-neutral block. Author a distinct course-id variant (same topic, different teaching approach)
  only when a path genuinely needs a different pedagogy; paths pick the fitting variant. Variants are
  added **on demand** — no speculative variants are enumerated.
- **DD-10 · Interview technique is NEW content; fundamentals are shared courses.** The four interview
  modules teach technique; DS&A/OOP/system-design **depth** are library courses every path can use.
  Cleanly separates "technique" (refresh register, `interview-ready`-owned) from "subject depth"
  (shared).
- **DD-11 · AI-band scope-guard (baked in).** `creating-ai-powered-apps` = _use an LLM in an app_;
  `agentic-ai` = a _single survey_ of what an agent is that **forward-links each primitive to its
  harness-cluster course and stops short of build-your-own depth**; the harness cluster
  (`the-agent-loop`, `agent-tools-and-mcp`, `agent-context-and-memory`,
  `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`) builds each
  subsystem one-per-course. The cross-reference contract prevents 57 and the cluster from duplicating
  the loop/tools/MCP/memory/evals explanations — the band's largest duplication-creep risk.
- **DD-12 · `detection-engineering-and-siem-operations` kept distinct from `defensive-security`;
  mislabel fixed.** `defensive-security` (60) is **hands-on By-Example** (Sigma-on-ELK/OpenSearch + IR
  - hardening as generalist blue-team breadth) — the catalog's "concept" label was wrong and is
    corrected. `detection-engineering-and-siem-operations` owns the **Wazuh-specific deep tier**
    (decoders, correlation-rule authoring, FP tuning, dashboards) and declares `defensive-security` as
    its prerequisite. Explicit scope lines drawn in both bodies.
- **DD-13 · Harness-engineering cluster as a marquee build-your-own track.** The five harness courses +
  `capstone-build-your-own-coding-agent`, in **Python** (matching `remotebrowser`), sit after the AI
  band so prerequisites precede them. Available to all four paths; central to the three
  software-engineer paths' converging endpoint, and directly relevant to the fourth path's
  build-AI-systems scope (D1/DD-21) — the AI path's own manifest composition, including whether it
  walks or links to this cluster, is decided during that path's authoring (DD-27), and was resolved by
  DD-33 in favour of walking.
- **DD-14 · Two-altitude splits + gap-closers (retained, all keep-distinct).** Light
  `self-hosting-essentials` vs full-depth `bare-metal-virtualization`; `defensive-security` vs
  `detection-engineering-and-siem-operations` (DD-12); dedicated `just-enough-cpp` on-ramp (prereq
  `just-enough-c`); the `capstone-build-your-own-pentest-engine` security flagship. All are library
  courses; every path decides whether to include them.
- **DD-17 · FS-SE hard dependency removed.** The prior "the FS-SE plan must be DONE first" gate is gone
  — FS-SE is closed (`plans/done/2026-07-19__fundamentally-strong-software-engineer/`) and its Passes
  3–5 scope (topics 34–94 authoring) is **absorbed here** as the backfill.
- **DD-18 · Proof-of-transfer outcome-anchor (principles, not repo-specifics).** Courses teach durable
  **principles**; the target codebases are **evidence the principles transfer**, never subject matter.
  Path-independent — it justifies the **library**; all four paths inherit it (amended 2026-07-20 — was
  three). See
  [Productive in Target Codebases](#productive-in-target-codebases-proof-of-transfer-outcome-anchor).
- **DD-20 · Seven inter-topic capstones promoted to first-class catalog/manifest entries (2026-07-19
  reconciliation).** `capstone-solid-core`, `capstone-real-world-delivery`, `capstone-secure-service`,
  `capstone-data-pipeline`, `capstone-concurrency-and-systems`, `capstone-concurrency-showdown`, and
  `capstone-lead-at-altitude` are fully-specified inter-topic capstone specs embedded inside
  `engineering-management.md`, `defensive-security.md` (×3), `compilers-parsers-and-transpilers.md`
  (×2), and `site-reliability-engineering.md` respectively — each with a goal, an
  integrated-concepts checklist, ordered steps, acceptance criteria, and a done bar, indistinguishable
  in rigor from the six capstones the catalog already tracked. `capstone-solid-core` is **already live
  on disk** (`apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/capstone-solid-core/`,
  re-classified `Ecap`); the other six have no legacy home and are authored native (re-classified `N`).
  **Ruling: promote all seven** to the [Course Library Catalog](#course-library-catalog), all three
  path manifests (placed prerequisite-consistently), `syllabus/courses/README.md`'s capstone
  enumeration, and the delivery checklists. Corrected baseline: **114 → 121 courses, still 0 merges**.
  Never fold into a parent course's intra-course capstone or cut — each is a genuine, independently
  valuable building block with its own stable ID. **Decided 2026-07-19.**
  - _Split note_: this plan authors six of the seven natively (Band 8). `capstone-solid-core` is
    re-homed by `ayokoding-learning-path-01-url-restructure`; the manifest placements are performed
    by `ayokoding-learning-path-05-manifests`.
- **DD-25 · Evals split: an early light gate plus a later deep-evals course (D5).** Resolves a genuine
  ordering disagreement (Huyen-style "evals first" vs. bootcamp-style "evals after building") rather
  than silently picking a side. A **light eval gate** lands early — immediately after a learner's first
  working LLM call, before RAG and agents — answering only "how will you know this works?" A separate
  **deep evals course** lands after agents, covering error analysis, task-specific criteria,
  LLM-as-judge with measured human agreement, CI gating, and judge-scope reliability; it absorbs the
  three scattered evals treatments currently duplicated across `creating-ai-powered-apps` (co-19),
  `agentic-ai` (co-25/co-26), and `agent-orchestration-subagents-and-observability` (Theme D), which
  are trimmed to forward-links rather than gaining a fourth treatment. The scope boundary between the
  two courses is explicit, in the style of the library's existing AI-band scope-guard (DD-11).
- **DD-26 · Statistics-for-evals course authored, scoped tightly (D6).** No statistics or ML course
  exists anywhere in the (pre-amendment) 121-course library. Research verdict: "no ML background
  needed" is credible for training theory (backprop, architectures) but oversold for statistics — judge
  concordance and significance testing are irreducibly statistical. The new course is scoped to exactly
  what evals demand, not a general statistics course; `analytics-and-experimentation` (classical
  product A/B testing) remains a distinct, keep-separate course and may become a sibling or
  prerequisite rather than being merged.
- **DD-28 · Course surgery (update / merge / split / create) now permitted; six net-new AI courses
  bring the catalog to 127 (D8, amends the create-only half of DD-7).** Supersedes the "pure manifest
  reuse, zero new bodies beyond genuine gaps" invariant: course surgery against an **existing** course
  is now permitted, not only creation for a genuine gap. **Binding rule — course surgery is a
  four-path change.** Courses are shared; any edit, split, or merge to a course ripples to every
  manifest carrying that course ID. Each surgery **must state its blast radius** across all four
  manifests before it is applied, and every affected manifest must be **re-verified
  prerequisite-consistent** afterward (enforced as a gate). Concretely: the library's evals content,
  currently triple-taught with no single owner (`creating-ai-powered-apps` co-19, `agentic-ai`
  co-25/co-26, `agent-orchestration-subagents-and-observability` Theme D), is extracted into the new
  owned deep-evals course (DD-25) and the three donor courses are trimmed to forward-links — a surgery,
  not a fourth treatment. `agent-permissions-and-sandboxing` (guardrails) is explicitly **not** a
  surgery target — it already has a clear owner and is the library's strongest area. Six net-new
  courses are agreed for the fourth path (light eval gate, statistics for evals, deep evals, product
  patterns for probabilistic systems, inference serving and model deployment, fine-tuning and
  adaptation — DD-25/DD-26), bringing the catalog from the original 121 (114 authored + 7 DD-20
  capstones catalogued) to **127**.
  - **Amendment pair split across plans (binding — read both halves).** DD-28 is the **amendment**;
    the invariant it amends, **DD-7**, lands in
    [`ayokoding-learning-path-05-manifests`](../ayokoding-learning-path-05-manifests/tech-docs.md#design-decisions).
    **DD-28 supersedes the "create-only, never modify existing" half of DD-7.**
  - **DD-7's surviving half still binds here**, restated so a reader of this plan alone cannot read
    "surgery permitted" as "forking permitted": _a path omits a course that does not fit and creates a
    new shared course only for a genuine gap; per-path framing is a lightweight intro/outro callout
    around the shared body. Single source of truth per course._ **No body is ever forked per path.**
  - The manifest plan's copy of DD-7 carries the reciprocal link back to this DD-28. If either link
    breaks, a reader of one plan inherits a stale claim — `prd.md` names exactly this class of
    "per-role convergence confusion" as a live product risk mitigated only by the amendment record
    being cross-referenced from every site making the original claim.
- **DD-29 · Context and harness engineering: name and cite in existing courses, do not add or rename
  any course (D9).** Research verdict, verified against the actual course files: both disciplines are
  already taught, concept-for-concept, by the existing library — they are simply never named.
  `agent-context-and-memory` maps onto what the industry began calling **context engineering** in June
  2025 (Lütke 2025-06-19, Karpathy 2025-06-25, Willison 2025-06-27, and Anthropic's Effective Context
  Engineering methodology, 2025-09-29); the six-course harness cluster (`the-agent-loop`,
  `agent-tools-and-mcp`, `agent-context-and-memory`, `agent-permissions-and-sandboxing`,
  `agent-orchestration-subagents-and-observability`, `capstone-build-your-own-coding-agent`) satisfies
  all four necessary conditions in the only academic definition of an agent harness (arXiv 2606.10106),
  which the industry began calling **harness engineering** from late 2025 (Anthropic 2025-11-26;
  OpenAI; Böckeler/Thoughtworks 2026-04-02). A naming/lineage line citing this is added to
  `agent-context-and-memory` and to the harness cluster + `capstone-build-your-own-coding-agent`, so a
  learner connects the material to job-market vocabulary. The OpenAI/Anthropic-vs-HumanLayer
  containment dispute (whether harness is the umbrella containing context management, or the reverse)
  is cited as **unresolved**, not resolved or adopted as structure. **No course is renamed and no
  course is added** — "harness engineering" is roughly five months old and contested among named
  practitioners; building durable course structure on terminology this unsettled ages the curriculum
  badly.
  - **Citations** (matching the sourcing style used throughout `syllabus/courses/`):
    - [Web-cited] Tobi Lütke, X/Twitter, 2025-06-19 — "I really like the term 'context engineering'
      over prompt engineering… the art of providing all the context for the task to be plausibly
      solvable by the LLM." <https://x.com/tobi/status/1935533422589399127> (accessed 2026-07-21).
    - [Web-cited] Andrej Karpathy, X/Twitter, 2025-06-25 — "+1 for 'context engineering' over 'prompt
      engineering'…" <https://x.com/karpathy/status/1937902205765607626> (accessed 2026-07-21).
    - [Web-cited] Simon Willison, "Context engineering," 2025-06-27.
      <https://simonwillison.net/2025/jun/27/context-engineering/> (accessed 2026-07-21).
    - [Web-cited] Anthropic, "Effective context engineering for AI agents."
      <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents> (accessed
      2026-07-21; the specific 2025-09-29 publication date cited above was not independently
      re-verified against the live page).
    - [Web-cited] arXiv 2606.10106, "What makes a harness a harness: necessary and sufficient
      conditions for an agent harness" — confirmed real via WebSearch during the audit that produced
      this finding.
    - [Web-cited] Anthropic, "Effective harnesses for long-running agents," 2025-11-26.
      <https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents> (accessed
      2026-07-21).
    - [Web-cited] Birgitta Böckeler / Thoughtworks (via martinfowler.com), "Harness Engineering — first
      thoughts," 2026-04-02.
      <https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html> (accessed
      2026-07-21).
    - [Unverified] "OpenAI" — no specific OpenAI publication was identified to support this
      attribution; treat as unsourced until a specific OpenAI URL is supplied.
- **DD-30 · The capstone teaches the METR-vs-Scale-AI dispute as durable epistemic content (D10).**
  `capstone-build-your-own-coding-agent` teaches the contested evidence on whether harness quality even
  matters, as content that survives whatever happens to the vocabulary: **METR** (independent, no
  vendor stake, 2026-02-13) found Claude Code ahead of a generic ReAct scaffold in 50.7% of bootstrap
  samples on Opus 4.5 — a coin flip; **Scale AI / SWE-bench Pro** reports large scaffold-driven swings,
  with native scaffolds exploring roughly 1.5-2× more; the **competence-floor reconciliation** — METR
  compared against a competently built generic baseline while Scale compared against naive ones,
  implying harness quality matters enormously below a competence floor and then flattens — is
  explicitly labelled a **synthesis no single source makes**, not a finding either source reports. The
  unsourced 42%→78% scaffold-swing claim is a **do-not-cite**: it traces to no primary source.
  - **Citations**:
    - [Web-cited] METR, "Measuring Time Horizon using Claude Code and Codex," 2026-02-13.
      <https://metr.org/notes/2026-02-13-measuring-time-horizon-using-claude-code-and-codex/> (accessed
      2026-07-21) — confirms Claude Code beats a ReAct scaffold in 50.7% of bootstrap samples on
      Opus 4.5.
    - [Web-cited] Scale AI, "SWE-Bench Pro: Raising the Bar for Agentic Coding."
      <https://scale.com/blog/swe-bench-pro> (accessed 2026-07-21) — supports the native-scaffold
      exploration-multiplier claim; the precise 1.5-2× figure was not independently re-derived from the
      primary report — re-verify the exact multiplier before citing it in course content.
    - The 42%→78% scaffold-swing figure remains a **do-not-cite** per this DD's own text — no primary
      source was found for it.
- **DD-31 · Four concept-level additions land inside existing courses, never as new courses (D11).**
  Verified absent by direct file read at decision time, now confirmed present as `co-NN` entries in the
  corresponding course files (each already had mandated example/concept headroom): **cache-aware prefix
  ordering** → `agent-context-and-memory` co-23 (order context by staleness, not logical grouping —
  framed as the vendor-neutral stable-before-variable principle, not tied to Anthropic's explicit
  breakpoints or OpenAI's automatic threshold); **tool-count degradation** → `agent-tools-and-mcp`
  co-23 (tool-selection accuracy declines as available tool count rises, per the Berkeley
  Function-Calling Leaderboard and a GeoEngine benchmark finding a model failing at 46 tools and
  succeeding at 19 — governs when to split a tool surface across subagents); **tool-result token
  efficiency** → `agent-tools-and-mcp` co-24 (a tool's result shape is a context-budget decision;
  promotes the prior unquantified ex-27 aside to a named concept); **train-vs-production permission
  asymmetry** → `agent-permissions-and-sandboxing` co-23 (a training/exploration harness is permissive,
  a production harness restrictive — the distinction is about risk, not model capability, which is why
  it stays durable as models improve). None of the four introduces a new course.
- **DD-32 · Net-new course list locked at exactly 6; context and harness engineering add zero (D12,
  confirms DD-28).** Unchanged from the list DD-28 already catalogs (light eval gate, deep evals,
  statistics for evals, product patterns for probabilistic systems, inference serving and model
  deployment, fine-tuning and adaptation). DD-29 through DD-31 are naming, citation, and concept-level
  work **inside existing courses** — they add zero courses on top. This locks the arithmetic DD-28
  established: **127-course catalog** (121 + 6), not subject to further growth from the context/harness
  naming work.

### Cross-cutting (reproduced verbatim in all five split plans)

- **DD-15 · Build order (locked; amended 2026-07-20 by DD-27 — see below).** Group A (architecture +
  `course-paths` UI — hard prerequisite) → `interview-ready` MVP ships first (re-home 1–33, author the
  4 interview courses + `capstone-interview-loop`, one manifest, deploy) → `immediately-effective`
  manifest → `fundamentally-strong` manifest → backfill topics 34–94 native into `courses/` as the
  library fills. **DD-27 amends steps 2 onward**: the MVP is narrowed to an architecture smoke test
  only (interview-course authoring is no longer bundled into it), and the fourth path is inserted as
  authoring priority #1 immediately after the MVP.
- **DD-27 · Build order amended: the fourth path is authoring priority #1, behind an
  architecture-smoke-test-only MVP (D7, amends DD-15).** Locked order: **Group A** (architecture + UI,
  unchanged hard prerequisite) → **`interview-ready` MVP, narrowed to an architecture smoke test only**
  (ships against topics 1–33, already live on disk; proves routing, manifest loading, `?path` context,
  prev/next, breadcrumb, and prerequisite display against real content, in days not months —
  authoring the 4 NEW interview courses + `capstone-interview-loop` is **no longer bundled into this
  MVP gate**) → **`careers/immediately-effective/ai-engineer`** (authoring priority #1 for all authoring effort)
  → **`careers/immediately-effective/software-engineer`** manifest → **`careers/fundamentally-strong/software-engineer`**
  manifest → **backfill topics 34–94**. Rationale (preserved from the original build-order decision):
  nothing in the AI path exists on disk (~17 courses); making it literally first — ahead of even the
  MVP — would mean nothing ships until all 17 are authored, with the UI architecture unvalidated the
  entire time. Ordering it immediately after an architecture-smoke-test MVP gives the AI path first
  claim on every unit of real authoring effort while keeping the architecture proven early against
  content that already exists.

### Referenced but owned elsewhere

| DD    | Subject                                                          | Owner plan                                                |
| ----- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| DD-2  | One canonical body + URL per course; re-home with redirects      | `ayokoding-learning-path-01-url-restructure`              |
| DD-6  | Every course declares `prerequisites` → a prerequisite DAG       | `ayokoding-learning-path-02-schema-and-prerequisite-dag`  |
| DD-7  | Omit-or-create; per-path framing is a callout, never a body fork | `ayokoding-learning-path-05-manifests` (amended by DD-28) |
| DD-16 | Prerequisite-consistency is the audited smoothness property      | `ayokoding-learning-path-02-schema-and-prerequisite-dag`  |
| DD-21 | The AI path teaches building AI systems, not driving them        | `ayokoding-learning-path-05-manifests`                    |
| DD-22 | Convergence amended: paths converge per role, not globally       | `ayokoding-learning-path-05-manifests`                    |
| DD-24 | Fourth path's entry point: linked, not included, prerequisites   | `ayokoding-learning-path-05-manifests`                    |
| DD-33 | Fourth path's manifest WALKS the AI/harness cluster; spine is 15 | `ayokoding-learning-path-05-manifests`                    |

## Course Library Catalog

The library holds **127 courses** (amended 2026-07-20, DD-28 — was 121): **33 re-homed** (shipped
topics 1–33) + **61 transferred-native** (FS-SE topics 34–94) + **4 existing capstones** + **29 new**
(20 courses + 9 capstones). The **29 new** breaks down as the original **14 courses** + the **fourth
path's six net-new AI-engineering courses** + **9 capstones**. **Zero merges among the original 121**
— every overlap resolved keep-distinct per the reconciliation rulings recorded in
[`README.md`](./README.md) and the **DD-20** inter-topic-capstone reconciliation. Course surgery
against the original 121 is now permitted (DD-28) and, when applied, replaces "zero merges" with an
explicit blast-radius statement for that surgery.

> **This plan authors 90 of the 127.** The other 37 (33 shipped topics + 4 existing capstones,
> including `capstone-solid-core`) already exist on disk and are **re-homed** by
> `ayokoding-learning-path-01-url-restructure`. The 127 total is the manifest plan's terminal
> assertion; this plan asserts its own **90** — see [delivery.md](./delivery.md).

Each row lists **course-id · origin · format · primary language · prerequisites · one-line scope**.
**Origin**: `E` = existing shipped (1–33, re-homed elsewhere), `T(n)` = transferred FS-SE topic n
(authored here), `Ecap` = existing capstone (re-homed elsewhere), `N` = one of the 29 new (authored
here). **Order is NOT a catalog property** — it lives in the four path manifests owned by
`ayokoding-learning-path-05-manifests`. `prerequisites` are the course's own DAG edges (`—` = entry
point). Variants are added **on demand** and are not enumerated here.

Full per-course detail is the cross-plan
[`syllabus/courses/` catalog](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md).

### Editor & tooling foundations

| Course ID                 | Origin | Format     | Primary language | Prerequisites                         | One-line scope                       |
| ------------------------- | ------ | ---------- | ---------------- | ------------------------------------- | ------------------------------------ |
| `just-enough-nvim`        | E      | Primer     | Neovim           | —                                     | Modal editing, motions, buffers      |
| `just-enough-lua`         | E      | Primer     | Lua              | —                                     | Lua as Neovim's scripting language   |
| `extending-neovim`        | E      | By Example | Lua              | `just-enough-nvim`, `just-enough-lua` | Neovim config, plugins, LSP, keymaps |
| `just-enough-python`      | E      | Primer     | Python           | —                                     | Python syntax, types, idioms         |
| `just-enough-bash`        | E      | Primer     | Bash             | —                                     | Shell scripting, pipes, composition  |
| `version-control-and-git` | E      | By Example | Git              | —                                     | Branching, merging, history          |

### Coding, DS&A & interview technique

| Course ID                                   | Origin | Format            | Primary language  | Prerequisites                                                      | One-line scope                                                     |
| ------------------------------------------- | ------ | ----------------- | ----------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `data-structures-and-algorithms-essentials` | E      | By Example        | Python            | `just-enough-python`                                               | Core DS&A, complexity                                              |
| `advanced-algorithms`                       | E      | By Example        | Python            | `data-structures-and-algorithms-essentials`                        | Graphs, DP, advanced techniques                                    |
| `coding-interview`                          | N      | By Example        | Python (agnostic) | `data-structures-and-algorithms-essentials`, `advanced-algorithms` | LeetCode-pattern recognition + narration                           |
| `take-home-and-live-coding`                 | N      | By Example        | Python            | `data-structures-and-algorithms-essentials`                        | Take-home + live/pair technique                                    |
| `object-oriented-programming-essentials`    | E      | By Example        | Python            | `just-enough-python`                                               | Classes, inheritance, polymorphism                                 |
| `object-oriented-design-and-patterns`       | E      | By Example        | Python            | `object-oriented-programming-essentials`                           | SOLID, patterns, refactoring                                       |
| `sql-essentials`                            | E      | By Example        | SQL + Python      | `just-enough-python`                                               | Relational modeling, joins                                         |
| `system-design-interview`                   | N      | Annotated-concept | none              | `backend-essentials`, `networking-essentials`, `sql-essentials`    | Interview rubric + whiteboard flow (forward-links `system-design`) |
| `technical-communication`                   | E      | Annotated-concept | none              | —                                                                  | Docs, proposals, reviews                                           |
| `behavioral-and-leadership-interviews`      | N      | Annotated-concept | none              | —                                                                  | STAR, senior rounds, layoff/gap narrative                          |

### Web & platform productivity

| Course ID                           | Origin | Format            | Primary language    | Prerequisites                                             | One-line scope                                                                                |
| ----------------------------------- | ------ | ----------------- | ------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `just-enough-typescript`            | E      | Primer            | TypeScript          | —                                                         | Typed-JS types, tooling, idioms                                                               |
| `frontend-essentials`               | E      | By Example        | TypeScript          | `just-enough-typescript`                                  | Interactive UIs, components, state                                                            |
| `backend-essentials`                | E      | By Example        | Python (PostgreSQL) | `just-enough-python`, `sql-essentials`                    | HTTP backend + persistence (usable slice)                                                     |
| `async-python-and-fastapi-services` | N      | By Example        | Python              | `backend-essentials`, `concurrency-and-parallelism`       | FastAPI + Pydantic + uv/ruff/pyright (defers async concepts to 24, framework internals to 40) |
| `networking-essentials`             | E      | By Example        | Python              | `just-enough-python`                                      | TCP/IP, HTTP, DNS, sockets                                                                    |
| `api-design`                        | T(41)  | By Example        | Python              | `backend-essentials`                                      | REST/GraphQL/gRPC, OpenAPI, versioning                                                        |
| `advanced-frontend`                 | T(47)  | By Example        | TypeScript          | `frontend-essentials`                                     | State mgmt, performance, FE architecture                                                      |
| `self-hosting-essentials`           | N      | By Example        | ops/config          | `backend-essentials`, `networking-essentials`             | One box: containerize, reverse proxy + TLS, PaaS push                                         |
| `backend-at-scale`                  | T(39)  | By Example        | Python              | `backend-essentials`, `api-design`                        | Caching, sharding, queues, scaling                                                            |
| `containers-and-orchestration`      | T(50)  | By Example        | YAML/CLI            | `just-enough-bash`, `backend-essentials`                  | Docker + Kubernetes                                                                           |
| `cloud-and-iac`                     | T(51)  | Annotated-concept | HCL/YAML            | `containers-and-orchestration`                            | Terraform/OpenTofu IaC lifecycle                                                              |
| `cicd-and-release-engineering`      | T(55)  | By Example        | YAML + Python       | `version-control-and-git`, `containers-and-orchestration` | Pipelines, artifacts, release                                                                 |
| `build-automation-and-task-runners` | T(54)  | By Example        | multi-tool          | `just-enough-bash`, `version-control-and-git`             | Build systems, task runners, graphs                                                           |

### Mobile & desktop platforms

| Course ID                       | Origin | Format     | Primary language | Prerequisites                        | One-line scope                         |
| ------------------------------- | ------ | ---------- | ---------------- | ------------------------------------ | -------------------------------------- |
| `just-enough-kotlin`            | T(68)  | Primer     | Kotlin           | —                                    | Kotlin syntax, null-safety, coroutines |
| `android-app-development`       | T(69)  | By Example | Kotlin           | `just-enough-kotlin`                 | Native Android with the SDK            |
| `just-enough-swift`             | T(70)  | Primer     | Swift            | —                                    | Swift syntax, optionals                |
| `ios-app-development`           | T(71)  | By Example | Swift            | `just-enough-swift`                  | Native iOS with the SDK                |
| `just-enough-dart`              | T(72)  | Primer     | Dart             | —                                    | Dart syntax, async, Flutter idioms     |
| `hybrid-app-development`        | T(73)  | By Example | Dart             | `just-enough-dart`                   | Cross-platform from one Dart codebase  |
| `just-enough-csharp`            | T(74)  | Primer     | C#               | —                                    | C# syntax, LINQ, async, .NET           |
| `windows-app-development`       | T(75)  | By Example | C#               | `just-enough-csharp`                 | Native Windows desktop                 |
| `linux-app-development`         | T(76)  | By Example | Python           | `just-enough-python`                 | Native Linux desktop, packaging        |
| `building-production-cli-tools` | T(77)  | By Example | Go + Rust        | `just-enough-go`, `just-enough-rust` | Distributable CLI tools                |

### CS foundations, paradigms & concurrency

| Course ID                      | Origin | Format            | Primary language | Prerequisites                                       | One-line scope                                  |
| ------------------------------ | ------ | ----------------- | ---------------- | --------------------------------------------------- | ----------------------------------------------- |
| `computer-science-foundations` | E      | Annotated-concept | Python           | `just-enough-python`                                | Automata, computability, complexity             |
| `computer-architecture`        | E      | By Example        | C                | `just-enough-c`                                     | CPU, memory, caches, instruction execution      |
| `programming-paradigms`        | E      | By Example        | Python           | `just-enough-python`                                | Imperative/functional/logic survey              |
| `functional-programming`       | E      | By Example        | Python           | `just-enough-python`                                | Pure fns, immutability, HOFs                    |
| `concurrency-and-parallelism`  | E      | By Example        | Python           | `just-enough-python`                                | Threads, async, locks (owns async fundamentals) |
| `just-enough-go`               | T(64)  | Primer            | Go               | —                                                   | Go syntax, goroutines                           |
| `csp-style-concurrency`        | T(65)  | By Example        | Go               | `just-enough-go`, `concurrency-and-parallelism`     | Channels, CSP concurrency                       |
| `just-enough-elixir`           | T(66)  | Primer            | Elixir           | —                                                   | Elixir syntax, pattern matching                 |
| `actor-model-concurrency`      | T(67)  | By Example        | Elixir           | `just-enough-elixir`, `concurrency-and-parallelism` | Actors, supervision trees                       |

### Data depth

| Course ID                                | Origin | Format            | Primary language | Prerequisites                                                 | One-line scope                       |
| ---------------------------------------- | ------ | ----------------- | ---------------- | ------------------------------------------------------------- | ------------------------------------ |
| `advanced-networking`                    | E(29)  | Annotated-concept | Python           | `networking-essentials`                                       | Load balancing, proxies, TLS         |
| `advanced-sql-and-query-performance`     | E(26)  | By Example        | SQL + Python     | `sql-essentials`                                              | Query plans, indexing, tuning        |
| `data-access-orms-and-query-builders`    | E(27)  | By Example        | Python           | `sql-essentials`, `object-oriented-programming-essentials`    | Using ORMs/query builders safely     |
| `build-your-own-orm-and-query-builder`   | E(28)  | By Example        | Python           | `data-access-orms-and-query-builders`                         | Implementing a small ORM             |
| `nosql-databases`                        | T(34)  | By Example        | Python           | `sql-essentials`                                              | Document, KV, column stores          |
| `graph-databases`                        | T(35)  | By Example        | Cypher + Python  | `sql-essentials`                                              | Modeling/querying connected data     |
| `database-internals-and-storage-engines` | T(36)  | By Example        | Python           | `sql-essentials`, `data-structures-and-algorithms-essentials` | B-trees, LSM-trees, WAL              |
| `data-engineering`                       | T(37)  | Annotated-concept | Python           | `sql-essentials`, `backend-essentials`                        | Pipelines, batch/stream, warehousing |
| `search-and-information-retrieval`       | T(38)  | By Example        | Python           | `data-structures-and-algorithms-essentials`                   | Inverted indexes, ranking            |

### Architecture, distributed & AI / harness

| Course ID                                         | Origin | Format            | Primary language | Prerequisites                                                  | One-line scope                                                                                                 |
| ------------------------------------------------- | ------ | ----------------- | ---------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `software-architecture`                           | T(42)  | Annotated-concept | Python           | `backend-essentials`, `object-oriented-design-and-patterns`    | Styles, tradeoffs, structuring                                                                                 |
| `domain-driven-design`                            | T(43)  | By Example        | Python           | `object-oriented-design-and-patterns`, `software-architecture` | Bounded contexts, modeling                                                                                     |
| `system-design`                                   | T(44)  | Annotated-concept | Python           | `backend-at-scale`, `networking-essentials`                    | Designing for scale/availability (depth sibling of `system-design-interview`)                                  |
| `event-driven-architecture`                       | T(45)  | By Example        | Python           | `software-architecture`, `backend-essentials`                  | Events, brokers, EDA                                                                                           |
| `distributed-systems`                             | T(46)  | By Example        | Python           | `networking-essentials`, `concurrency-and-parallelism`         | Consensus, replication, CAP                                                                                    |
| `build-your-own-web-framework`                    | T(40)  | By Example        | Python           | `backend-essentials`, `networking-essentials`                  | WSGI/ASGI, router, middleware (demystifies FastAPI)                                                            |
| `build-your-own-reactive-ui`                      | T(48)  | By Example        | TypeScript       | `advanced-frontend`                                            | Reactive UI lib + virtual DOM                                                                                  |
| `software-engineering-practices`                  | E(30)  | Annotated-concept | Python           | `version-control-and-git`, `software-testing`                  | Code review, CI, quality gates                                                                                 |
| `agentic-coding`                                  | E(31)  | Annotated-concept | polyglot         | `version-control-and-git`                                      | Driving AI agents (user/driver side — distinct axis)                                                           |
| `creating-ai-powered-apps`                        | T(56)  | By Example        | Python           | `backend-essentials`, `api-design`                             | **Use an LLM in an app**: RAG, tool-calling, MCP, evals (scope-guard head, DD-11)                              |
| `agentic-ai`                                      | T(57)  | By Example        | Python           | `creating-ai-powered-apps`                                     | **Survey** of agents; forward-links each primitive to the harness cluster (does NOT re-teach at depth — DD-11) |
| `browser-automation-with-cdp`                     | N      | By Example        | Python (CDP)     | `just-enough-python`, `networking-essentials`                  | Chrome DevTools Protocol automation (remotebrowser skill)                                                      |
| `the-agent-loop`                                  | N      | By Example        | Python           | `agentic-ai`                                                   | LLM read-eval-act loop, streaming, stops (build-your-own tier)                                                 |
| `agent-tools-and-mcp`                             | N      | By Example        | Python           | `the-agent-loop`                                               | Tool/function schemas; MCP server + client                                                                     |
| `agent-context-and-memory`                        | N      | Annotated-concept | Python           | `the-agent-loop`                                               | Context budgeting, compaction, memory                                                                          |
| `agent-permissions-and-sandboxing`                | N      | By Example        | Python           | `the-agent-loop`                                               | Approval models, sandboxing, guardrails                                                                        |
| `agent-orchestration-subagents-and-observability` | N      | Annotated-concept | Python           | `agent-tools-and-mcp`, `agent-context-and-memory`              | Subagents, hooks/skills, evals, tracing                                                                        |

### AI-engineering specialization (the fourth path's six net-new courses)

Authored in Phase 1 from their settled cross-plan spec files (295–425 lines each).

| Course ID                                    | Origin | Format                     | Primary language | Prerequisites                                             | One-line scope                                                             |
| -------------------------------------------- | ------ | -------------------------- | ---------------- | --------------------------------------------------------- | -------------------------------------------------------------------------- |
| `evaluating-ai-output-essentials`            | N      | Annotated-concept          | Python           | per its settled spec                                      | Light eval gate: "how will you know this works?" before RAG/agents (DD-25) |
| `statistics-for-evaluation`                  | N      | Annotated-concept (code)   | Python           | per its settled spec                                      | Judge concordance + significance testing for evals only (DD-26)            |
| `evaluating-ai-systems-in-depth`             | N      | By Example                 | Python           | `statistics-for-evaluation` (hard), plus its settled spec | Deep evals: error analysis, LLM-as-judge, CI gating (DD-25)                |
| `product-patterns-for-probabilistic-systems` | N      | Annotated-concept, no code | none             | per its settled spec                                      | Product patterns for probabilistic, not deterministic, outputs (DD-28)     |
| `inference-serving-and-model-deployment`     | N      | By Example                 | Python           | per its settled spec                                      | vLLM/TGI, KV-cache, batching, GPU considerations (DD-28)                   |
| `fine-tuning-and-adaptation`                 | N      | By Example                 | Python           | per its settled spec                                      | Fine-tuning / LoRA / PEFT versus RAG as a foil (DD-28)                     |

Each row's `prerequisites` cell reads "per its settled spec" deliberately: the exact chain is declared
in that course's `syllabus/courses/<id>.md` file and is transcribed at authoring time, not restated
here where it could drift. The Phase 1 catalog-rows step replaces each cell with the transcribed
chain.

### Low-level systems, JVM & languages, internals builds

| Course ID                           | Origin | Format     | Primary language     | Prerequisites                                                     | One-line scope                                             |
| ----------------------------------- | ------ | ---------- | -------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------- |
| `just-enough-c`                     | T(78)  | Primer     | C                    | —                                                                 | Minimal C for the OS/systems topics                        |
| `just-enough-cpp`                   | N      | Primer     | C++                  | `just-enough-c`                                                   | RAII, templates, STL, smart pointers (no FS-SE C++ course) |
| `linux-os`                          | T(79)  | By Example | C + shell            | `just-enough-c`, `just-enough-bash`                               | Processes, syscalls, filesystems                           |
| `windows-os`                        | T(80)  | By Example | C + PowerShell       | `just-enough-c`                                                   | Windows internals, the API                                 |
| `system-programming`                | T(81)  | By Example | C                    | `just-enough-c`, `linux-os`                                       | Close-to-metal C: memory model, manual RM                  |
| `just-enough-rust`                  | T(82)  | Primer     | Rust                 | —                                                                 | Ownership, borrowing, type system                          |
| `modern-system-programming`         | T(83)  | By Example | Rust                 | `just-enough-rust`                                                | Safe systems programming (Rust counterpart of 81)          |
| `just-enough-java`                  | T(84)  | Primer     | Java                 | —                                                                 | Java syntax, JVM, collections                              |
| `enterprise-java-and-the-jvm`       | T(85)  | By Example | Java                 | `just-enough-java`                                                | Spring, JVM ecosystem                                      |
| `lisp`                              | T(86)  | By Example | Scheme + Clojure     | —                                                                 | Macros, homoiconicity                                      |
| `just-enough-fsharp`                | T(87)  | Primer     | F#                   | —                                                                 | DUs, functional-first                                      |
| `type-systems`                      | T(88)  | By Example | OCaml + Haskell + F# | `just-enough-fsharp`, `functional-programming`                    | Algebraic types, inference                                 |
| `compilers-parsers-and-transpilers` | T(89)  | By Example | F#                   | `just-enough-fsharp`, `data-structures-and-algorithms-essentials` | Lexers, parsers, ASTs                                      |
| `build-your-own-git`                | T(90)  | By Example | Python               | `just-enough-python`, `version-control-and-git`                   | Git object model + plumbing                                |
| `build-your-own-database`           | T(91)  | By Example | Python               | `just-enough-python`, `database-internals-and-storage-engines`    | Storage, indexing, transactions                            |
| `build-your-own-raft`               | T(92)  | By Example | Go                   | `just-enough-go`, `distributed-systems`                           | Raft consensus + replicated KV                             |

### Security, ops, quality & delivery

| Course ID                                   | Origin | Format            | Primary language            | Prerequisites                                                  | One-line scope                                                                                                             |
| ------------------------------------------- | ------ | ----------------- | --------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `security-essentials`                       | E(17)  | By Example        | Python                      | `backend-essentials`                                           | Common vulns, auth, secrets                                                                                                |
| `it-and-application-security`               | T(58)  | Annotated-concept | Python                      | `security-essentials`                                          | CIA, STRIDE, OWASP, crypto, identity                                                                                       |
| `offensive-security`                        | T(59)  | By Example        | Python + shell              | `security-essentials`, `networking-essentials`                 | Recon, scanning, exploitation (lab-local)                                                                                  |
| `defensive-security`                        | T(60)  | **By Example**    | Python + shell              | `security-essentials`, `networking-essentials`                 | **Hands-on** generalist blue-team: Sigma-on-ELK/OpenSearch + IR lifecycle + hardening (label fixed — NOT "concept", DD-12) |
| `detection-engineering-and-siem-operations` | N      | By Example        | XML/rules + config + Python | `defensive-security`                                           | **Wazuh-specific deep tier**: decoders, correlation rules, FP tuning, dashboards (specialist — DD-12)                      |
| `vulnerability-management-and-assessment`   | T(61)  | By Example        | Python                      | `security-essentials`                                          | Scanning, triage, remediation at scale, SBOM                                                                               |
| `it-governance-grc`                         | T(62)  | Annotated-concept | none                        | `it-and-application-security`                                  | Governance, risk, compliance, audit                                                                                        |
| `bare-metal-virtualization`                 | T(52)  | By Example        | HCL/YAML/shell              | `containers-and-orchestration`                                 | Proxmox, hypervisors (full-depth sibling of `self-hosting-essentials`)                                                     |
| `self-managed-kubernetes-and-gitops`        | T(53)  | By Example        | YAML/CLI                    | `containers-and-orchestration`, `cicd-and-release-engineering` | Self-owned prod K8s + GitOps                                                                                               |
| `platform-engineering-and-devex`            | T(93)  | Annotated-concept | none                        | `containers-and-orchestration`, `cicd-and-release-engineering` | Internal platforms, golden paths                                                                                           |
| `site-reliability-engineering`              | T(94)  | Annotated-concept | Python                      | `containers-and-orchestration`, `system-design`                | SLOs, observability, IR                                                                                                    |
| `software-testing`                          | E(15)  | By Example        | Python + TS                 | `just-enough-python`, `just-enough-typescript`                 | Unit, integration, E2E (Playwright)                                                                                        |
| `debugging-and-profiling`                   | E(16)  | By Example        | Python + native             | `just-enough-python`                                           | Systematic debugging + profiling                                                                                           |
| `analytics-and-experimentation`             | T(63)  | By Example        | Python                      | `sql-essentials`                                               | Metrics, A/B testing                                                                                                       |
| `information-architecture-and-seo`          | T(49)  | Annotated-concept | HTML                        | `frontend-essentials`                                          | Structuring content, SEO                                                                                                   |
| `software-product-engineering`              | E(32)  | Annotated-concept | none                        | —                                                              | Turning engineering into products                                                                                          |
| `engineering-management`                    | E(33)  | Annotated-concept | none                        | —                                                              | Leading engineers/teams                                                                                                    |
| `project-management`                        | E(9)   | Annotated-concept | none                        | —                                                              | Scoping, planning, tracking                                                                                                |

### Capstones (courses too — each a building block)

| Course ID                                | Origin | Kind                    | Primary language  | Prerequisites                                                                                                                                                                                             | One-line scope                                                                                                                                                                                                                                |
| ---------------------------------------- | ------ | ----------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `capstone-forge-ready`                   | Ecap   | Prologue milestone      | multi             | `extending-neovim`, `just-enough-python`, `just-enough-bash`, `version-control-and-git`                                                                                                                   | Reproducible dev forge (nvim + lua + extend)                                                                                                                                                                                                  |
| `capstone-interview-loop`                | N      | Interview milestone     | Python + prose    | `coding-interview`, `take-home-and-live-coding`, `system-design-interview`, `behavioral-and-leadership-interviews`                                                                                        | Full mock loop: coding + system-design + behavioral                                                                                                                                                                                           |
| `capstone-first-working-software`        | Ecap   | Web milestone           | Python + TS       | `frontend-essentials`, `backend-essentials`, `security-essentials`, `software-testing`                                                                                                                    | First secure, tested web app                                                                                                                                                                                                                  |
| `capstone-full-stack-app`                | Ecap   | Full-stack milestone    | TS + Python       | `frontend-essentials`, `backend-essentials`, `sql-essentials`, `api-design`                                                                                                                               | Typed FE ↔ BE ↔ SQL vertical slice                                                                                                                                                                                                            |
| `capstone-build-your-own-coding-agent`   | N      | Harness milestone       | Python            | `agent-tools-and-mcp`, `agent-context-and-memory`, `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`                                                                  | Assemble the harness cluster into a coding-agent CLI                                                                                                                                                                                          |
| `capstone-build-your-own-pentest-engine` | N      | Security milestone      | TypeScript        | `offensive-security`, `detection-engineering-and-siem-operations`, `agent-orchestration-subagents-and-observability`, `browser-automation-with-cdp`                                                       | Agentic pentest engine (swarm + MCP + CDP + security chaining) — **lab-local, authorized-scope-only** (inherits `offensive-security`'s rules-of-engagement guard; body must restate scope/authorization limits per OWASP 2026 Agentic Top-10) |
| `capstone-solid-core`                    | Ecap   | Pass-boundary milestone | Python + TS       | `capstone-first-working-software`, `object-oriented-design-and-patterns`, `functional-programming`, `concurrency-and-parallelism`, `advanced-sql-and-query-performance`, `software-engineering-practices` | Re-engineer the Pass-1 app to a SOLID/functional-core professional baseline with a CI gate + ADRs (DD-20; embedded spec in `engineering-management.md`)                                                                                       |
| `capstone-real-world-delivery`           | N      | Full-stack milestone    | Python + TS + IaC | `capstone-solid-core`, `system-design`, `event-driven-architecture`, `containers-and-orchestration`, `cloud-and-iac`, `cicd-and-release-engineering`, `defensive-security`                                | Deploy-as-code, secured, observable delivery of the Pass-2 app — DDD + capacity plan + red/blue-team loop (DD-20; embedded spec in `defensive-security.md`)                                                                                   |
| `capstone-secure-service`                | N      | Security milestone      | Python + shell    | `security-essentials`, `backend-essentials`, `it-and-application-security`, `offensive-security`, `defensive-security`                                                                                    | End-to-end secured HTTP service: OWASP-2025 + OAuth2/OIDC, red-team validated + blue-team detected (DD-20; embedded spec in `defensive-security.md`)                                                                                          |
| `capstone-data-pipeline`                 | N      | Data milestone          | SQL + Python      | `sql-essentials`, `advanced-sql-and-query-performance`, `data-engineering`, `creating-ai-powered-apps`, `backend-essentials`                                                                              | Medallion pipeline (bronze/silver/gold) → governed warehouse → RAG-grounded query interface (DD-20; embedded spec in `defensive-security.md`)                                                                                                 |
| `capstone-concurrency-and-systems`       | N      | Systems milestone       | Go or Elixir + C  | `csp-style-concurrency`, `actor-model-concurrency`, `containers-and-orchestration`, `site-reliability-engineering`                                                                                        | Concurrent, containerized, SRE-instrumented (golden signals + SLO) service (DD-20; embedded spec in `compilers-parsers-and-transpilers.md`)                                                                                                   |
| `capstone-concurrency-showdown`          | N      | Comparison milestone    | Go + Elixir       | `csp-style-concurrency`, `actor-model-concurrency`                                                                                                                                                        | The same problem solved CSP-Go vs actor-Elixir, compared head-to-head (DD-20; embedded spec in `compilers-parsers-and-transpilers.md`)                                                                                                        |
| `capstone-lead-at-altitude`              | N      | Whole-journey milestone | polyglot + prose  | `capstone-concurrency-and-systems`, `capstone-real-world-delivery`, `site-reliability-engineering`, `software-product-engineering`, `engineering-management`                                              | Whole-journey leadership synthesis: SLOs, strategy, prioritization, a six-pass retrospective (DD-20; embedded spec in `site-reliability-engineering.md`)                                                                                      |

**Count check**: 33 re-homed (E) + 61 transferred-native (T) + 4 existing capstones (Ecap) + 23 new
(N: 14 courses + 9 capstones) = **121** among the original software-engineer-role baseline, zero
merges (DD-28 permits course surgery against this 121 going forward, replacing "zero merges" with an
explicit per-surgery blast-radius statement). Plus the fourth path's **6 net-new AI-engineering
courses** = **127** total catalog.

**This plan's own share**: 61 (T) + 23 (N) + 6 (AI) = **90 authored bodies**. The remaining 37
(33 E + 4 Ecap) are re-homed by `ayokoding-learning-path-01-url-restructure`. 90 + 37 = 127.

## Productive in Target Codebases (proof-of-transfer outcome-anchor)

**Philosophy.** The library teaches durable **PRINCIPLES**; the target codebases are **evidence the
principles transfer**, never subject matter. No course is "about" a target repo. This anchor is
path-independent — it justifies the **library**, and all four paths inherit it (DD-18, amended
2026-07-20 — was three).

The target codebases and the principle-modules that build each stack skill (the gap-filling NEW courses
— `async-python-and-fastapi-services`, `browser-automation-with-cdp`, the harness cluster,
`just-enough-cpp`, `detection-engineering-and-siem-operations`, `capstone-build-your-own-pentest-engine`
— are library courses every path can include):

- **`ose-public` / `ose-primer` / `ose-infra`** (this workspace family) [Repo-grounded — `AGENTS.md`]
  — Nx monorepo, F#/Giraffe backends, Rust CLIs, Playwright E2E, multi-harness AI-agent binding.
- **`remotebrowser`** [Web-cited — <https://github.com/remotebrowser/remotebrowser>, accessed
  2026-07-18] — async-Python/FastAPI browser-fleet orchestration over CDP + MCP; built by
  `async-python-and-fastapi-services`, `browser-automation-with-cdp`, and the harness cluster.
- **`wazuh/wazuh`** [Web-cited — <https://github.com/wazuh/wazuh>, accessed 2026-07-18] — C/C++
  manager/agent core (C++-dominant, actively developed in C++17–C++20; C is legacy) + XML detection
  ruleset; built by `just-enough-cpp` and `detection-engineering-and-siem-operations`.
- **`anggipradana/vacti` + `anggipradana/vacti-pentest-engine`** [Unverified — maintainer-supplied;
  not publicly discoverable on 2026-07-18 search; treat all specifics as subject to change] — a
  TypeScript/Nx product and its agentic pentest engine; built by the web/monorepo courses + the
  security suite + `capstone-build-your-own-pentest-engine`.

**Citation notes**: `remotebrowser` (Python; `uv` + Podman; CDP-driven isolated Chrome; bundled MCP
server; REST control API) and `wazuh` (open-source XDR+SIEM, OSSEC lineage; manager/agent + indexer +
dashboard; 3000+ XML decoders/rules) facts are drawn from their public GitHub + docs surfaces on the
access date; both are version-sensitive, so the driven NEW courses must re-verify current specifics via
`apps-ayokoding-www-facts-checker` at authoring time. The two `vacti` repos were **not publicly
discoverable** on 2026-07-18 — all their specifics are maintainer-supplied and must never be written as
version-pinned facts; the gap-closer courses are grounded primarily in the publicly verified `wazuh`
target.

## UI-gate and API-gate posture (R9)

Both postures are declared explicitly. Per the
[api-quality-gate workflow](../../../repo-governance/workflows/api/api-quality-gate.md)'s
§Relationship to Other Gates, a plan bearing neither surface **is not thereby exempt** — exemption
belongs only to a plan with no reachable behavioural delta at all, and it must be stated here.

### UI gate — **exempt**, and here is the reasoning rather than the assertion

`swe-ui-checker` validates component **source** — it globs for `.tsx` files. This plan's own
[Overview](#overview) already states the fact plainly: it "writes no TypeScript, no YAML data file,
no route, no component, and no redirect rule." Its entire output is 90 markdown page bundles under
`apps/ayokoding-www/content/en/learn/courses/<course-id>/`. A checker run scoped to this plan's diff
would scan **zero** `.tsx` files and return zero findings — a vacuous pass, recorded as an exemption
rather than a claimed one. The components that render these bodies — `PathRail`, `PathLanding`,
`PathCard`, the paths hub — are owned and gated by `ayokoding-learning-path-03-navigation-ui`.

**The exemption is narrow.** It covers `ui-quality-gate` **only**. Because this plan ships 90
user-visible pages, manual behavioural verification via Playwright MCP is **mandatory and
performed** — [Phase 13](./delivery.md#phase-13-manual-content-verification-playwright-mcp) opens a
sample of authored course pages at all three breakpoints in the `en` content locale, with committed
screenshot evidence. The **Rule-15 three-tester retest is separately and already exempted**, with its
own stated reasons, in
[README §Rule-15 three-tester retest — exemption recorded](./README.md#rule-15-three-tester-retest--exemption-recorded):
the triad would exercise the navigation plan's rendering layer, not this plan's content, and this
plan's content correctness is instead covered by dedicated content-domain checkers
(`apps-ayokoding-www-{by-example,annotated-concept,primer,general}-checker`,
`apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`) — strictly stronger, for prose
correctness, than a generalist live-site UX triad. This posture declaration reproduces that existing
exemption rather than re-deciding it; the two records must not diverge. **The distinction that
matters**: the Rule-15 triad's exemption is a separate, narrower ruling than `ui-quality-gate`'s —
both happen to resolve the same way for this plan, but for different reasons, and neither entails the
other.

### API gate — **exempt**

Unlike its sibling manifest-owning plans, this plan **never edits a manifest file** — forbidden
outright by [§The manifest ownership invariant](#the-manifest-ownership-invariant-binding) — and
ships no code, no YAML, no route. Its one piece of structured data, the `prerequisites` frontmatter
this plan writes into each of the 90 `_index.md` files, is **inert until a downstream consumer reads
it**: `checkManifestIntegrity` / `checkPrerequisiteConsistency` run against it only once
`ayokoding-learning-path-05-manifests` grows a manifest to include these courses. This plan's own
structural check — `test -d` / `test -f` + frontmatter grep (see
[Testing / Verification Strategy](#testing--verification-strategy)) — verifies only that the field is
present and well-formed, never that it resolves; that re-verification belongs entirely to the
manifest plan, which is correspondingly **not** exempt (see its own R9 posture).

The colocated `code/` samples inside each course body are course material, not application code — "no
importable module, no test target, and no runtime behaviour the app depends on" (already recorded in
[the TDD exemption](#tdd-exemption-this-plan-ships-no-application-code) above). Between the inert
frontmatter and the non-runtime content, this plan has **no reachable behavioural delta of its own**
for `api-quality-gate` to exercise.

**Rule-16 API exploratory retest — not applicable.** No REST or GraphQL endpoint changes;
`api-exploratory-tester` has nothing to exercise.

## Exemptions (stated explicitly, not silently taken)

### UI-design-funnel exemption (not UI-bearing)

A plan is UI-bearing when it **adds or changes user-facing screens or components** under `apps/` or
`libs/`. This plan does neither. Every artefact it produces is a markdown page bundle under
`apps/ayokoding-www/content/`, rendered by components this plan does not touch. The complete
UI-design-funnel for Screens 0–3 (low-fi alternatives, hi-fi `.excalidraw.png` finalists, named
selections, rationale records, responsive strategies) is owned by
[`ayokoding-learning-path-03-navigation-ui`](../ayokoding-learning-path-03-navigation-ui/prd.md);
Screen 4's funnel is owned by
[`ayokoding-learning-path-01-url-restructure`](../ayokoding-learning-path-01-url-restructure/prd.md).
**This plan carries no `assets/` folder and produces no render.**

### Specs & Gherkin (app-code) exemption

The [Feature Change Completeness Convention](../../../repo-governance/development/quality/feature-change-completeness.md)
binds app/lib code changes to companion `specs/` Gherkin. This plan changes **no app or lib code** —
it adds content under `apps/ayokoding-www/content/`, which the source plan explicitly classifies as
"largely content (exempt from `specs:coverage`)". The `course-paths` feature's Gherkin companion is
owned by the schema and navigation-UI plans.

The eleven Gherkin scenarios in [`prd.md`](./prd.md#acceptance-criteria-gherkin) are therefore
**content-level acceptance criteria**, bound to delivery steps and verified by grep-checkable
assertions plus the ayokoding content checkers — not by `specs:behavior:coverage`. The plan still
runs `npx nx affected -t specs:behavior:coverage` in its verification phase to prove it introduced no
regression against the existing feature tree.

### TDD exemption (this plan ships no application code)

The [Test-Driven Development Convention](../../../repo-governance/development/workflow/test-driven-development.md)
mandates an explicit RED → GREEN → REFACTOR three-substep shape for every **code**-delivery step.
This plan has none. Its delivery steps produce prose, worked examples, and colocated runnable `code/`
samples that are **course material**, not application code: they ship no importable module, no test
target, and no runtime behaviour the app depends on. Their correctness is established by the
maker-checker-fixer pipeline documented above, which the source plan states verbatim:

> _Content authoring is a maker-checker-fixer cycle, not code TDD — no RED/GREEN/REFACTOR labels._

**If any step in this plan ever needs to touch app or lib code, that step is out of scope and must be
routed to the owning plan** — the exemption does not extend to smuggling code changes into a content
phase.

### Rule-15 three-tester retest exemption

Recorded with reasons in
[README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded). The exemption is
narrow: manual behavioural verification via Playwright MCP remains **mandatory and performed**, with
committed screenshot evidence. Only the `web-exploratory-tester` / `web-usability-tester` /
`web-design-tester` triad is waived, because the surface it would exercise belongs to the
navigation-UI plan.

### Rule-16 API exploratory retest — not applicable

This plan changes no REST or GraphQL endpoint and ships no API contract. `api-exploratory-tester` has
nothing to exercise.

## Dependencies

| Dependency                                                      | Kind       | Note                                                                 |
| --------------------------------------------------------------- | ---------- | -------------------------------------------------------------------- |
| `ayokoding-learning-path-01-url-restructure` merged             | hard, plan | populated flat `courses/` namespace + `courses/_index.md`            |
| `ayokoding-learning-path-02-schema-and-prerequisite-dag` merged | hard, plan | `syllabus/courses/` specs + the `prerequisites` frontmatter contract |
| `apps-ayokoding-www-by-example-maker` and its checker           | agent      | the By-Example bodies                                                |
| `apps-ayokoding-www-annotated-concept-maker` and its checker    | agent      | the Annotated-concept bodies                                         |
| `apps-ayokoding-www-primer-maker` and its checker               | agent      | the `just-enough-*` primer bodies                                    |
| `apps-ayokoding-www-general-maker` / `-general-checker`         | agent      | `drilling/overview.md` and general prose                             |
| `apps-ayokoding-www-facts-checker`                              | agent      | version-pinned / market / pre-1.0-stack fact verification            |
| `apps-ayokoding-www-link-checker`                               | agent      | intra-course and cross-course link integrity                         |
| `web-researcher`                                                | agent      | the per-course accuracy pre-verify (`V`) step                        |
| `apps-ayokoding-www-deployer`                                   | agent      | post-merge deploy to `prod-ayokoding-www`                            |
| `nx run ayokoding-www:build`                                    | Nx target  | renders the authored tree                                            |
| `rhino-cli md links validate` / `md heading-hierarchy validate` | CLI        | run as raw `cargo run`, not Nx targets                               |
| `npm run lint:md`                                               | npm script | markdownlint over the authored tree                                  |

**No new package dependency.** This plan adds no entry to `package.json`, `go.mod`, `Cargo.toml`, or
any other manifest.

## Rollback

Every artefact this plan produces is an **additive** new directory under `<COURSES>`. Nothing is
moved, renamed, or deleted, so rollback is subtractive and total:

- **Per band**: revert that band's merge commit. The bodies disappear; no other course is affected
  because bodies are content-independent (each writes only its own subtree). The corresponding
  band-completion signal is reverted with it, so the manifest plan sees no stale signal.
- **Per course**: `git rm -r <COURSES><course-id>/` plus removing its row from the catalog and its
  entry from `<COURSES>_index.md`. Safe **only** if no manifest already references the ID — check
  with the manifest plan first, since the reference direction is manifest → body.
- **Whole plan**: revert every band merge in reverse order. The `courses/` bucket returns to the 37
  re-homed bundles the URL-restructure plan placed there.

**The one-way door**: once a manifest references a course ID, deleting that body breaks
`checkManifestIntegrity` downstream. That is why the ordering is bodies-first, manifests-after — and
why this plan may never grow a manifest itself.

## Testing / Verification Strategy

| Level                     | What it verifies                                                                             | Mechanism                                                              |
| ------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Per-course content checks | concept coverage, register, format, worked-example volume, scope boundary                    | matching `apps-ayokoding-www-*-checker`                                |
| Per-course fact checks    | version-pinned / market / pre-1.0-stack facts; volatile facts confined to dated sidebars     | `apps-ayokoding-www-facts-checker`                                     |
| Per-course link checks    | intra-course and cross-course links resolve                                                  | `apps-ayokoding-www-link-checker`                                      |
| Contract assertions       | scope-boundary / forward-link / citation / concept-addition contracts are stated in the body | grep-checkable acceptance clauses on the authoring steps               |
| Structural                | bundle anatomy present; `prerequisites` declared                                             | `test -d` / `test -f` + frontmatter grep                               |
| Section build             | the authored tree renders                                                                    | `npx nx run ayokoding-www:build`                                       |
| Markdown quality          | markdownlint, link validation, heading hierarchy                                             | `npm run lint:md` + the two `rhino-cli md` subcommands                 |
| Regression                | no existing project's gates broke                                                            | `npx nx affected -t typecheck lint test:quick specs:behavior:coverage` |
| Manual behavioural        | a sample of authored course pages renders correctly at three breakpoints in `en`             | Playwright MCP + committed `evidence/` screenshots                     |

**Deliberately absent**: unit, integration, and e2e tests for this plan's own artefacts. There is no
application code here to test. The e2e suite that walks a course page is owned by the navigation-UI
plan; `ayokoding-www:test:e2e` and `ayokoding-www:test:integration` are no-op echo targets in this
workspace and are therefore never cited as evidence — the real e2e project is `ayokoding-www-fe-e2e`,
and it is not this plan's to run.
</content>
