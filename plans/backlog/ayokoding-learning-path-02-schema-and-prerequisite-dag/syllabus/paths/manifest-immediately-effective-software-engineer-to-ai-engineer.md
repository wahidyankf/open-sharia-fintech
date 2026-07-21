# Path Manifest — `immediately-effective/software-engineer-to-ai-engineer` (AI-engineer transition)

The **ordered manifest** for the software-engineer→AI-engineer transition path: a **curated,
prerequisite-consistent** ordered list of **course IDs** over the
[shared course library](../courses/README.md). This is the authoritative reading order for this path; a
course page under `?path=immediately-effective/software-engineer-to-ai-engineer` follows it for prev/next

- breadcrumb. Persona: a **working software engineer specializing into AI engineering** — assumes
  software-engineer competence and teaches **building AI systems** fast, not using AI to code faster (D1).

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth** is
the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/immediately-effective/software-engineer-to-ai-engineer.yaml`
(a standalone YAML/JSON data file in the `course-paths` feature, NOT `courseOrder` frontmatter on any
`_index.md`). Path landing served at
`/en/c/learn/paths/immediately-effective/software-engineer-to-ai-engineer`. Order rationale:
[tech-docs §Path `immediately-effective/software-engineer-to-ai-engineer`](../../tech-docs.md#path-immediately-effectivesoftware-engineer-to-ai-engineer-fourth-path-added-2026-07-20).

## Composition (short AI-specific spine, NEW 2026-07-20)

A **short AI-specific specialization spine** (D4), not a curated ordering over the whole library. Unlike
the three software-engineer-role paths, this path **is not a fraction of the 121/127-course library** — it
**assumes a working software engineer** and teaches only the AI-engineer transition. Its size is stated as
an **absolute count of 15 courses**, deliberately **not** as "N of 121" or "N of 127".

- **Entry point — a working software engineer (D4)**: every software-engineer prerequisite is **linked,
  not included**. A learner arrives here having completed (or able to skip into)
  `immediately-effective/software-engineer` or equivalent. The courses this spine's members declare as
  prerequisites but does not list — `just-enough-python`, `software-testing`,
  `cicd-and-release-engineering`, `backend-at-scale`, `containers-and-orchestration`,
  `computer-architecture`, `site-reliability-engineering`, `data-engineering`,
  `data-structures-and-algorithms-essentials`, `software-product-engineering`, `frontend-essentials` —
  are assumed and reached via each course page's prerequisite links, never re-taught here.
- **Scope — AI as material, not AI-assisted coding (D1)**: this path teaches **building AI systems**.
  `agentic-coding` (driving AI coding agents — the engineer's own side) is deliberately **not** in this
  spine; it stays in the software-engineer paths.
- **Composed courses (15)** — the AI/harness cluster (9) plus the six AI-engineer-role courses this plan
  authored:
  - **From the existing AI/harness cluster (9)**: `creating-ai-powered-apps`, `agentic-ai`,
    `browser-automation-with-cdp`, `the-agent-loop`, `agent-tools-and-mcp`, `agent-context-and-memory`,
    `agent-permissions-and-sandboxing`, `agent-orchestration-subagents-and-observability`,
    `capstone-build-your-own-coding-agent`.
  - **The six new AI-engineer-role courses**: `evaluating-ai-output-essentials`,
    `statistics-for-evaluation`, `evaluating-ai-systems-in-depth`,
    `product-patterns-for-probabilistic-systems`, `inference-serving-and-model-deployment`,
    `fine-tuning-and-adaptation`.
- **Deliberately kept out of the spine (judgment calls, flagged)**:
  - `agentic-coding` — excluded per **D1** (AI-assisted coding is not this path's subject).
  - `software-engineering-practices` — treated as a **linked software-engineer prerequisite** (a general
    code-review / CI / quality-gate practices course a working engineer already holds), so the spine
    opens at `creating-ai-powered-apps` exactly as the D5 order states. **Judgment call**: the two
    software-engineer manifests place `software-engineering-practices` at the head of their AI & harness
    section; a reviewer who prefers to open this spine with it instead would carry **16** courses. The
    D5 order starts at `creating-ai-powered-apps`, so the conservative reading links it out.
  - No DD-20 inter-topic capstones — those belong to the whole-library software-engineer paths.
- **Created bodies**: none by this manifest. The six new courses are added to the shared **library**
  (available to every path) and authored elsewhere in this plan; this manifest only orders existing
  course IDs. **Prerequisite-consistent** — see the Smoothness notes for the per-course prerequisite
  trace.
- **Convergence (D2)**: this path converges on the **AI-engineer endpoint** — a defensible evaluation
  discipline, a probabilistic feature shipped as a product, and self-hosted / adapted models — **not** the
  software-engineer paths' shared endpoint. Paths converge **per role, not globally**.

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

- **Fast because it assumes competence, not because it skips depth (D4)**: the software-engineer
  prerequisites are **linked** and reachable from each course page, never re-taught. That is what
  "immediately effective" means for a specialization.
- **Light gate early, deep evals after agents (D5)**: `evaluating-ai-output-essentials` sits right after
  the first working model call and before agents, answering "how will you know this works?";
  `evaluating-ai-systems-in-depth` waits until after the harness cluster, because agent trajectories are
  what make its material concrete. `statistics-for-evaluation` is a **hard** prerequisite of the deep
  course and is placed immediately before it (D6).
- **Prereq-chaining holds** (every course appears after all its in-spine prerequisites): light gate after
  `creating-ai-powered-apps`; statistics after the light gate; deep evals after statistics, `agentic-ai`,
  and `agent-orchestration-subagents-and-observability`; `fine-tuning-and-adaptation` after
  `evaluating-ai-systems-in-depth`, `statistics-for-evaluation`, and
  `inference-serving-and-model-deployment` (all hard prerequisites it declares).
- **Two ordering choices are judgment calls, not prerequisites**:
  `product-patterns-for-probabilistic-systems` is placed after the eval-depth stage for narrative flow
  even though its hard prerequisites are satisfied as early as Stage 1; and `product-patterns` precedes
  `inference-serving-and-model-deployment` though neither depends on the other. Both follow the D5 arc, not
  a declared prerequisite.
- **Surgery ownership (surgery.md §S1)**: this path is the **owner** of the two eval courses (D5). S1
  places the light gate before RAG/agents and the deep course after agents here **by construction**. After
  S1 executes, re-verify (per surgery.md's four-manifest gate) that `evaluating-ai-output-essentials`
  still precedes the agent material and `statistics-for-evaluation` still precedes
  `evaluating-ai-systems-in-depth`.
- **Convergence (D2)**: ends at the **AI-engineer endpoint** — a different endpoint from the three
  software-engineer paths, which is why the composition is a spine count rather than a fraction of the
  library.

See [tech-docs §Smoothness Architecture](../../tech-docs.md#smoothness-architecture-per-path).
