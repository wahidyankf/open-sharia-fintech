# Path Manifest — `careers/immediately-effective/ai-engineer` (AI-engineer, from-scratch)

> **R3 custody exception (2026-07-21 ruling).** This file was renamed from
> `manifest-immediately-effective-software-engineer-to-ai-engineer.md`, and its framing is corrected
> here as a **deliberate, reasoned exception** to this plan's "no edits under `syllabus/`" custody rule
> (see [tech-docs §Custody rules](../../tech-docs.md#custody-rules-binding)). The path is **no longer a
> transition path** that assumes an already-working software engineer — it is a genuine **from-scratch**
> path. Its previously-**linked** software-engineer prerequisites are now **included** in `courseOrder`.
> **No new course body is authored for this correction** — every included prerequisite is an existing
> library course; the growth is a manifest-composition change only (2026-07-21 clarification to R3). The
> corrected top-matter and composition rules below are final; the **detailed stage-by-stage insertion**
> of the newly-included prerequisite courses (including their own transitive prerequisites) is
> **pending** and tracked as
> [delivery.md Phase 1.4](../../delivery.md#14-syllabus-custody-exception--ai-engineer-path-correction-r3)
> — deferred rather than invented here, because a prerequisite-consistent placement of a dozen-plus
> courses is manifest-authoring work, not a mechanical custody fix.

The **ordered manifest** for the from-scratch AI-engineer path: a **curated, prerequisite-consistent**
ordered list of **course IDs** over the [shared course library](../courses/README.md). This is the
authoritative reading order for this path; a course page under
`?path=careers/immediately-effective/ai-engineer` follows it for prev/next + breadcrumb. Persona: a
**reader with no assumed prior software-engineering competence** who wants to become immediately
effective at **building AI systems** (models, agents, evals, inference serving), not at driving coding
agents (D1).

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth** is
the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/ai-engineer.yaml`
(a standalone YAML/JSON data file in the `course-paths` feature, NOT `courseOrder` frontmatter on any
`_index.md`). Per
[tech-docs §Variable-depth `pathId`](../../tech-docs.md#variable-depth-pathid-careers-vs-skills--r2-r8),
the manifest also carries an explicit `arc: immediately-effective` field — the arc is a manifest field
independent of the URL grammar, which is what keeps a future `skills/<arc>/<subject>` shape purely
additive (R8). Path landing served at `/en/learn/paths/careers/immediately-effective/ai-engineer`. Order
rationale:
[tech-docs §Path `careers/immediately-effective/ai-engineer`](../../tech-docs.md#path-careersimmediately-effectiveai-engineer-fourth-path-corrected-2026-07-21).

## Composition (from-scratch AI-engineering path, corrected 2026-07-21 — was a transition spine)

A path over the shared library that **includes** its software-engineering prerequisites rather than
linking them. Unlike the three `careers/*` software-engineer-role paths, this path **is not a curated
fraction of the 121/127-course library** — it composes only the courses this AI-engineering journey
actually needs, from a from-scratch entry point through the AI-specific specialization spine. Its size
is stated as an **absolute count**, deliberately **not** as "N of 121" or "N of 127" (unchanged from the
prior framing — only the entry assumption and the linked-vs-included treatment changed).

- **Entry point — from-scratch, no assumed prior software-engineering competence (corrected, was D4)**:
  every course this path's AI-specific spine declares as a prerequisite is now **included** in
  `courseOrder` rather than linked out. The courses previously marked "linked, not included" —
  `just-enough-python`, `software-testing`, `cicd-and-release-engineering`, `backend-at-scale`,
  `containers-and-orchestration`, `computer-architecture`, `site-reliability-engineering`,
  `data-engineering`, `data-structures-and-algorithms-essentials`, `software-product-engineering`,
  `frontend-essentials` — must now be **present** in `courseOrder`, ordered prerequisite-consistently
  (each of these also declares its own further prerequisites, so the final included set is very likely
  larger than these 11 — see [Stage 0](#stage-0--software-engineering-foundation-from-scratch-entry--pending-detailed-ordering-r3)
  below). **No new course body is authored**: every one of these is an existing library course.
- **Scope — AI as material, not AI-assisted coding (D1, unchanged)**: this path teaches **building AI
  systems**. `agentic-coding` (driving AI coding agents — the engineer's own side) is deliberately
  **not** in this spine; it stays in the `careers/*` software-engineer-role paths.
- **AI-specialization spine (15 courses, unchanged by this correction)** — the AI/harness cluster (9)
  plus the six AI-engineer-role courses added to the library:
  - **From the existing AI/harness cluster (9)**: `creating-ai-powered-apps`, `agentic-ai`,
    `browser-automation-with-cdp`, `the-agent-loop`, `agent-tools-and-mcp`, `agent-context-and-memory`,
    `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`,
    `capstone-build-your-own-coding-agent`.
  - **The six AI-engineer-role courses**: `evaluating-ai-output-essentials`,
    `statistics-for-evaluation`, `evaluating-ai-systems-in-depth`,
    `product-patterns-for-probabilistic-systems`, `inference-serving-and-model-deployment`,
    `fine-tuning-and-adaptation`.
- **Deliberately kept out of the spine (judgment calls, flagged, unchanged)**:
  - `agentic-coding` — excluded per **D1** (AI-assisted coding is not this path's subject).
  - No DD-20 inter-topic capstones — those belong to the whole-library `careers/*` software-engineer
    paths.
  - `software-engineering-practices` — previously treated as a linked prerequisite; under the R3
    correction it is a **candidate for inclusion**, like the 11 courses named above, pending the same
    delivery-time re-composition.
- **Created bodies**: none — by this manifest or by this correction. Every included course, old and new
  to `courseOrder`, is an existing library course; this manifest only orders existing course IDs.
  **Prerequisite-consistent** ordering for the newly-included set is pending — see
  [Stage 0](#stage-0--software-engineering-foundation-from-scratch-entry--pending-detailed-ordering-r3)
  and the Smoothness notes.
- **Convergence (D2, unchanged)**: this path converges on the **AI-engineer endpoint** — a defensible
  evaluation discipline, a probabilistic feature shipped as a product, and self-hosted / adapted models —
  **not** the `careers/*` software-engineer paths' shared endpoint. Paths converge **per role, not
  globally**.

## Stage 0 · Software-engineering foundation (from-scratch entry — PENDING detailed ordering, R3)

> **Not yet ordered.** This stage records which courses must be included, not yet the
> prerequisite-consistent sequence they must appear in. See the pending-work callout at the top of this
> file and
> [delivery.md Phase 1.4](../../delivery.md#14-syllabus-custody-exception--ai-engineer-path-correction-r3).
> A deliberate scope decision made while correcting this file: the fixer that performed this rename did
> **not** chase the transitive prerequisite closure of the 11 courses below (several of them — e.g.
> `backend-at-scale`, `cicd-and-release-engineering` — themselves declare further prerequisites such as
> `backend-essentials`, `sql-essentials`, `security-essentials`, `version-control-and-git`,
> `software-engineering-practices`, `cloud-and-iac`). Computing the full closure and a
> prerequisite-consistent order over it is manifest-authoring work, not a mechanical custody fix, and is
> left for the delivery step below.

- `just-enough-python`, `data-structures-and-algorithms-essentials`, `frontend-essentials`,
  `software-product-engineering`, `software-testing`, `cicd-and-release-engineering`,
  `containers-and-orchestration`, `computer-architecture`, `backend-at-scale`,
  `site-reliability-engineering`, `data-engineering` — the 11 courses previously marked "linked, not
  included" in the retired transition framing; every one must now appear in `courseOrder`.

## Stage 1 · From one model call to a gated feature

1. `creating-ai-powered-apps`
2. `evaluating-ai-output-essentials` (the **light eval gate** — prereq `creating-ai-powered-apps`
   immediately above; placed early, before agents, so a learner can tell an improvement from a
   regression before adding retrieval and agency — D5)

## Stage 2 · Agents & the harness cluster

1. `agentic-ai`
2. `browser-automation-with-cdp`
3. `the-agent-loop`
4. `agent-tools-and-mcp`
5. `agent-context-and-memory`
6. `agent-permissions-and-sandboxing`
7. `agent-orchestration-subagents-and-observability`
8. `capstone-build-your-own-coding-agent`

## Stage 3 · Measuring what the agent does (evaluation depth)

1. `statistics-for-evaluation` (prereq `evaluating-ai-output-essentials` (Stage 1); a **hard**
   prerequisite of the deep course, placed immediately before it — D6)
2. `evaluating-ai-systems-in-depth` (the **deep evals** owner — hard prereqs `statistics-for-evaluation`
   (above) and `evaluating-ai-output-essentials` (Stage 1); also needs `agentic-ai` and
   `agent-orchestration-subagents-and-observability` (Stage 2) because agent trajectories are what make
   error analysis, derived criteria, and process scoring concrete — D5)

## Stage 4 · Shipping a probabilistic feature as a product

1. `product-patterns-for-probabilistic-systems` (hard prereqs `creating-ai-powered-apps` and
   `evaluating-ai-output-essentials` (both Stage 1) — satisfied since Stage 1. **Judgment call**: placed
   here, after the eval-depth stage, for the D5 arc — ship criteria written against a real measurement —
   though its earliest prerequisite-safe slot is right after the light gate in Stage 1)

## Stage 5 · Serving & adapting the model yourself

1. `inference-serving-and-model-deployment` (in-spine prereq `creating-ai-powered-apps` (Stage 1); its
   quantization example scores the model on the deep-eval suite, so placed after Stage 3)
2. `fine-tuning-and-adaptation` (placed last, framed as a decision skill per its deliberate de-emphasis —
   hard prereqs `evaluating-ai-systems-in-depth` (Stage 3), `statistics-for-evaluation` (Stage 3), and
   `inference-serving-and-model-deployment` (immediately above), plus `creating-ai-powered-apps` (Stage 1))

## Smoothness notes (RD-16)

- **From-scratch, not fast-because-competent (corrected, was D4)**: the software-engineer prerequisites
  are now **included**, not linked, and their prerequisite-consistent placement (Stage 0) is pending —
  see the callout above. This replaces the retired framing, which described the path as fast because it
  assumed competence.
- **Light gate early, deep evals after agents (D5)**: `evaluating-ai-output-essentials` sits right after
  the first working model call and before agents, answering "how will you know this works?";
  `evaluating-ai-systems-in-depth` waits until after the harness cluster, because agent trajectories are
  what make its material concrete. `statistics-for-evaluation` is a **hard** prerequisite of the deep
  course and is placed immediately before it (D6).
- **Prereq-chaining holds within Stages 1-5** (every course appears after all its in-spine
  prerequisites): light gate after `creating-ai-powered-apps`; statistics after the light gate; deep
  evals after statistics, `agentic-ai`, and `agent-orchestration-subagents-and-observability`;
  `fine-tuning-and-adaptation` after `evaluating-ai-systems-in-depth`, `statistics-for-evaluation`, and
  `inference-serving-and-model-deployment` (all hard prerequisites it declares). **Stage 0 is not yet
  ordered** (see above), so prerequisite-consistency for the whole manifest is not yet verified
  end-to-end.
- **Two ordering choices within Stages 1-5 are judgment calls, not prerequisites**:
  `product-patterns-for-probabilistic-systems` is placed after the eval-depth stage for narrative flow
  even though its hard prerequisites are satisfied as early as Stage 1; and `product-patterns` precedes
  `inference-serving-and-model-deployment` though neither depends on the other. Both follow the D5 arc,
  not a declared prerequisite.
- **Surgery ownership (surgery.md §S1)**: this path is the **owner** of the two eval courses (D5). S1
  places the light gate before RAG/agents and the deep course after agents here **by construction**. After
  S1 executes, re-verify (per surgery.md's four-manifest gate) that `evaluating-ai-output-essentials`
  still precedes the agent material and `statistics-for-evaluation` still precedes
  `evaluating-ai-systems-in-depth`.
- **Convergence (D2, unchanged)**: ends at the **AI-engineer endpoint** — a different endpoint from the
  three `careers/*` software-engineer paths, which is why the composition is a spine count rather than a
  fraction of the library.

See [tech-docs §Smoothness Architecture](../../tech-docs.md#smoothness-architecture-per-path).
