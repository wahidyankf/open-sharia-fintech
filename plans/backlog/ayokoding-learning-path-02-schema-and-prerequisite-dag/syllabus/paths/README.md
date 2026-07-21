# Path Manifests — Curated Orderings Over the Shared Library

This folder holds the **path manifests** — the human-readable mirrors of the machine-consumed ordering
data. A **path** is an ordered, prerequisite-consistent list of **course IDs** over the
[shared course library](../courses/README.md); it composes existing course building blocks in a chosen
order and adds **zero new bodies** (every course body it names lives once in the library). The **three
software-engineer-role paths** all **converge on the same deep-mastery endpoint** (the AI/harness
cluster, internals builds, distributed systems, and the security capstone) — only the entry point,
journey ordering, teaching emphasis, and **which courses are curated into the spine** differ. A **fourth
path**, `immediately-effective/software-engineer-to-ai-engineer`, is a **role-to-role specialization
spine** that assumes a working software engineer and converges on a **different, AI-engineer endpoint** —
paths converge **per role, not globally** (D2; see
[tech-docs §Design Decisions](../../tech-docs.md#design-decisions)). See the
[syllabus root README](../README.md) for the full course-vs-path architecture.

## Curated + converge (LOCKED decision, 2026-07-19)

The three software-engineer-role paths are **not all comprehensive** — not every course appears in every
path. Each is a **curated subset ordering** over the one prerequisite DAG:

- **`fundamentally-strong/software-engineer`** is the **complete-mastery** path: it includes **all 121
  software-engineer-role courses** in a theory-first ordering and is the only software-engineer-role path
  that omits none of them. (The six AI-engineer-role courses this plan added to the library are **not**
  in it — they compose only the fourth, AI-engineer path; per-role convergence, D2.)
- **`interview-ready/software-engineer`** teaches an **interview + core + production spine**, then offers
  the deep-systems / OS / kernel / compilers / internals-builds / niche courses as an explicit optional
  **"Go deeper" tail** — reachable, but never required for interview-readiness.
- **`immediately-effective/software-engineer`** teaches a **build-first spine** (ship a real app first),
  then defers the heavy theory (CS foundations, type systems, advanced algorithms, paradigms, computer
  architecture, and the rest of the CS/systems depth) into a later **Deepening band**.

The **fourth path**, `immediately-effective/software-engineer-to-ai-engineer`, is different in kind: not
a curated ordering over the whole library but a **short AI-specific specialization spine** (D4). It
assumes a working software engineer (its software-engineer prerequisites are **linked, not included**)
and composes the AI/harness cluster plus the six AI-engineer-role courses this plan added — so its size
is stated as an absolute count, **not** a fraction of the library.

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
the slash-form path id — e.g. `manifests/interview-ready/software-engineer.yaml`). Path landing pages are
served at `/en/c/learn/paths/<path-id>`; a course page reads path context via `?path=<path-id>` and its
prev/next + breadcrumb follow that path's ordering.

## The paths

| Path id                                                  | Persona                                         | Shape                                                                       | Manifest                                                                         |
| -------------------------------------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| `interview-ready/software-engineer`                      | Experienced engineer re-entering the job market | Interview/production **spine** + optional **Go deeper tail** (116 courses)  | [manifest](./manifest-interview-ready-software-engineer.md)                      |
| `immediately-effective/software-engineer`                | Builder who wants to be effective fast          | Build-first **spine** + **Deepening band** (119 courses)                    | [manifest](./manifest-immediately-effective-software-engineer.md)                |
| `fundamentally-strong/software-engineer`                 | Learner who wants university-style depth        | Theory-first, **all 121 software-engineer-role courses** (complete mastery) | [manifest](./manifest-fundamentally-strong-software-engineer.md)                 |
| `immediately-effective/software-engineer-to-ai-engineer` | Working software engineer specializing into AI  | Short **AI-specific specialization spine** (15 courses)                     | [manifest](./manifest-immediately-effective-software-engineer-to-ai-engineer.md) |

- **`interview-ready`** was formerly `job-seeking`.
- **`immediately-effective`** was formerly the `fundamentally-strong` shipping-first path.
- **`fundamentally-strong`** is the new university-style path, and is also the library/section brand.
- **`immediately-effective/software-engineer-to-ai-engineer`** is new (this plan) — the first
  AI-engineer-role path (D3); its landing is served at
  `/en/c/learn/paths/immediately-effective/software-engineer-to-ai-engineer`.

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
