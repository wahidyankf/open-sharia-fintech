# Path Manifests — Curated Orderings Over the Shared Library

This folder holds the **path manifests** — the human-readable mirrors of the machine-consumed ordering
data. A **path** is an ordered, prerequisite-consistent list of **course IDs** over the
[shared course library](../courses/README.md); it composes existing course building blocks in a chosen
order and adds **zero new bodies** (every course body it names lives once in the library). **This plan
is careers-only** (R4, 2026-07-21 ruling): all four paths below sit under the `careers/` URL category
(`/en/learn/paths/careers/<arc>/<role>`), and `ayokoding-learning-path-05-manifests` owns exactly these
**4 careers manifests** — not 6. A sibling `skills/` category (`/en/learn/paths/skills/<subject>`,
2 manifests) exists in the wider programme but is owned **end-to-end** by a new "plan 06" (not yet
created as of this ruling; its exact folder identifier is not this plan's to invent); neither its
manifests nor its corpus live here. See
[tech-docs §Ownership split](../../tech-docs.md#ownership-split-careers-vs-skills--r4) for the full
accounting.

The **three software-engineer-role paths** all **converge on the same deep-mastery endpoint** (the
AI/harness cluster, internals builds, distributed systems, and the security capstone) — only the entry
point, journey ordering, teaching emphasis, and **which courses are curated into the spine** differ. A
**fourth path**, `careers/immediately-effective/ai-engineer`, is a **from-scratch specialization path**
(corrected 2026-07-21, R3 — it no longer assumes a working software engineer; every previously-linked
prerequisite is now **included** in `courseOrder`) that converges on a **different, AI-engineer
endpoint** — paths converge **per role, not globally** (D2; see
[tech-docs §Design Decisions](../../tech-docs.md#design-decisions)). See the
[syllabus root README](../README.md) for the full course-vs-path architecture.

Every manifest also carries an explicit `arc` field (`interview-ready` | `immediately-effective` |
`fundamentally-strong`), independent of the URL grammar — see
[tech-docs §Variable-depth `pathId`](../../tech-docs.md#variable-depth-pathid-careers-vs-skills--r2-r8)
(R2, R8).

## Curated + converge (LOCKED decision, 2026-07-19)

The three software-engineer-role paths are **not all comprehensive** — not every course appears in every
path. Each is a **curated subset ordering** over the one prerequisite DAG:

- **`careers/fundamentally-strong/software-engineer`** is the **complete-mastery** path: it includes
  **all 121 software-engineer-role courses** in a theory-first ordering and is the only
  software-engineer-role path that omits none of them. (The six AI-engineer-role courses this plan added
  to the library are **not** in it — they compose only the fourth, AI-engineer path; per-role
  convergence, D2.)
- **`careers/interview-ready/software-engineer`** teaches an **interview + core + production spine**,
  then offers the deep-systems / OS / kernel / compilers / internals-builds / niche courses as an
  explicit optional **"Go deeper" tail** — reachable, but never required for interview-readiness.
- **`careers/immediately-effective/software-engineer`** teaches a **build-first spine** (ship a real app
  first), then defers the heavy theory (CS foundations, type systems, advanced algorithms, paradigms,
  computer architecture, and the rest of the CS/systems depth) into a later **Deepening band**.

The **fourth path**, `careers/immediately-effective/ai-engineer`, is different in kind: not a curated
ordering over the whole library but a **from-scratch AI-specific specialization** (corrected 2026-07-21,
R3 — was a transition spine that assumed a working software engineer). Its previously-linked
software-engineer prerequisites are now **included** in `courseOrder`, and it composes the AI/harness
cluster plus the six AI-engineer-role courses this plan added — so its size is stated as an absolute
count, **not** a fraction of the library.

The curated paths **genuinely omit** a small, curriculum-judged set of niche courses (never a
prerequisite of anything they include, so each manifest stays **prerequisite-closed**). Every course a
path includes appears **after all of its prerequisites** — a property machine-verified for all four
manifests.

**DD-20 addendum (2026-07-19)**: the 127-course catalog includes seven inter-topic capstones
reconciled in from other topics' embedded specs (`capstone-solid-core` plus six new capstones — see
[tech-docs DD-20](../../tech-docs.md#design-decisions)). All seven are included in all three
software-engineer-role manifests (none is genuinely omitted); each is placed at its earliest
prerequisite-safe position. The fourth (AI-engineer) manifest does not carry the DD-20 inter-topic
capstones — it is a specialization spine, not a whole-library ordering.

Each manifest is the **human-readable mirror**. The **machine-consumed source of truth** is a standalone
data file at `apps/ayokoding-www/src/features/course-paths/manifests/<path-id>.yaml` (nested to mirror
the slash-form path id — e.g. `manifests/careers/interview-ready/software-engineer.yaml`). Path landing
pages are served at `/en/learn/paths/<path-id>`; a course page reads path context via `?path=<path-id>`
and its prev/next + breadcrumb follow that path's ordering. `<path-id>` is `careers/<arc>/<role>` for
every path in this folder (R1, R2) — see
[tech-docs §Variable-depth `pathId`](../../tech-docs.md#variable-depth-pathid-careers-vs-skills--r2-r8).

## The paths

All four path ids below share the `careers/` category segment (R1); it is omitted as its own table
column since every row carries it.

| Path id (under `careers/`)                | Persona                                                                    | Shape                                                                                                                        | Manifest                                                          |
| ----------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| `interview-ready/software-engineer`       | Experienced engineer re-entering the job market                            | Interview/production **spine** + optional **Go deeper tail** (116 courses)                                                   | [manifest](./manifest-interview-ready-software-engineer.md)       |
| `immediately-effective/software-engineer` | Builder who wants to be effective fast                                     | Build-first **spine** + **Deepening band** (119 courses)                                                                     | [manifest](./manifest-immediately-effective-software-engineer.md) |
| `fundamentally-strong/software-engineer`  | Learner who wants university-style depth                                   | Theory-first, **all 121 software-engineer-role courses** (complete mastery)                                                  | [manifest](./manifest-fundamentally-strong-software-engineer.md)  |
| `immediately-effective/ai-engineer`       | Reader with no assumed prior SWE competence, specializing directly into AI | From-scratch **AI-specific specialization** — 15-course AI spine (Stages 1-5) + a pending from-scratch entry stage (Stage 0) | [manifest](./manifest-immediately-effective-ai-engineer.md)       |

- **`interview-ready`** was formerly `job-seeking`.
- **`immediately-effective`** was formerly the `fundamentally-strong` shipping-first path.
- **`fundamentally-strong`** is the new university-style path, and is also the library/section brand.
- **`immediately-effective/ai-engineer`** is new (this plan) — the first AI-engineer-role path (D3); its
  landing is served at `/en/learn/paths/careers/immediately-effective/ai-engineer`. **Corrected
  2026-07-21 (R3, custody exception)**: originally modelled and named as a software-engineer→AI-engineer
  _transition_ path (`immediately-effective/software-engineer-to-ai-engineer`, prerequisites linked, not
  included); it is now a genuine from-scratch path and its mirror file was renamed to
  `manifest-immediately-effective-ai-engineer.md`. See
  [tech-docs §Custody rules](../../tech-docs.md#custody-rules-binding).

## How to read a manifest

Each manifest is an **ordered list of course IDs** grouped into phases/stages, with a short composition
rationale, an ordered spine, an optional-tail / deepening-band section for the deferred-or-deeper courses,
and smoothness notes (RD-16). Order is a per-path property; it is **not** a catalog property (the
[catalog](../courses/README.md) is order-neutral).

Every manifest is **prerequisite-consistent**: it is a valid topological entry into the library's
prerequisite DAG, so every `just-enough-<lang>` primer — and every prerequisite course — precedes its
first use within that path. A course a path relegates to its optional tail or deepening band is still
present in that path (just out of the required spine); a course a path genuinely omits appears only in
the paths that include it. Each course's own **"In which paths"** section names the exact section it sits
in for every path that carries it.

---

← Back to the [syllabus root README](../README.md)
