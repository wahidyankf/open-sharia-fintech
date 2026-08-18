# Technical Documentation — Learning Path Schema and Prerequisite DAG

## Corpus Disposition

`archive-with-plan` — this plan custodies its `syllabus/` corpus and no consumer **outside `plans/`**
reads it: no checker, agent, Nx target, build/generation step, or shipped content front-matter names a
syllabus path (the consumers are the sibling `plans/` — plans 04 and 05 — which do not trigger
promotion). The corpus therefore moves to `plans/done/` with the plan folder on archival; the
promotion trigger (name a non-plan reader) is not met. See
[Learning-Plan Syllabus Convention §Corpus Disposition](../../../repo-governance/conventions/structure/learning-plan-syllabus/corpus-disposition.md#corpus-disposition).

## Overview

This plan creates the `course-paths` feature's **pure functional core** inside `ayokoding-www`, plus
the two data contracts it operates over: the **course-prerequisite frontmatter contract** and the
**`PathManifest` schema**. It creates no component, no route, and no rendered page.

`ayokoding-www` is a Next.js app [Repo-grounded — `apps/ayokoding-www/next.config.ts`,
`apps/ayokoding-www/src/app/[locale]/(content)/[...slug]/page.tsx`] following the repo's
**functional-core/imperative-shell** feature layout, `src/features/<name>/{core,shell}`
[Repo-grounded — `apps/ayokoding-www/src/features/{content,navigation}/{core,shell}` all exist]. The
`course-paths` feature is **new**: `test -d apps/ayokoding-www/src/features/course-paths` returns
non-zero on `origin/main` today [Repo-grounded — verified 2026-07-21]. This plan creates its `core/`
half; `ayokoding-learning-path-03-navigation-ui` creates its `shell/` half.

## Path constants

Used throughout this document and `delivery.md`. Reproduced verbatim in all five split plans — a
checklist whose `<FEAT>` placeholders cannot be expanded is not executable.

> **On-disk slug vs. served URL — the `/c/` namespace.** Every path below is an **on-disk content
> path**; the URL it is served at is **not** the same string. `contentUrl` maps every content-tree
> slug to `/{locale}/c/{slug}`. Repo-grounded:
> `apps/ayokoding-www/src/features/content/core/content-url.ts` returns a
> `/{locale}/c/{normalized}` template literal for every content-tree slug; only the two per-locale
> `LOOSE_PAGE_ALLOWLIST` top-level pages and the empty/`_index` slug escape the `/c/` namespace, and
> seven assertions in `content-url.test.ts` pin it. So the on-disk `content/en/learn/courses/x/` is
> served at `/en/c/learn/courses/x`, and the Indonesian mirror root `content/id/belajar/` is served
> at `/id/c/belajar`. **This plan does not change that namespace** — it only appends an optional
> `?path=` query string.

- `<PLAN>` = this plan's own folder at its current stage —
  `plans/in-progress/ayokoding-learning-path-02-schema-and-prerequisite-dag` once promoted,
  `plans/backlog/ayokoding-learning-path-02-schema-and-prerequisite-dag` before then (no trailing
  slash). Promotion happens **before Phase 0 runs**, so no command or table row hardcodes a stage
  prefix; `delivery.md`'s first Phase 0 step resolves `<PLAN>` once and the executor expands it
  textually thereafter — see
  [delivery.md §Path constants](./delivery.md#path-constants)
- `<COURSES>` = `apps/ayokoding-www/content/en/learn/courses/` (course bundles; served at `/en/c/learn/courses/<course-id>`)
- `<PATHS>` = `apps/ayokoding-www/content/en/learn/paths/` (thin path-landing anchors; served at `/en/c/learn/paths/<path-id>`)
- `<SE_OLD>` = `apps/ayokoding-www/content/en/learn/fundamentally-strong/software-engineer/` (legacy home of the 33 shipped topics + 4 existing capstones, incl. `capstone-solid-core` — the re-home source)
- `<FEAT>` = `apps/ayokoding-www/src/features/course-paths/`
- `<MANIFESTS>` = `<FEAT>manifests/` (standalone YAML data files, nested to mirror slash path ids —
  `<MANIFESTS><path-id>.yaml`; `<path-id>` is **variable-depth**: `careers/<arc>/<role>` (3 segments) or
  `skills/<subject>` (2 segments) — see
  [§Variable-depth `pathId`](#variable-depth-pathid-careers-vs-skills--r2-r8))
- `<LEGACY>` = `apps/ayokoding-www/content/en/learn/legacy/` (**new bucket**, scope extension; served at `/en/c/learn/legacy/<domain>/…`)
- `<REDIR>` = `apps/ayokoding-www/src/redirects/`
- `<SPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`
- `<NAVSPECS>` = `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/navigation/` (existing domain — the three-bucket Gherkin lands beside `content-namespace-redirects.feature`, whose own scenarios pin the `/c/` namespace: `/en/learn/software-engineering` 308-redirects to `/en/c/learn/software-engineering`)
- **This plan is careers-only** (R4): the 4 path ids it owns are `careers/interview-ready/software-engineer`,
  `careers/immediately-effective/software-engineer`, `careers/fundamentally-strong/software-engineer`,
  `careers/immediately-effective/ai-engineer` (fourth path, corrected 2026-07-21 — see
  [§Path `careers/immediately-effective/ai-engineer`](#path-careersimmediately-effectiveai-engineer-fourth-path-corrected-2026-07-21) —
  manifest at `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml`). A sibling `skills/` category
  (**4** path ids as of amendment A10 — `skills/conventional-accounting`, `skills/sharia-accounting`,
  `skills/conventional-erp`, `skills/sharia-erp` — up from the original two) exists in the wider
  programme but is out of this plan's scope — see [§Ownership split](#ownership-split-careers-vs-skills--r4).

## Architecture — the pure core this plan builds

```text
apps/ayokoding-www/src/features/course-paths/          # NEW feature — this plan creates core/
├── core/                      # PURE — no IO. THIS PLAN.
│   ├── schemas.ts             # PathManifest zod schema (pathId, title, description, courseOrder[])
│   ├── manifest.ts            # PathManifest type + course-ref normalization (id | {id, framing})
│   ├── path-nav.ts            # resolvePathNav(manifest, courseId) -> {prev, next} (pure)
│   ├── path-context.ts        # parsePathContext(searchParams, manifests) -> pathId | null
│   ├── prerequisites.ts       # resolvePrerequisites + checkPrerequisiteConsistency (pure)
│   ├── manifest-integrity.ts  # checkManifestIntegrity(manifest, libraryCourseIds) (pure)
│   └── *.test.ts              # unit tests for every resolver, checker, and the context parser
├── manifests/                 # THIS PLAN creates the directory + README.md, EMPTY of .yaml
│   └── README.md              # notes that <path-id>.yaml data files land here later
└── shell/                     # NOT this plan — ayokoding-learning-path-03-navigation-ui
```

Plus one edit outside the feature:
`apps/ayokoding-www/src/features/content/core/content-url.ts` [Repo-grounded — file exists] gains an
optional `pathId` param appending `?path=<path-id>`. Its canonical shape —
`/en/c/learn/courses/<course-id>` — is the `/c/`-namespaced URL the function **already** emits and is
preserved unchanged; see the `/c/` note under [Path constants](#path-constants).

### Module interaction

```mermaid
%% Component interactions inside the course-paths pure core, and the two boundaries it touches.
%% Node SHAPE encodes ownership: rectangle = built by THIS plan, stadium = built downstream,
%% cylinder = data contract. Edge STYLE: solid = direct call/import, dotted = downstream consumption.
%% Colours are the repo's verified colour-blind-friendly palette and are redundant with shape.
flowchart TD
    SCHEMA["schemas.ts<br/>PathManifest zod"]:::mine
    MAN["manifest.ts<br/>course-ref normalization"]:::mine
    NAV["path-nav.ts<br/>resolvePathNav"]:::mine
    CTX["path-context.ts<br/>parsePathContext"]:::mine
    PRQ["prerequisites.ts<br/>resolvePrerequisites<br/>+ consistency check"]:::mine
    INT["manifest-integrity.ts<br/>checkManifestIntegrity"]:::mine
    URL["content-url.ts<br/>contentUrl(…, pathId?)"]:::mine

    FM[("prerequisites: frontmatter<br/>contract")]:::data
    YAML[("MANIFESTS &lt;path-id&gt;.yaml<br/>data files")]:::data

    REPO(["manifest-repository.ts<br/>navigation-ui plan"]):::downstream
    UI(["shell components<br/>navigation-ui plan"]):::downstream

    SCHEMA --> MAN
    MAN --> NAV
    MAN --> INT
    SCHEMA --> CTX
    FM --> PRQ
    MAN --> PRQ
    YAML --> SCHEMA

    NAV -.->|"prev/next neighbours"| UI
    CTX -.->|"active pathId or null"| UI
    PRQ -.->|"prerequisite refs"| UI
    URL -.->|"links carrying ?path="| UI
    SCHEMA -.->|"validates every loaded manifest"| REPO
    INT -.->|"build-time integrity gate"| REPO

    classDef mine fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef data fill:#029E73,stroke:#000000,color:#FFFFFF
    classDef downstream fill:#DE8F05,stroke:#000000,color:#000000
```

**Accessibility note.** Ownership is carried by node shape (rectangle = this plan, stadium =
downstream, cylinder = data contract) **and** by each node's own label naming its owning plan, never
by colour alone. Call direction versus downstream consumption is carried by line style (solid versus
dotted) **and** by the edge labels. Fills use the verified accessible palette (`#0173B2` blue,
`#029E73` teal, `#DE8F05` orange) with black borders and WCAG-AA-contrasting text, per the
[Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md).

## Course-block schema

Each course block carries this canonical metadata (the body is authored once and never forked):

| Field                           | Meaning                                                                                                                                            |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `course-id`                     | Stable kebab-case slug (e.g. `coding-interview`). No numeric order prefix — order is a per-path property, never a body property.                   |
| Canonical body                  | One bundle at `content/en/learn/courses/<course-id>/`, one canonical URL.                                                                          |
| `prerequisites: [course-id, …]` | **EVERY course declares this.** The union of all `prerequisites` edges forms the library's **prerequisite DAG**. Entry-point courses declare `[]`. |
| Format                          | `Primer` / `By Example` / `Annotated-concept` (or a capstone milestone kind).                                                                      |
| Primary language                | The course's primary teaching language (or `none` for concept-only).                                                                               |

Additional rules:

- **Prerequisites are surfaced on the page.** The canonical course page renders its declared
  `prerequisites` (each linking to its own canonical course). This is path-independent — it is the
  body's own honest dependency statement. (The rendering itself is
  `ayokoding-learning-path-03-navigation-ui`'s; the resolver behind it is this plan's.)
- **Manifests must be prerequisite-consistent.** Every path's `courseOrder` must be a **valid
  topological ordering**: no course precedes any of its prerequisites **within that path's order**.
  This is a machine-checkable gate — see
  [Manifest integrity invariants](#manifest-integrity-invariants-verified-as-gates--unit-tests).
- **Per-path framing is a callout, never a body fork.** A path may attach an optional lightweight
  intro/outro framing callout around a shared block; the shared body itself is never modified per path.
- **Path context via `?path=<path-id>`.** Prev/next + breadcrumb follow that path's manifest ordering;
  no context → canonical standalone view.

## The prerequisite frontmatter contract (canonical here)

> **Canonical owner: this plan.** `ayokoding-learning-path-01-url-restructure` **writes** this field
> into 37 re-homed `_index.md` files while this plan **defines its shape**. Both plans are Wave 1 and
> merge independently, so nothing serialises them — which is why the contract is **reproduced
> verbatim in both plans' `tech-docs.md`** rather than linked across folders. **If the two statements
> ever diverge, this plan's wins.**

The contract, stated in full:

```yaml
# apps/ayokoding-www/content/en/learn/courses/<course-id>/_index.md — frontmatter
prerequisites:
  - data-structures-and-algorithms-essentials
  - just-enough-python
```

Binding rules:

1. The key is exactly `prerequisites` — lowercase, plural, no prefix, no namespace.
2. Its value is a **YAML sequence of course-ID strings**. Each string is a stable kebab-case course
   slug, identical to the course's directory name under `<COURSES>`.
3. An entry-point course with no prerequisites declares an **empty sequence** (`prerequisites: []`),
   never an omitted key and never `null`. The resolver treats an omitted key as an empty list, but a
   body that omits the key is a contract violation, because a missing declaration and a deliberate
   "no prerequisites" are then indistinguishable to a reviewer.
4. IDs reference **courses**, never paths, never URLs, never file paths.
5. The list is **unordered** — it is a set of edges into the DAG, not a reading order. Order is the
   manifest's job (DD-1).
6. A referenced ID that is not in the library is a **resolver miss**, not a crash:
   `resolvePrerequisites` returns only the IDs it can resolve, and `checkPrerequisiteConsistency`
   reports the rest.

**Why this failure mode is dangerous.** The field is inert until a Wave-2 consumer reads it. If
`ayokoding-learning-path-01-url-restructure` writes a shape this plan's resolver does not parse —
say a comma-separated string, or a nested `meta.prerequisites` — **nothing fails in Wave 1**. Both
plans merge green. The defect surfaces much later, inside
`ayokoding-learning-path-03-navigation-ui`, as 37 course pages rendering an empty prerequisite list
with a passing build and no error anywhere. Duplication of a six-line contract is a cheap insurance
premium against that.

## Prerequisite DAG (illustrative excerpt)

The full DAG is the union of every course's `prerequisites` edges. A representative slice:

```mermaid
%% Color Palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC — WCAG-AA, CB-friendly.
%% Node colour is redundant with position in the arc: entry-point (blue), shared depth (teal),
%% interview technique (orange), capstone (purple). Every edge direction is explicit.
flowchart TD
    PY["just-enough-python"]:::blue
    DSA["data-structures-and-<br/>algorithms-essentials"]:::teal
    ADV["advanced-algorithms"]:::teal
    CI["coding-interview"]:::orange
    SQL["sql-essentials"]:::teal
    BE["backend-essentials"]:::teal
    NET["networking-essentials"]:::teal
    SDI["system-design-interview"]:::orange
    CIL["capstone-interview-loop"]:::purple

    PY --> DSA --> ADV --> CI
    PY --> SQL --> BE
    PY --> NET
    BE --> SDI
    NET --> SDI
    SQL --> SDI
    CI --> CIL
    SDI --> CIL

    classDef blue fill:#0173B2,stroke:#000,color:#fff,stroke-width:2px
    classDef teal fill:#029E73,stroke:#000,color:#fff,stroke-width:2px
    classDef orange fill:#DE8F05,stroke:#000,color:#fff,stroke-width:2px
    classDef purple fill:#CC78BC,stroke:#000,color:#fff,stroke-width:2px
```

Each of the four path manifests is a distinct topological walk over this DAG that respects every
edge. `checkPrerequisiteConsistency` is the function that proves a given walk respects them.

## Path = ordered manifest (manifest format)

- A **path** is a manifest: a **path ID**, an **arc**, a display **title**, a **description**, and an
  ordered **`courseOrder`** list of course IDs. See
  [§Variable-depth `pathId`](#variable-depth-pathid-careers-vs-skills--r2-r8) for why `arc` is its own
  field, separate from `pathId`.
- **Storage**: each manifest is a standalone data file under `<MANIFESTS>` — the loader globs
  `manifests/**/*.yaml` and a **slash in a path ID becomes a nested directory** (e.g.
  `manifests/careers/interview-ready/software-engineer.yaml`, or, for the 2-segment `skills/` category
  owned by two separate plans, `manifests/skills/conventional-erp.yaml`). This data file is
  the **single machine-consumed source of truth** for the path — it is NOT `courseOrder` frontmatter on
  any content `_index.md`.

  ```yaml
  # apps/ayokoding-www/src/features/course-paths/manifests/careers/interview-ready/software-engineer.yaml
  pathId: careers/interview-ready/software-engineer
  arc: interview-ready
  title: "Interview-Ready Software Engineer"
  description: "Interview-first track for an experienced engineer re-entering the market."
  courseOrder:
    - just-enough-nvim
    - just-enough-lua
    - extending-neovim
    - just-enough-python
    - capstone-forge-ready
    # … ordered course IDs, prerequisite-consistent …
  ```

- **Human-readable mirror**: the per-path files under `syllabus/paths/` in this plan folder are the
  human-readable orderings used during authoring and review. The machine-consumed source of truth is
  the nested `manifests/**/*.yaml` data file above.
- **Course reference**: each `courseOrder` entry is a course ID string, optionally a mapping
  `{ id, framing?: { intro?, outro? } }` when the path adds a **lightweight per-course framing**
  callout. The framing is rendered by the path layer around the shared body; the body itself is never
  modified. `manifest.ts` normalizes both forms to one internal shape so no downstream caller has to
  branch on it.

## Variable-depth `pathId` (careers vs. skills — R2, R8)

**Ruling, 2026-07-21.** `pathId` is the slash-shaped id after `paths/`, and it is **variable-depth by
design**: `careers/<arc>/<role>` (3 segments) or `skills/<subject>` (2 segments). This plan's schema,
`?path=` parser (`path-context.ts`), and `<MANIFESTS>` directory globbing must all handle **both**
depths from day one, without hardcoding either — and this plan is careers-only (R4), so it is the
`careers/` (3-segment) shape that this plan's own four manifests actually instantiate; the 2-segment
shape is exercised only via unit-test fixtures proving the code does not silently assume 3 segments.

- **Do NOT hardcode a 3-segment assumption anywhere** — not in `schemas.ts`'s zod refine, not in
  `path-context.ts`'s parsing, not in the `<MANIFESTS>` glob pattern (`manifests/**/*.yaml` already
  matches any depth; nothing here needs to change for that reason alone).
- **Do NOT encode "skills always has exactly 2 segments" as a validated invariant.** That is precisely
  the constraint the ruling keeps open, so that a future `skills/<arc>/<subject>` (3 segments) is a
  purely additive change, never a breaking URL/schema migration.
- **DO validate that the first segment is one of `careers` | `skills`**, and that the id resolves to a
  loaded manifest.
- **The one permitted arity assertion is a floor, never a ceiling and never an equality.** The
  `.refine()` may assert that **at least one further non-empty segment follows** the category segment
  — so a bare `"careers"` or `"careers/"` is rejected as malformed — and nothing beyond that. No
  **fixed** total segment count is ever asserted, in either direction: `=== 2`, `=== 3`, `!== 3`,
  `<= 3` and `> 3` are all forbidden; `>= 2` (equivalently `> 1`) is the sole legal depth expression.
  A 4-segment `careers/a/b/c` must validate, and a unit-test fixture proves it (Phase 1.2).
- **Segments are counted after empty tokens are dropped.** `"careers/".split("/")` is
  `["careers", ""]`, so an unfiltered length-2 count would wrongly accept it; the count is therefore
  taken over `pathId.split("/").filter(Boolean)`, making
  `pathId.split("/").filter(Boolean).length >= 2` the concrete form of the floor above. This filter
  constrains **emptiness, not arity** — it removes empty segments and asserts nothing about how many
  non-empty ones there are, so `"skills/conventional-accounting"` (2), `"careers/interview-ready/software-engineer"`
  (3) and `"careers/a/b/c"` (4) all pass the identical expression, while `"careers"` and `"careers/"`
  (both 1 after filtering) are rejected by it. The filter is also invisible to the Phase 1.2 REFACTOR
  depth guard, which flags comparisons against 3 or 4 and equalities against 2 — `filter(Boolean).length >= 2`
  matches neither alternative, so no guard change is needed.
- **`arc` is a required manifest field, independent of the URL grammar (R8).** Every `PathManifest` —
  careers or skills — carries an explicit `arc` string. For `careers/*` paths the arc is also the
  `pathId`'s middle segment (`interview-ready`, `immediately-effective`, or `fundamentally-strong`).
  For `skills/*` paths the arc is **omitted from the URL** (every skills path is currently the
  `immediately-effective` arc — R8 — so naming it in every URL would be noise) but **still present in
  the manifest data**. Conflating "arc" with "a URL segment" is the trap: modelling skills paths as
  arc-less would make a future second skills arc a schema migration **and** a URL migration — exactly
  what R2 forbids. Keeping `arc` a required field regardless of category means only the URL grammar
  would ever need to widen.
- **Unit-test proof of depth-independence** (Phase 1.2, `schemas.test.ts`): a fixture manifest with a
  2-segment `skills/<subject>` `pathId`, one with a 3-segment `careers/<arc>/<role>` `pathId`, **and
  one with a 4-segment `careers/a/b/c` `pathId`** all validate successfully through the same
  `PathManifestSchema`; a fixture whose `pathId` starts with neither `careers/` nor `skills/` is
  rejected; and both bare single-segment fixtures — `"careers"` **and** `"careers/"` — are rejected
  by the same minimum-arity floor, because the count is taken after empty tokens are dropped. No
  fixture asserts a specific segment count.

This plan does not itself validate that a `skills/` manifest exists or resolves to any real content —
the `skills/` category, its manifests, and its corpus are owned end-to-end by **two** sibling plans,
`ayokoding-learning-path-06-skills-accounting` and `ayokoding-learning-path-07-skills-erp` (see
[§Ownership split](#ownership-split-careers-vs-skills--r4)). What this plan guarantees is that
its own schema and resolvers never structurally prevent either plan's manifests from loading.

### Canonical `pathId` form (2026-07-21 ruling — binding on every sibling plan)

**This plan owns the `pathId` definition; this ruling is citable by every plan that writes or reads
one.** It resolves a live discrepancy: plan
`ayokoding-learning-path-01-url-restructure` (and possibly others) used a **2-segment shorthand**
for careers paths (`interview-ready/software-engineer`) instead of the 3-segment canonical form
(`careers/interview-ready/software-engineer`). Ruled as follows.

> **Canonical form.** `pathId` is always the **full path string including its category segment as
> the first `/`-delimited token** — `careers/<arc>/<role>` (3 segments) or `skills/<subject>`
> (2 segments). There is **no separate `category` field**: the category is the first segment of the
> one `pathId` string, never a field carried alongside it.

1. **Full form, not a 2-field split.** `PathManifest` has exactly one identifier field, `pathId`,
   never a `pathId` + `category` pair. Splitting them would let the two drift (a manifest's `category`
   field disagreeing with its own `pathId`'s first segment) for no benefit — a single string is both
   the URL suffix (`/en/c/learn/paths/<pathId>`), the YAML file's nested path
   (`<MANIFESTS><pathId>.yaml`), and the `?path=` query value, so keeping it one string keeps all
   three uses trivially in sync.
2. **A bare 2-segment careers shorthand is never legal — not an alias, not a legacy form. It is
   invalid.** `interview-ready/software-engineer` is **structurally indistinguishable in arity** from
   a 2-segment `skills/<subject>` id (R2's own point: a fixed-arity assumption anywhere is already
   wrong, which is exactly why an arity-only-implied-category shorthand is hazardous). The schema's
   `.refine()` checks the **literal value** of the first segment, never a **fixed** segment count —
   so `interview-ready/software-engineer`'s first segment (`interview-ready`) is neither `careers` nor
   `skills` and `PathManifestSchema.safeParse(...)` **rejects it outright**, exactly like any other
   malformed `pathId`. No code path in this plan special-cases or coerces the 2-segment shorthand.
3. **Resolution of the other form is a hard, typed validation failure — never silent acceptance.**
   `safeParse` returns `success: false`; nothing in this plan's core normalizes, upgrades, or aliases
   a category-less careers id into its 3-segment canonical form. Silent acceptance is exactly the
   failure mode this ruling forecloses: it would let two spellings of the same path coexist and
   diverge without anything failing (per the concern that prompted this ruling). Any plan whose
   content still writes the 2-segment shorthand for a careers path is citing an **invalid** `pathId`
   and must update to the 3-segment canonical form — that conformance sweep is **not** this plan's to
   run (see the escalation-response note below). **Status, re-measured 2026-07-23 — scoped to the
   sibling plans' own documents**: no sibling folder writes a bare 2-segment careers `pathId` as its
   current canonical spelling, but the shorthand string still appears **59 times across five of the
   six** sibling `ayokoding-learning-path-*` folders' top-level
   `README`/`brd`/`prd`/`tech-docs`/`delivery` documents, in three categories (45 + 7 + 7 = 59)
   [Repo-grounded — measured 2026-07-23, self-verifying pinned command, counts **matches, not
   lines**, run from the repo root:
   `python3 -c "import re; p = re.compile(r'(?<!careers/)(interview-ready|immediately-effective|fundamentally-strong)/[a-zA-Z-]+'); r = 'immediately-effective/software-engineer-to-ai-engineer'; [print(plan, sum(len(p.findall(open(f'plans/backlog/ayokoding-learning-path-{plan}/{f}').read())) for f in ['README.md','brd.md','prd.md','tech-docs.md','delivery.md']), sum(open(f'plans/backlog/ayokoding-learning-path-{plan}/{f}').read().count(r) for f in ['README.md','brd.md','prd.md','tech-docs.md','delivery.md'])) for plan in ['01-url-restructure','03-navigation-ui','04-course-authoring','05-manifests','06-skills-accounting','07-skills-erp']]"`.
   Per-plan (total, retired-id-hits): 01→(39,1), 03→(8,1), 04→(4,0), 05→(6,5), 06→(2,0), 07→(0,0);
   summed totals 39+8+4+6+2+0=**59**. Category 2 (retired id) is every retired-id hit in any plan:
   1+1+0+5+0+0=**7**. Category 1 (legacy-dir/elided-ancestor) is every non-retired-id hit in plans
   01/04/05/06: (39−1)+(4−0)+(6−5)+(2−0)=38+4+1+2=**45**. Category 3 (genuine unprefixed `pathId`) is
   every non-retired-id hit in plan 03 alone: 8−1=**7**. 45+7+7=59, matching the independently-summed
   per-plan total exactly — re-run the command verbatim to reproduce every figure in this paragraph].
   First, references to legacy or elided-ancestor **filesystem/directory path fragments, not `pathId`
   values** — most are the legacy **content directory and legacy URL**
   `.../learn/fundamentally-strong/software-engineer/` (plan 01's `<SE_OLD>` constant); one is the
   ASCII directory-tree diagram's elided-`careers/`-ancestor comment
   `.../interview-ready/software-engineer/ _index.md is plan 05's, NOT this plan's`, describing the
   **new** target directory structure with its `careers/` ancestor elided by the tree's `...`
   continuation marker rather than omitted as a genuine unprefixed shorthand — both correct as
   written: these account for **38** of `…-01-url-restructure`'s 39 total shorthand hits (37
   legacy-directory references + 1 elided-ancestor tree-diagram reference; the 39th is the retired-id
   hit counted in the second category below), **4** in `…-04-course-authoring`, **2** in
   `…-06-skills-accounting`, and **1** in `…-05-manifests` (that plan's own `<SE_OLD>` constant
   definition — the same shape as the other three plans' references, previously left out of every
   category and out of the sum) — **45** total. Second, historical notes recording the fourth path's
   **retired** id
   `immediately-effective/software-engineer-to-ai-engineer` — **5** of `…-05-manifests`'s 6 hits, plus
   one in plan 01's `README`, plus one in plan 03's `README` (its `DL-7` bullet) — **7** total. Third,
   **7 genuine unprefixed `pathId`s in `…-03-navigation-ui`** — **7** total — inside its
   verbatim-reproduced build-order text: 3 in the **Build order (inherited)** section (1 in that
   section's stale-flag intro sentence, plus 2 in its `DD-27` bullet) and 2 in the `DL-7` bullet under
   the **Decisions Locked (inherited)** section (both in `README.md`), plus 2 in the `DD-27` bullet
   under the **Inherited verbatim (build order — no single plan owns it)** section in `tech-docs.md`.
   Line numbers are
   deliberately not cited here — plans 03, 04, and 05 are all under active concurrent edit in this
   same gate, and this exact
   citation already drifted once from raw line numbers alone; the section-heading and decision-ID
   references above stay stable across further edits to those files (re-derive a line pointer with
   `grep -n` against the named section if one is ever needed). That plan's own `README` already
   discloses this population as "Stale relative to the 2026-07-21 category-split ruling — flagged, not
   silently corrected here" inside a verbatim-quoted, sibling-owned block.
   `…-07-skills-erp` has none. An earlier revision of this sentence claimed "all six sibling
   folders now write the 3-segment form" with "four remaining 2-segment hits" confined to plan 01;
   a direct count falsifies it in both dimensions — the residual population is 59 occurrences, not 4,
   and it spans five folders, not one. **That sweep did not, and was never intended to, cover this
   plan's
   own custodied course corpus.** Every entry in `syllabus/courses/` writes the bare 2-segment
   shorthand and **none writes the `careers/` 3-segment form** — **388 such lines across all 122
   entries**: 374 across the 120 course spec files, 10 in `README.md` (its per-course template plus
   its worked examples), and **4 in `surgery.md`**, in that file's four-manifest table. The
   per-course distribution is **not** uniform: 105 of the 120 course files carry exactly three, one
   per arc, while 2 carry one, 3 carry two, 6 carry four, 3 carry six, and 1 carries nine
   [Repo-grounded — measured 2026-07-22 with the shell's `grep` shim bypassed via `command grep`. The
   population sweep is `command grep -cE '(interview-ready|immediately-effective|fundamentally-strong)/[a-z]' *.md`
   run from `syllabus/courses/`: `-l` returned 122 and the summed `-c` returned 388. The companion
   sweep `command grep -cE 'careers/(interview-ready|immediately-effective|fundamentally-strong)/' *.md`,
   same directory, returned **0** for every file; its control probe —
   `command grep -cE 'careers/(interview-ready|immediately-effective|fundamentally-strong)/' README.md paths/README.md`
   run from `syllabus/` — returned **8** and **12**, so that zero is a real zero rather than a
   non-matching pattern. Both counts are **matching lines, not occurrences**; reconstructing the
   pattern loosely (for example allowing intervening characters, which catches Mermaid `<br/>`-split
   node labels) yields different figures and will not reproduce these]. An
   earlier revision of this sentence read "371 such lines across 121 files" and asserted `surgery.md`
   "has none"; both figures were wrong, and `surgery.md` in fact carries four. That population is
   **knowingly out of scope**, not
   overlooked: custody rule 1a deliberately limited its mechanical `careers/`-prefix correction to
   `syllabus/README.md`, `syllabus/paths/README.md` and the four manifest mirrors, and its own
   falsifiability clause is explicitly bounded to "those two files", because custody rule 1 forbids
   content edits to the frozen corpus outside the single R3 exception. So: **the escalation is closed
   for the sibling plans' documents and for the manifest-bearing files; it remains deliberately
   unapplied to the course corpus's prose cross-references.** An earlier revision of this line ended
   "nothing is outstanding" without that qualification, which read as a completed corpus-wide
   fact-check and was wrong.

**Filename convention for `syllabus/paths/manifest-*.md` mirrors.** These filenames do **not** encode
the category today (`manifest-interview-ready-software-engineer.md`,
`manifest-immediately-effective-ai-engineer.md` — arc + role, dash-joined, no `careers` marker),
per the flat dash-joined convention this plan's four mirrors already shipped under. Ruling: **the four
existing careers mirror filenames are not renamed** — no collision risk exists today (the careers
vocabulary — three arcs, two roles — shares no token with any skills subject), and renaming
already-settled filenames is pure churn with no correctness benefit. **Going forward, a skills
manifest mirror filename MUST carry an explicit `skills-` marker** — `manifest-skills-<subject>.md`
(e.g. `manifest-skills-conventional-accounting.md`, `manifest-skills-sharia-erp.md`, per the four
subjects amendment A10 introduced) — keeping
the same flat dash-joined shape (no literal slash in the filename) but making the category
unambiguous in the filename itself, by design rather than by vocabulary coincidence. This asymmetry
(careers unmarked, skills marked) is deliberate: the careers filenames are locked, shipped-adjacent
history; the skills filenames do not exist yet, so there is zero cost to making them collision-proof
from the start. This is **this plan's ruling for its own `syllabus/paths/` mirrors and the pattern it
recommends**; it does not itself create or rename any skills-owning plan's files (owned end-to-end by
the skills plans, R4) — those plans decide their own mirror location, and are pointed at this ruling
for the naming pattern to apply if their own folder uses an equivalent mirror concept.

**Escalation-response note.** This ruling is recorded here so it is citable; it does not itself edit
`ayokoding-learning-path-01-url-restructure` or any other sibling plan folder — those stay out of
scope for this plan-fixer pass (folder-scope restriction) and are conformed by whoever runs the
cross-plan sweep.

### The `PathManifest` zod schema

The schema is written in `<FEAT>core/schemas.ts` using **zod 4.3.6** [Repo-grounded —
`apps/ayokoding-www/package.json` declares `"zod": "4.3.6"`], the version already on the app's
dependency list. Shape:

- `pathId` — string, the slash-form path ID. Validated (via `.refine()`) to start with `careers/` or
  `skills/` **and** to carry at least one further segment; **never** validated by a fixed segment
  count, and never bounded above (R2).
- `arc` — string, **required** on every manifest regardless of category (R8). Not constrained to a
  fixed enum — new arcs (careers or skills) are expected to be added later without a schema change.
- `title` — string, display title.
- `description` — string, landing-page prose.
- `courseOrder` — array whose elements are either a course-ID string or an object carrying `id` and
  an optional `framing` object with optional `intro` and `outro` strings.

The schema is the **only** definition of a valid manifest. `manifest-repository.ts` (built by
`ayokoding-learning-path-03-navigation-ui`) parses each YAML file through it; a manifest that does
not validate is not loaded.

## Manifest integrity invariants (verified as gates + unit tests)

- Every `courseOrder` ID resolves to an existing course under `courses/<course-id>/` (no dangling ref).
- No course ID appears twice within one manifest.
- **Prerequisite-consistency**: for every course in a manifest, all of its declared `prerequisites`
  that are **also present in that manifest** appear **before** it. **Scope is ordering-only, not
  completeness**: a declared prerequisite that is simply **absent** from the manifest is not a
  violation and is never reported — see [§Link-don't-walk: prerequisite omission is
  permitted](#link-dont-walk-prerequisite-omission-is-permitted-oi-4-ruling-2026-07-21) for the
  binding ruling and the reasoning.
- No course body is duplicated per path (all manifests reference courses **by ID**, never copy a
  body) — a "no forked body" check.
- Course IDs are stable slugs; a re-home changes a body's URL (with a redirect) but never its ID.

This plan implements the first three as pure functions. The fourth and fifth are properties of the
authoring and manifest plans, enforced there.

### Manifest validation lifecycle

```mermaid
%% The states a manifest passes through, and which check gates each transition.
%% No colour classes are used — every node and edge is distinguished by its label text,
%% so the diagram reads identically in monochrome and to a screen reader.
flowchart TD
    AUTHORED["Authored<br/>YAML data file exists"]
    SCHEMAVALID["Schema-valid<br/>PathManifest parsed"]
    INTEGRITY["Integrity-checked<br/>no dangling, no dup"]
    PUBLISHED["Published<br/>path is walkable"]
    FAILED["Rejected<br/>fix and re-run"]

    AUTHORED -->|"schemas.ts parse — THIS PLAN"| SCHEMAVALID
    AUTHORED -->|"parse fails: not loaded"| FAILED
    SCHEMAVALID -->|"checkManifestIntegrity — THIS PLAN"| INTEGRITY
    SCHEMAVALID -->|"dangling or duplicated entry"| FAILED
    INTEGRITY -->|"checkPrerequisiteConsistency — THIS PLAN"| PUBLISHED
    INTEGRITY -->|"a course precedes its prerequisite"| FAILED
    FAILED -->|"correct the data file"| AUTHORED
```

**Accessibility note.** This diagram uses no colour classes at all; every node and edge is
distinguished by label text alone.

Three of the four transitions above are gated by a function **this plan** ships. This plan ships no
manifest to run them against — `ayokoding-learning-path-05-manifests` does. The `Published` state is
reached only once `ayokoding-learning-path-03-navigation-ui` has a renderer for it.

### Path-context resolution — the decision branch

```mermaid
%% Decision branches inside parsePathContext and resolvePathNav. Each outcome is labelled,
%% and the two terminal renderings are distinguished by node shape as well as colour.
flowchart TD
    IN["searchParams.path"]:::input
    Q1{"param present?"}:::decision
    Q2{"names a loaded<br/>manifest?"}:::decision
    Q3{"course present in<br/>that courseOrder?"}:::decision
    PATHAWARE(["path-aware view:<br/>manifest prev/next<br/>+ path breadcrumb"]):::pathaware
    CANON{{"canonical view:<br/>weight-based nav<br/>+ content-tree breadcrumb"}}:::canonical

    IN --> Q1
    Q1 -->|"no — absent"| CANON
    Q1 -->|"yes"| Q2
    Q2 -->|"no — unknown or renamed path id"| CANON
    Q2 -->|"yes"| Q3
    Q3 -->|"no — course omitted from this path"| CANON
    Q3 -->|"yes"| PATHAWARE

    classDef input fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef decision fill:#DE8F05,stroke:#000000,color:#000000
    classDef pathaware fill:#029E73,stroke:#000000,color:#FFFFFF
    classDef canonical fill:#CC78BC,stroke:#000000,color:#000000
```

**Accessibility note.** Every branch carries an explicit edge label naming the condition that
selected it, and the two terminal outcomes differ by node shape (stadium versus hexagon) as well as
by colour. Fills use the verified accessible palette with black borders and WCAG-AA-contrasting text.

**Three of the four branches end in the canonical view.** That is deliberate — graceful fallback is a
first-class behaviour of the core, not an error path bolted on by the renderer.

## Link-don't-walk: prerequisite omission is permitted (OI-4 ruling, 2026-07-21)

**This section resolves a real contradiction** between this file's own prose and its own
implementation spec, surfaced by `ayokoding-learning-path-06-skills-accounting` as **OI-4** and
correctly routed here rather than fixed in that plan's folder. The prose formerly read: _"A path may
omit a prerequisite only if it also omits every course that needs it — enforced as a gate."_ That
sentence was **false as a description of `checkPrerequisiteConsistency`** — the function has never
enforced it, and its own TDD spec ([delivery.md §2.6](./delivery.md#26-tdd-cycle-6--checkprerequisiteconsistency-prerequisitests))
explicitly asserts the opposite: _"a prerequisite that is declared but omitted from the manifest is
not reported."_ Two documents inside the same plan disagreed; this section is the single ruling.

### 1. Direction and disposition

Two directions exist, and only one is at issue:

- **Direction A — a path includes a course but omits (links out to) its declared prerequisite.**
  **Permitted.** This is the pattern in question.
- **Direction B — a path includes both a course and its prerequisite.** Always legal and the common
  case; nothing here restricts it, and ordering between the two is still enforced (below).

**Ruling: Direction A is PERMITTED, not required, and not forbidden.** Grounded independently of any
single path's history:

1. **Curation already implies partial coverage (DL-2).** A path is defined as _"a curated subset of
   course IDs... freely omits courses that do not fit."_ A rule that forbade omitting a course's
   prerequisite while keeping the course itself would make ordinary curation nearly impossible — the
   overwhelming majority of non-trivial courses in a 121+-course library have _some_ declared
   prerequisite, so "keep the course, must therefore keep (or exclude) whole prerequisite chains"
   would collapse the curated-subset model DL-2 already establishes as this plan's foundational
   design.
2. **Manifest completeness is an editorial property, not a machine-checkable one — this plan already
   draws that line elsewhere.** [§Smoothness Architecture](#smoothness-architecture-per-path) already
   states that difficulty monotonicity, skip affordances, and the refresh register are editorial
   properties audited by a human, with prerequisite-**ordering** singled out as _"the one
   machine-checkable component."_ Whether an omitted prerequisite is _appropriate for this path's
   audience_ requires knowing who the path is for — information a pure function over a DAG and a
   `courseOrder` array does not and structurally cannot have. Extending the ruling to prerequisite
   **completeness** would contradict this plan's own already-drawn boundary between what a pure
   resolver can prove and what only an author/reviewer can judge.

### 2. Does the implementation match? (it already does — the prose was wrong)

**Yes, exactly.** `checkPrerequisiteConsistency`'s scope, as specified in
[delivery.md §2.6](./delivery.md#26-tdd-cycle-6--checkprerequisiteconsistency-prerequisitests), is
**ordering-only**: for each course in `courseOrder`, report every declared prerequisite that is
**both** in the library **and** in the same manifest but appears at a later index. A prerequisite
that is declared but **absent** from the manifest entirely produces no report — not because of a bug,
but because the function's RED spec contains an explicit assertion that this case must **not** be
reported. **The prose changed to match the implementation, not the reverse** — the implementation was
already correct and required no code change (none has been written yet; this plan has not started
Phase 0).

### 3. Distinguishing a legitimate linked prerequisite from a genuinely forgotten one

This is the genuinely hard question, and the honest answer has two parts.

**Part A — `checkPrerequisiteConsistency` cannot and should not try.** As established in §1.2 above,
"was this omission intentional" requires audience context the function never receives. Any attempt to
infer intent from the DAG alone (e.g., "flag it if the omitted prerequisite has many dependents" or
"flag it if it's a _direct_ rather than _transitive_ prerequisite") would be a heuristic standing in
for a judgment call, producing exactly the false-positive/false-negative churn this plan's own
[Anti-Hallucination](../../../repo-governance/development/quality/plan-anti-hallucination.md)
discipline warns against for machine-generated claims. **The check's silence in this direction is by
design, not a hole to be closed by more cleverness inside the function.**

**Part B — the actual distinguishing signal lives one layer up, in documentation, and this plan adds
one small, additive, non-breaking mechanism to make it checkable by a human reviewer without becoming
a hard gate.** A **legitimate** linked prerequisite is one the manifest's own human-readable mirror
(`syllabus/paths/manifest-*.md` for this plan's careers manifests; the equivalent mirror concept for
any other plan's manifests) **names explicitly** — e.g. a stated "Linked prerequisites (not included
in this path): `<course-id>`, ... — because `<reason>`" note. A **genuinely forgotten** prerequisite
has no such note anywhere. This is a **documentation-level, human-reviewable** distinction — the same
class of guarantee this plan already relies on for smoothness — not a schema field and not a new
required input, so it creates **zero new authoring burden** on any manifest-owning plan, including
the two that already conformed to this plan's other rulings.

**The additive mechanism**: `checkPrerequisiteConsistency`'s REFACTOR step
([delivery.md §2.6](./delivery.md#26-tdd-cycle-6--checkprerequisiteconsistency-prerequisitests)) now
also returns a second, purely **informational** list —
`linkedPrerequisites: { courseId, missingPrerequisiteId }[]` — enumerating every declared-but-absent
prerequisite the function already has enough data to compute (it is a read of the same
`prerequisitesByCourse` + `courseOrder` inputs the ordering check already uses; **no new manifest
field, no new required input, and no change to pass/fail semantics** — a manifest is never rejected
for anything on this list). A reviewer (or a future documentation-linting step, out of this plan's
scope to build) can then mechanically diff this list against the manifest's own "linked, not
included" prose: every ID present in `linkedPrerequisites` but **not named** in that prose is the
concrete, checkable signal of a plausibly-forgotten prerequisite — turning "look identical to the
checker" into "look identical to the checker, but not to a reviewer holding both artefacts side by
side." This is diagnostic tooling, not a gate; the manifest still validates either way.

## Downstream consumption

```mermaid
%% Sequence of how a downstream plan consumes this plan's output, and where each hand-off gates.
sequenceDiagram
    autonumber
    participant P2 as schema-and-prerequisite-dag (this plan)
    participant Main as origin/main
    participant P3 as navigation-ui (Wave 2)
    participant P4 as course-authoring (Wave 2)
    participant P5 as manifests (Wave 3)

    P2->>Main: merge core/ six pure modules incl. schemas.ts + MANIFESTS dir
    P2->>Main: merge course-paths Gherkin (RED, no step bindings)
    Note over Main: handoff signal — schemas.ts exists AND typecheck exits 0
    Main->>P3: import resolvePathNav, parsePathContext, resolvePrerequisites
    Main->>P3: manifest-repository globs MANIFESTS for *.yaml
    Main->>P4: syllabus/courses/<id>.md as authoring source of truth
    Main->>P4: prerequisites frontmatter contract for every new _index.md
    P3->>P5: path-landing, path-card, manifest-repository, ?path wiring
    P4->>P5: 90 authored course bodies
    P5->>P5: transcribe courseOrder from syllabus/paths mirrors
    P5->>P5: run checkManifestIntegrity + checkPrerequisiteConsistency at every gate
```

## Programme decisions

Folded in from the retired shared programme file (2026-07-22) so this plan is
**self-contained** and no longer depends on a shared cross-plan file. This plan sits at **Wave 1** —
it has **no prerequisite** and runs in parallel with `ayokoding-learning-path-01-url-restructure`.
Only the `R*`/`A*` decision ids this plan cites are reproduced below, **verbatim** from the programme
decision table; the `A8` and `A12` prose expansions follow because this plan cites both. These are
**programme-scope decisions, not governance rule ids** — nothing under `repo-governance/` defines
them.

`A*` amendments are **later than** the `R*` rules and **win on conflict**.

| Id  | Decision                                                                                                                                                                                     |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R0  | Remove the `/c/` content namespace by **inverting** `contentNamespaceRedirects` — supplementing it would 308-loop                                                                            |
| R1  | URL grammar is `/en/learn/paths/{careers,skills}/…` over six paths (raised to **eight** by `A10`)                                                                                            |
| R2  | `pathId` is **variable-depth by design** — `careers/<arc>/<role>` is 3 segments, `skills/<subject>` is 2; nothing may key on segment count                                                   |
| R3  | The fourth careers path targets a distinct AI-engineering endpoint (superseded in part by `A1`)                                                                                              |
| R4  | Ownership split: plans 01-05 are `careers/`-only; the `skills/` category is separate (revised by `A2`)                                                                                       |
| R5  | The full skills corpus is authored **in this programme**, not deferred                                                                                                                       |
| R7  | **Every URL segment must render** — no orphan segments                                                                                                                                       |
| R8  | Every `skills/` path uses the **immediately-effective** arc, always                                                                                                                          |
| R9  | Every plan declares its **UI-gate and API-gate posture explicitly**; a plan bearing neither surface is _not_ thereby exempt and must state why                                               |
| A2  | The skills category splits into **two** plans — 06 (accounting) and 07 (ERP), the latter `blockedBy` the former                                                                              |
| A3  | Plan 01 owns **every structural `_index.md`** under `paths/`; plans 05-07 own only their path landings, manifests and corpora                                                                |
| A4  | Research verification status is carried forward verbatim — an `[Unverified]` claim must never be restated as fact                                                                            |
| A8  | **Strict clean-room licensing, programme-wide** — binds all seven plans, not only 06-07; nothing copyrighted is reproduced, and every concept is restated in original words with a citation  |
| A10 | The skills category carries **four** paths — `conventional-accounting`, `sharia-accounting`, `conventional-erp`, `sharia-erp`; each Sharia path covers the basics too, and `A11` governs how |
| A12 | Every syllabus is **independently authored, then externally confirmed** — a published curriculum may corroborate coverage but must never supply the structure being written                  |

### A8 — licensing binds the whole programme

`A8` originally read as a plan-06/07 concern because the standards bodies are most visibly
restrictive there. That scoping was wrong: **every plan in the programme authors teaching material,
and teaching material is where copyright exposure concentrates.** The careers corpus carries its own
distinct hazards, and they are easy to miss precisely because programming content feels free:

- **Code examples** copied from documentation, tutorials, blog posts or Stack Overflow. Stack
  Overflow contributions are CC-BY-SA — attribution _and_ share-alike, which is a licence most course
  material cannot satisfy. Author examples originally.
- **Documentation prose** from a framework's official docs. Being free to read is not permission to
  reproduce; most project docs carry their own licence, and it is frequently copyleft.
- **Figures, diagrams and screenshots** lifted from vendor or project sites.
- **Book and course structure.** Reproducing a well-known book's chapter progression, or a paid
  course's module sequence, is the same derivative-work risk as `A12` addresses for syllabi.
- **Trademarks.** Language, framework and vendor names may be used nominatively but never in a course
  title, path segment, or anything that implies endorsement or affiliation.
- **Datasets and sample data** — author them; do not lift a dataset whose licence is unexamined.

The `A8` posture is therefore uniform across all seven plans: **describe, cite and link; never
reproduce.** Where a reader needs the source text, send them to the source.

### A12 — how a syllabus may and may not be confirmed

`A12` exists because the confirmation step introduces the exact risk the rest of `A8` guards against.
Published curricula — ACCA, CPA, CIMA, ASCM/APICS CPIM and CSCP, university course catalogues — are
**copyrighted works**, and several are commercial products whose syllabus _is_ the product. Checking
a syllabus against one is legitimate; deriving a syllabus from one is not.

The order of operations is what keeps this clean, and it is not optional:

1. Author the syllabus from domain reasoning and the plan's own research grounding.
2. **Then** research externally to ask whether the coverage is right — what a practitioner would
   expect that a draft omits, and what it includes that the field does not recognise.
3. Treat the answer as **evidence about coverage**, never as a structure to adopt. A finding is
   actionable as "this topic is missing"; it is never actionable as "reorder to match theirs."

Confirmation must never reproduce a curriculum's text, its module titles, or its sequence. Naming a
body as corroboration ("the topic appears in ASCM's CPIM outline") is nominative use and is fine;
transcribing its outline is not.

## Design Decisions

Five decisions are this plan's own, reproduced **verbatim** from the source plan with their
amendment annotations intact.

- **DD-1 · Order lives in the manifest, not the body.** Reading order is a per-path property carried by
  `courseOrder`, not by a global `weight`. One body cannot encode four orders; moving order to the
  manifest is what enables the shared library. The body keeps a `weight` only for the canonical
  (no-path) sidebar/prev-next fallback and the catalog sort.
- **DD-3 · Path-aware nav via `?path=` client context, not per-path URLs.** A course has exactly one
  URL; the active path rides in a query param. One canonical URL (no duplicate content / SEO split),
  shareable, with a clean fallback when the param is absent.
- **DD-6 · Every course declares `prerequisites` → a prerequisite DAG.** The union of all
  `prerequisites` edges is the library DAG; each manifest must be a valid topological ordering of it
  (a machine-checkable gate); the course page surfaces its prerequisites. The four paths are four
  entry points into the one DAG (amended 2026-07-20 — was three; see DD-22, DD-24). This is the
  structural guarantee that replaces ad-hoc "does this order read smoothly?" judgement with a
  checkable invariant.
- **DD-9 · Functional-core/imperative-shell for the nav feature.** Pure `resolvePathNav` /
  `parsePathContext` / `resolvePrerequisites` in `core/`; IO manifest loading + React in `shell/`.
  Matches the repo standard and makes the ordering/prereq logic unit-testable without IO.
- **DD-16 · Prerequisite-consistency is the audited smoothness property.** Each manifest is a verified
  topological ordering (DD-6); the old ad-hoc SF-1/SF-2 in-body forward-references are **eliminated** by
  making `just-enough-c` a prerequisite of `computer-architecture` and the language primers
  prerequisites of `building-production-cli-tools` (no course now precedes its own prereqs in any path).
- **R2 / R8 · Variable-depth `pathId` with a required `arc` field (2026-07-21 ruling; cited by R-number,
  not `DD-NN`, to avoid colliding with the numbering-gap tokens documented below).** `pathId` is
  `careers/<arc>/<role>` (3 segments) or `skills/<subject>` (2 segments); the schema validates the
  first segment (`careers` | `skills`) plus a **minimum** of one further segment, never a **fixed**
  segment count and never an upper bound, so a future
  `skills/<arc>/<subject>` is purely additive. `arc` is a required `PathManifest` field independent of
  the URL grammar — present even where the URL omits it (every `skills/*` path, always the
  `immediately-effective` arc per R8). See
  [§Variable-depth `pathId`](#variable-depth-pathid-careers-vs-skills--r2-r8).

**Referenced but not owned here.** DD-2 (one canonical body + URL, re-home with redirects) and DD-40
(three structural buckets) are owned by `ayokoding-learning-path-01-url-restructure`; DD-4 (graceful
canonical fallback) is owned by `ayokoding-learning-path-03-navigation-ui`; DD-15 and DD-27 (build
order) are cross-cutting and reproduced in this plan's `README.md`.

**A pre-existing `DD-15` numbering collision (found while reconciling A8, not fixed here).** **Nine**
of the 120 `syllabus/courses/*.md` spec files this plan custodies reference an inherited `DD-15`
marker — two of them spelling it out as `License-aware` / `License-awareness (DD-15)` — a reference
to the **original**
[`fundamentally-strong-software-engineer`](../../done/2026-07-19__fundamentally-strong-software-engineer/tech-docs.md)
closed plan's own `DD-15` ("License-aware technology choices": pick the free/teachable tool when a
well-known library's licence shifts, e.g. Redis SSPL→AGPL, Akka→BSL + the Apache Pekko fork). That is
a **different, narrower** decision from this plan's own `DD-15` above (build order) — the two plan
lineages independently minted a `DD-15` and the per-course files were never renumbered when the
content moved through `shared-course-library-and-learning-paths` into this plan. Both are true
simultaneously and neither is wrong in its own file; this note exists so a reader hitting both does not
assume one supersedes the other.
[Repo-grounded — measured 2026-07-22 by per-file loop over `syllabus/courses/`: `DD-15` appears in
**9** files, `License-aware` in **2**. An earlier revision of this paragraph read "The 127
`syllabus/courses/*.md` files … carry an inherited `License-aware (DD-15)` marker in **each** Scope
note", which was wrong twice over — the glob matches 122 entries (120 spec files), not 127, and the
marker is in nine of them rather than all. A mechanical 127→120 correction would have left the
"in each Scope note" half still false, so the sentence was rewritten around the measurement instead.]

**Reconciling with programme
[`A8`](#programme-decisions) (strict clean-room
licensing).** The inherited `DD-15` (technology-choice licensing) and `A8` (authorship/reproduction
licensing) are **complementary, not duplicate**: `DD-15` governs _which tool a course teaches_ when a
licence shift makes one option non-free; `A8` governs _how the course's own content is authored_ —
code examples, documentation prose, figures/screenshots, book/course structure, trademarks, and
datasets must never be reproduced from a source, only described, cited, and linked. `DD-15`'s narrower
scope does not need restating; `A8` is the current, binding, programme-wide rule this corpus's content
(existing and future) must additionally satisfy, and it is cited here rather than duplicated.

### The DD-34 / DD-35 / DD-39 numbering gap is deliberate

Restated **verbatim** from the source plan (`tech-docs.md:1837-1844`), so that no future reader
"closes" the apparent gap and rewrites 275 tokens whose meanings belong to a different, closed plan:

> **The following six decisions (DD-40 through DD-45) were made in the 2026-07-21 learn-section
> scope-extension pass.** They are numbered from **40**, not 34: the tokens `DD-34`, `DD-35`, and
> `DD-39` are already in use **inside this plan's own folder** — they appear throughout
> `syllabus/courses/**` carrying **FS-SE-inherited** meanings (concept enumeration, primary-source
> citation policy, typed-Python policy) rather than this document's numbering
> [Repo-grounded — `grep -rn "DD-3[4-9]" plans/backlog/shared-course-library-and-learning-paths/`
> returns hits only under `syllabus/courses/`]. Starting at 40 keeps every `DD-NN` token in this plan
> folder unambiguous for an execution-grade reader.

Occurrence counts, verified: `DD-34` 113, `DD-35` 113, `DD-39` 49. `DD-36`, `DD-37` and `DD-38` are
unused anywhere. **Never renumber.**

## `syllabus/` folder structure and custody

This plan's `syllabus/` directory carries the human-readable mirror of the library and the four
paths — **128 files**:

- `syllabus/README.md` — overview of the library + the four paths.
- `syllabus/courses/` — **120 per-course spec files** + `README.md` + `surgery.md` (122 directory
  entries). One file per course-id, each stating origin, format, primary language, `prerequisites`,
  and scope. `surgery.md` is the course-surgery plan, **not** a course spec — an earlier revision of
  this line read "121 per-course spec files + `README.md`", which reached the correct 122 total by
  silently counting `surgery.md` as a course. The 120 spec files plus the **7** DD-20 capstones
  embedded in host-topic files are what make the 127-course catalog.
- `syllabus/paths/` — **4 path-manifest mirrors** + `README.md` (5 directory entries):
  `manifest-interview-ready-software-engineer.md`,
  `manifest-immediately-effective-software-engineer.md`,
  `manifest-fundamentally-strong-software-engineer.md`, and — **renamed 2026-07-21, R3 custody
  exception** (was `manifest-immediately-effective-software-engineer-to-ai-engineer.md`) —
  `manifest-immediately-effective-ai-engineer.md`.

These markdown files are documentation mirrors; the machine-consumed source of truth for each path is
the nested `manifests/**/*.yaml` data file in the `course-paths` feature.

### Custody rules (binding)

1. **This plan owns the folder and performs no content edit inside it, with exactly one recorded
   content exception (rule 2).** The corpus's curriculum content — course specs, orderings,
   pedagogical framing — arrived settled and is never re-derived, added to, or removed by this plan,
   **except** the single R3 content exception below. This is distinct from — and does not conflict
   with — the mechanical, non-substantive string corrections in rules 1a and 1b.
   1. **1a — Mechanical `careers/`-prefix correction (not a content exception).** Two plan-fixer
      passes corrected the path-id **strings** already present in `syllabus/README.md`,
      `syllabus/paths/README.md`, and all four manifest mirrors, to carry the `careers/` category
      prefix R1/R2 made canonical. The first pass missed five ids in `syllabus/paths/README.md`
      (four table rows plus one prose bullet); the 2026-07-21 audit caught the gap and the follow-up
      pass closed it. **Verification, falsifiable both ways** — searching those two files for a
      path-id spelling that begins with a bare arc token (`interview-ready/`,
      `immediately-effective/` or `fundamentally-strong/` rather than `careers/`) finds **exactly
      one** occurrence: `syllabus/paths/README.md`'s explicitly-historical
      `immediately-effective/software-engineer-to-ai-engineer` annotation, which correctly records
      the retired name and is deliberately left unprefixed. Any additional occurrence is a
      regression; zero occurrences would mean the historical record was wrongly rewritten. This is a
      **string substitution**, never a curriculum, ordering, or framing decision — the same class of
      change as repointing a link after a rename (rule 5), required because the R1/R2 URL-grammar
      ruling changed every path id's canonical spelling programme-wide (see
      [§Canonical `pathId` form](#canonical-pathid-form-2026-07-21-ruling--binding-on-every-sibling-plan));
      leaving the corpus's own cross-references citing a `pathId` form the schema itself now rejects
      would make the corpus internally broken, not merely stale. It does **not** count against the
      "one content exception" invariant, and no delivery step performs it — like the R3 exception's
      rename, it was applied directly in the plan-authoring passes, before Phase 0.
   2. **1b — Mechanical corrections of two further string classes (not content exceptions).** Rule
      1a's justification is not specific to path-id spellings: it licenses any **string
      substitution** that keeps the corpus's own cross-references consistent with the rulings and
      repo facts they cite, and forbids any curriculum, ordering, or framing decision. Two further
      classes were corrected under it in the 2026-07-22 plan-fixer pass, both because the corpus had
      come to **contradict the very `tech-docs.md` sections it cross-links to**:
      1. **Sibling-plan identifiers.** `syllabus/README.md` and `syllabus/paths/README.md` described
         the `skills/` category as owned by a single **"not-yet-created" "plan 06"**, while the
         section they link to ([§Ownership split](#ownership-split-careers-vs-skills--r4)) names
         **two** existing plans. Both sentences now state the two-plan model and name
         `ayokoding-learning-path-06-skills-accounting` and `ayokoding-learning-path-07-skills-erp`.
         **Verification, falsifiable both ways** — searching `syllabus/` for `not-yet-created` or
         `not yet created` prints nothing and exits 1 (any hit is a regression), while
         `grep -rl "ayokoding-learning-path-06-skills-accounting" syllabus/` names exactly
         `syllabus/README.md` and `syllabus/paths/README.md` (zero files would mean the correction
         was reverted).
      2. **Serving-URL namespace.** Twelve serving-URL claims in `syllabus/README.md`,
         `syllabus/paths/README.md` and the four manifest mirrors asserted the **legacy**
         un-namespaced `/en/learn/…` form. `contentUrl` maps every content-tree slug to
         `/{locale}/c/{slug}` and the legacy form 308-redirects to it (see
         [§Path constants](#path-constants)), so those strings named a URL that answers **308**, not
         **200** — the exact failure mode this plan's Phase 4 sweep is written to catch. All twelve
         now carry `/c/`. **Verification, falsifiable both ways** — searching `syllabus/` for
         `/en/learn/` prints nothing and exits 1, while
         `grep -rn "/en/c/learn/" syllabus/ | wc -l` prints **12** (as of 2026-07-22; the corpus is
         frozen, so this figure is an invariant, not a drifting measurement)
         [Repo-grounded — measured 2026-07-22 three ways that agree: the shim's `grep -rn … | wc -l`,
         the same command with the shim bypassed via `command grep`, and a summed `grep -rc`, all
         **12**; the `/en/learn/` search printed nothing and exited **1**]. **Read the `12` as an
         assertion of a non-zero invariant, never as a zero-check.** Under one of the two grep engines
         this harness may route to, a plain `grep` that matches nothing prints a
         `0 matches for '<pattern>'` line, which `| wc -l` would read as **1** — so this shape can
         distinguish 12 from 11, but cannot distinguish a true 0 from a 1. A zero-assertion here would
         need a summed `grep -rc` instead.

      Both classes were corrected **in full**, never partially: a half-corrected class leaves the
      corpus asserting two different answers to the same question, which is strictly worse than
      uniform staleness. Like 1a, neither counts against the "one content exception" invariant and
      no delivery step performs either.

2. **The R3 custody exception (2026-07-21 ruling).** `careers/immediately-effective/ai-engineer`
   (formerly modelled as a transition path assuming SWE competence, prerequisites linked not included)
   is now a genuine from-scratch path. This is a **content change, not a rename** — the retired
   framing is factually wrong once the ruling lands, so leaving it unedited would mean this plan
   custodies a known-incorrect corpus rather than a frozen-but-correct one. The rename
   (`manifest-immediately-effective-software-engineer-to-ai-engineer.md` →
   `manifest-immediately-effective-ai-engineer.md`) and the top-matter/composition-framing correction
   were performed directly in this pass; the detailed stage-by-stage re-ordering of the newly-included
   prerequisite courses is **pending**, tracked as
   [delivery.md Phase 1.4](./delivery.md#14-syllabus-custody-exception--ai-engineer-path-correction-r3).
   No new course body was authored — every included course is an existing library course (2026-07-21
   clarification to R3); the growth is a manifest-composition change, owned by
   `ayokoding-learning-path-05-manifests` in its eventual YAML transcription, not by
   `ayokoding-learning-path-04-course-authoring`. **The rename's one mechanical corollary**: the
   in-corpus link to the old filename in `syllabus/courses/README.md`'s path list was repointed to
   the new filename in the same pass, for the same reason the Phase 7 archival move repoints its own
   inbound links in the same commit (see [README.md §Archival is gated on downstream
   archival](./README.md#archival-is-gated-on-downstream-archival)) — a rename obligates fixing its
   own inbound references; that is a mechanical corollary of the one recorded exception, not a
   second, independent content exception.
3. **Every sibling plan links into it and never copies it.** A copy forks the source of truth for 120
   course specs and four manifest orderings, so a later spec correction lands in one copy only.
4. **Cross-plan references use the full relative path** —
   `../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/<rest>` while both plans sit
   in the same stage folder. The source plan's `./syllabus/...` form resolves to nothing from any
   other folder.
5. **Archival repoints every inbound link in the same commit as the move.** See
   [delivery.md Phase 7](./delivery.md#phase-7-plan-archival-and-cross-plan-link-repoint).

## Sections that route to sibling plans

The `syllabus/` corpus custodied here carries **28 back-references** into this plan's `tech-docs.md`,
`prd.md` and `README.md`, targeting sections that the five-way split routed to **other** plans. The
corpus is frozen — the only delivery step that edits a file under `syllabus/` is the one recorded R3
custody exception, [delivery.md Phase 1.4](./delivery.md#14-syllabus-custody-exception--ai-engineer-path-correction-r3),
which touches a single manifest mirror and no anchor target — so those anchors are kept resolvable
from **this** side instead, as pointer sections.

Each heading below exists **only** to keep an inbound anchor alive and to name the plan that now owns
that content. None of them duplicates the content itself: duplicating a 200-line catalog or a
four-manifest ordering would fork exactly the source of truth this split exists to keep singular.

The distinct broken targets and their owners:

| Anchor target                                                                  | Owning plan                                       |
| ------------------------------------------------------------------------------ | ------------------------------------------------- |
| `tech-docs.md#course-library-catalog`                                          | `ayokoding-learning-path-04-course-authoring`     |
| `tech-docs.md#path-manifests` (and its four per-path anchors)                  | `ayokoding-learning-path-05-manifests`            |
| `tech-docs.md#path-aware-navigation-ui-ayokoding-www`                          | `ayokoding-learning-path-03-navigation-ui`        |
| `tech-docs.md#smoothness-architecture-per-path`                                | `ayokoding-learning-path-05-manifests`            |
| `tech-docs.md#productive-in-target-codebases-proof-of-transfer-outcome-anchor` | `ayokoding-learning-path-04-course-authoring`     |
| `prd.md#new-course--capstone-specifications`                                   | `ayokoding-learning-path-04-course-authoring`     |
| `README.md#four-paths-one-library-per-role-convergence`                        | this plan's `README.md` (carried as real content) |

### Course Library Catalog

Moved to **`ayokoding-learning-path-04-course-authoring`**. The catalog enumerates the **127-course
careers/software-engineering library** (121 software-engineer-role baseline + 6 net-new AI-engineering
courses, DD-28) — this figure is the careers-only total (R4/R5); the `skills/` category's ERP +
accounting corpus is additional and owned end-to-end by `ayokoding-learning-path-07-skills-erp` and
`ayokoding-learning-path-06-skills-accounting` respectively. The
authoritative per-course detail is [`syllabus/courses/`](./syllabus/courses/README.md), custodied
here.

### Path Manifests

Moved to **`ayokoding-learning-path-05-manifests`**, which owns every **careers** manifest file and
every manifest mutation — **exactly the 4 manifests below**, not 8 (R4, count amended by A10). A
sibling `skills/` category (4 manifests, two per subject, amendment A10) is owned end-to-end by two
other plans; see
[§Ownership split](#ownership-split-careers-vs-skills--r4). The authoritative human-readable orderings
are [`syllabus/paths/`](./syllabus/paths/README.md), custodied here; each YAML manifest's `courseOrder`
is transcribed from its mirror.

#### Path `careers/interview-ready/software-engineer` (interview-first)

Ordering owned by `ayokoding-learning-path-05-manifests`; mirror at
[`syllabus/paths/manifest-interview-ready-software-engineer.md`](./syllabus/paths/manifest-interview-ready-software-engineer.md).

#### Path `careers/immediately-effective/software-engineer` (build-fast-first)

Ordering owned by `ayokoding-learning-path-05-manifests`; mirror at
[`syllabus/paths/manifest-immediately-effective-software-engineer.md`](./syllabus/paths/manifest-immediately-effective-software-engineer.md).

#### Path `careers/fundamentally-strong/software-engineer` (theory-first)

Ordering owned by `ayokoding-learning-path-05-manifests`; mirror at
[`syllabus/paths/manifest-fundamentally-strong-software-engineer.md`](./syllabus/paths/manifest-fundamentally-strong-software-engineer.md).

#### Path `careers/immediately-effective/ai-engineer` (fourth path, corrected 2026-07-21)

Ordering owned by `ayokoding-learning-path-05-manifests`; mirror at
[`syllabus/paths/manifest-immediately-effective-ai-engineer.md`](./syllabus/paths/manifest-immediately-effective-ai-engineer.md).
Added 2026-07-20 as a transition path; **corrected 2026-07-21 (R3)** to a from-scratch path — see
[§Custody rules](#custody-rules-binding), rule 2.

## Ownership split (careers vs. skills — R4)

**Ruling, 2026-07-21; skills-category path count amended 2026-07-21 by A10.** Plans 01-05 (this plan
included) absorb the `careers/` URL category segment and its content; their wave DAG (W1: 01, 02 ·
W2: 03, 04 · W3: 05) is unchanged, and they stay **careers-only**. The `skills/` category carries
**four** paths (amendment A10 — up from the original two) and is owned **end-to-end** by **two**
sibling plans, two subjects each [Repo-grounded — both folders exist under `plans/backlog/`]:

| `skills/` path                   | Owning plan                                    | Scope                                                      |
| -------------------------------- | ---------------------------------------------- | ---------------------------------------------------------- |
| `skills/conventional-accounting` | `ayokoding-learning-path-06-skills-accounting` | Path landing, manifest, and conventional-accounting corpus |
| `skills/sharia-accounting`       | `ayokoding-learning-path-06-skills-accounting` | Path landing, manifest, and sharia-accounting corpus       |
| `skills/conventional-erp`        | `ayokoding-learning-path-07-skills-erp`        | Path landing, manifest, and conventional-ERP corpus        |
| `skills/sharia-erp`              | `ayokoding-learning-path-07-skills-erp`        | Path landing, manifest, and sharia-ERP corpus              |

Neither category's plans touch the other's manifests, corpus, or landing pages, and neither skills
plan touches the other's.

This scopes the manifest-ownership invariant **per path**, not globally: `ayokoding-learning-path-05-manifests`
is the sole owner of the **4 careers manifests** (unchanged from its original "owns every manifest
file" framing, now stated precisely as careers-only); each skills plan is the sole owner of its **two**
skills manifests (amendment A10 — up from one each). None owns another's. Every place in this plan's
docs that states "the manifest owner" or "four manifests" is scoped to careers — see the corrections in
[§Path constants](#path-constants), [§`syllabus/` folder structure](#syllabus-folder-structure-and-custody),
and [§Path Manifests](#path-manifests) above.

This plan's own surface (schema, resolvers, `<MANIFESTS>` directory) is **category-agnostic by
construction** (see [§Variable-depth `pathId`](#variable-depth-pathid-careers-vs-skills--r2-r8)) — it
does not need to know about the skills category's existence to remain correct for it, which is the
point of not hardcoding depth or category-specific assumptions.

### Path-Aware Navigation UI (ayokoding-www)

Moved to **`ayokoding-learning-path-03-navigation-ui`**, which owns the `shell/` half of the
`course-paths` feature, the `?path=` route wiring, the path rail, the path banner, the paths hub, and
the whole UI design funnel. This plan owns only the pure `core/` half those components import — see
[Architecture](#architecture--the-pure-core-this-plan-builds).

### Smoothness Architecture (per-path)

Moved to **`ayokoding-learning-path-05-manifests`**, which runs the per-path smoothness audits. The
one machine-checkable component of smoothness — prerequisite-consistency, DD-16 — is implemented here
as `checkPrerequisiteConsistency`; everything else in the smoothness architecture (difficulty
monotonicity, skip affordances, refresh register) is an editorial property of a manifest and is
audited there.

### Productive in Target Codebases (proof-of-transfer outcome anchor)

Moved to **`ayokoding-learning-path-04-course-authoring`**, which owns the course library and
therefore the outcome claim the library makes. The claim, in one sentence so the pointer is not
empty: the library teaches **durable principles**, and the named target codebases are **evidence
those principles transfer**, never subject matter — no course names any repository as its subject.
This heading exists only to keep the inbound anchor from
[`syllabus/README.md`](./syllabus/README.md) resolvable while the corpus stays frozen; the full
statement lives in the owning plan.

## Orphan-segment / one-pathId-one-page investigation (R7)

**Task, 2026-07-21**: the decision record's R7 asks every plan touching path ids to check whether its
own surface assumes a `pathId` maps to exactly one renderable page — since `/paths/careers/` (category
landing) and `/paths/careers/<arc>/` (arc landing) are now also pages, alongside the existing per-role
path landing (`/paths/careers/<arc>/<role>`). Findings below are reported per the task's own
instruction even though the fix, if any is needed, belongs to a sibling plan.

- **This plan's six core modules never assume 1:1 `pathId` → page.** `parsePathContext` and
  `resolvePathNav` (`path-context.ts`, `path-nav.ts`) treat `pathId` as an **opaque string**, matched
  only against the set of loaded manifests — they resolve "does a manifest with this id exist," never
  "is there exactly one page for this id." `manifest-integrity.ts` operates purely over the manifest
  set, with no page-count assumption. `schemas.ts` validates a `pathId`'s shape and never its
  reachability; `manifest.ts` loads and normalizes manifest records without reference to pages; and
  `prerequisites.ts` works over course ids alone, which are not `pathId`s at all. None of the six
  would need to change if a `pathId` were reachable from more than one page, or from none.
- **`content-url.ts`'s `contentUrl` only ever builds one URL shape**: the canonical course page,
  optionally carrying `?path=<pathId>`. It has no function that constructs or enumerates an
  **arc-landing** (`/paths/careers/<arc>/`) or **category-landing** (`/paths/careers/`,
  `/paths/skills/`) URL — those two page types are entirely outside this plan's surface.
- **Conclusion**: this plan's schema/resolvers are **already category-and-depth-agnostic** (R2) and, as
  of R8, every `PathManifest` carries an explicit `arc` field independent of the URL. That means the
  data downstream breadcrumb/hub components need to derive an arc-landing or category-landing URL
  (arc string, category string) is **already present** in this plan's schema output — no new pure
  function is needed here to support that. Whether a `pathId`-adjacent function to construct those two
  new page-type URLs is actually needed, and where it should live, is **not this plan's call**: per R7's
  own table, `/paths/careers/` and `/paths/careers/<arc>/` are pages owned by
  `ayokoding-learning-path-01-url-restructure` (routing/IA) and rendered by
  `ayokoding-learning-path-03-navigation-ui` (hub/breadcrumbs). This plan does not add a URL-building
  function for them, and this finding is reported to those plans' agents rather than acted on here.

## UI-gate and API-gate posture (R9)

Both postures are declared explicitly. Per the
[api-quality-gate workflow](../../../repo-governance/workflows/api/api-quality-gate.md)'s
§Relationship to Other Gates, a plan bearing neither surface **is not thereby exempt** — exemption
belongs only to a plan with no reachable behavioural delta at all, and it must be stated here.

### UI gate — **exempt**, and here is the reasoning rather than the assertion

`swe-ui-checker` validates component **source** — it globs for `.tsx` files. This plan's entire
`apps/` surface (see [File Impact](#file-impact)) is six pure TypeScript modules under `<FEAT>core/`,
none of which imports React or renders anything, plus one additive optional parameter on an existing
pure function in `content-url.ts`. **Zero `.tsx` files.** A checker run scoped to this plan's diff
would scan zero component files and return zero findings — a vacuous pass, recorded as an exemption
rather than a claimed one. The rendering components that will eventually consume this plan's core
(`path-landing.tsx`, `path-card.tsx`, the `?path=` wiring) are owned and gated by
`ayokoding-learning-path-03-navigation-ui`.

**The exemption is narrow.** It covers `ui-quality-gate` **only**. Manual behavioural verification via
Playwright MCP is **mandatory and performed** —
[delivery.md Phase 4](./delivery.md#phase-4-manual-no-regression-verification-and-rule-15-exemption-record)'s
no-regression sweep, both supported locales (`en`/`id`) at all three breakpoints — because the one
shipped-code change (`contentUrl`'s optional `pathId` parameter and canonical URL shape) touches an
existing, already-rendered surface. The **Rule-15 three-tester retest is already exempted, with its
own stated reason**, in that same phase: this plan ships no new screen or component for the triad to
explore, and the retest obligation belongs to `ayokoding-learning-path-03-navigation-ui`. This posture
reproduces that exemption rather than re-deciding it — the two records must not diverge.

### API gate — **NOT exempt**

This plan has a reachable behavioural delta: **it authors the manifest-integrity and path-resolution
functions themselves.** `checkManifestIntegrity`, `checkPrerequisiteConsistency` (whose OI-4 ruling
adds an additive, non-breaking `linkedPrerequisites` diagnostic output — see
[Link-don't-walk](#link-dont-walk-prerequisite-omission-is-permitted-oi-4-ruling-2026-07-21)),
`parsePathContext`, and `resolvePathNav` are the mechanism by which a malformed manifest fails closed
and by which a `?path=` query decides which navigation view a reader sees. That this plan ships no
manifest data of its own to run them against yet does not make the functions unreachable — every
manifest any Wave-2/3 plan will ever publish is validated by exactly this code, and nothing else in
the programme re-implements it.

**How it is exercised, named explicitly**: each function's own TDD-authored unit suite
(`schemas.test.ts`, `manifest.test.ts`, `path-context.test.ts`, `prerequisites.test.ts`,
`manifest-integrity.test.ts`, `path-nav.test.ts` — one per `core/` module, all six listed in
[File Impact](#file-impact)),
re-run at every phase gate, plus `content-url.test.ts` for the modified `contentUrl()`.

**What cannot run, and why** [Repo-grounded, re-verified 2026-07-21]: `api-quality-gate` requires a
running service and an identified contract (OpenAPI 3.x or GraphQL SDL). `ayokoding-www` publishes
neither; its only API route is the internal tRPC handler. There is also, as yet, no manifest for a
live loop to exercise — `ayokoding-learning-path-05-manifests` publishes the first one. **This plan
therefore does not claim the gate was run and passed.** It records the unit-level substitute instead.

**Rule-16 API exploratory retest — not applicable**, already recorded alongside the Rule-15 exemption
in
[delivery.md Phase 4](./delivery.md#phase-4-manual-no-regression-verification-and-rule-15-exemption-record):
this plan exposes no REST or GraphQL endpoint and adds no HTTP surface.

## UI-design-funnel exemption

**This plan is exempt from the UI-design-funnel requirement**, explicitly and with reasoning rather
than by silent omission.

The funnel binds a plan that adds or changes **user-facing screens or components** under `apps/` or
`libs/`. This plan adds neither. Its entire `apps/` surface is:

- six pure TypeScript modules under `<FEAT>core/`, none of which imports React or renders anything;
- one directory plus a `README.md` under `<MANIFESTS>`;
- one additive optional parameter on an existing pure function in `content-url.ts`.

The design funnel for every screen in the parent architecture — Screens 0 through 3 (landing hero,
paths hub, path landing, course page in path context) — is owned by
`ayokoding-learning-path-03-navigation-ui`; Screen 4 (legacy landing) is owned by
`ayokoding-learning-path-01-url-restructure`. Neither set of artefacts is carried here, and no
archival check in this plan asserts a render exists.

## Specs and Gherkin delivery applicability

**This plan is NOT exempt.** It creates observable behaviour under `apps/` — six pure functions with
externally-observable contracts — so it carries companion Gherkin under `<SPECS>`, authored RED in
Phase 2.

The step bindings that turn that Gherkin green are **not** this plan's: they live in the shell
components and route wiring built by `ayokoding-learning-path-03-navigation-ui`.

**How the deferral is expressed without redding the build — one semantics, everywhere.** Every
scenario this plan authors under `<SPECS>` carries the `@wip` tag. `@wip` is the behavior-coverage
validator's own step-binding-deferral exemption [Repo-grounded —
`apps/rhino-cli/src/application/behavior_coverage/validator.rs`: "`@wip` scenarios are fully exempt",
and `extract.rs` parses the tag], so `npx nx run ayokoding-www:specs:behavior:coverage` **exits 0**
at every gate in this plan, before and after the new domain lands. That matters beyond tidiness:
`test:quick` runs `test:specs`, which runs `specs:behavior:coverage` [Repo-grounded —
`apps/ayokoding-www/project.json`], and `test:quick` is a pre-push hook target — so an untagged
`course-paths` scenario would block **every** push from Phase 2 onward, including the archival push.

The **deferred obligation** is recorded explicitly with its closing plan named, rather than expressed
as a red target: `ayokoding-learning-path-03-navigation-ui` replaces the `@wip` tags with real level
tags (`@unit` / `@e2e`) and adds the matching `@covers` markers when it authors the step bindings.
See the Phase 2 gate in `delivery.md`.

The existing Gherkin domain layout is [Repo-grounded]:
`specs/apps/ayokoding/behavior/ayokoding-www/gherkin/` currently holds `app-shell/`, `content/`,
`i18n/`, `navigation/`, `search/`, `tools/` and a `README.md`. `course-paths/` is a **new sibling
domain folder**.

## File Impact

| Path                                                                           | Change                            | Note                                                                                                                                                                         |
| ------------------------------------------------------------------------------ | --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `apps/ayokoding-www/src/features/course-paths/core/schemas.ts`                 | _New file_                        | `PathManifest` zod schema                                                                                                                                                    |
| `apps/ayokoding-www/src/features/course-paths/core/schemas.test.ts`            | _New test_                        | Six `pathId` / `arc` / `courseOrder` assertion groups; created by [delivery.md cycle 1.2 RED](./delivery.md#12-pathmanifest-zod-schema--tdd-cycle)                           |
| `apps/ayokoding-www/src/features/course-paths/core/manifest.ts`                | _New file_                        | Type + course-ref normalization                                                                                                                                              |
| `apps/ayokoding-www/src/features/course-paths/core/manifest.test.ts`           | _New test_                        | Course-ref normalization; created by [delivery.md cycle 2.1 RED](./delivery.md#21-tdd-cycle-1--course-ref-normalization-manifestts)                                          |
| `apps/ayokoding-www/src/features/course-paths/core/path-nav.ts`                | _New file_                        | `resolvePathNav`                                                                                                                                                             |
| `apps/ayokoding-www/src/features/course-paths/core/path-nav.test.ts`           | _New test_                        | Boundaries + missing course                                                                                                                                                  |
| `apps/ayokoding-www/src/features/course-paths/core/path-context.ts`            | _New file_                        | `parsePathContext`                                                                                                                                                           |
| `apps/ayokoding-www/src/features/course-paths/core/path-context.test.ts`       | _New test_                        | Valid / unknown / absent                                                                                                                                                     |
| `apps/ayokoding-www/src/features/course-paths/core/prerequisites.ts`           | _New file_                        | `resolvePrerequisites`, `checkPrerequisiteConsistency`                                                                                                                       |
| `apps/ayokoding-www/src/features/course-paths/core/prerequisites.test.ts`      | _New test_                        | Declared / missing; consistent + deliberately-violating fixtures                                                                                                             |
| `apps/ayokoding-www/src/features/course-paths/core/manifest-integrity.ts`      | _New file_                        | `checkManifestIntegrity`                                                                                                                                                     |
| `apps/ayokoding-www/src/features/course-paths/core/manifest-integrity.test.ts` | _New test_                        | Unresolved + duplicate ID fixtures                                                                                                                                           |
| `apps/ayokoding-www/src/features/course-paths/manifests/README.md`             | _New file_                        | Directory marker; states which plan writes `.yaml` here                                                                                                                      |
| `apps/ayokoding-www/src/features/content/core/content-url.ts`                  | Modified                          | Optional `pathId` param appending `?path=`; the existing `/{locale}/c/{slug}` shape (`/en/c/learn/courses/<course-id>`) is preserved unchanged [Repo-grounded — file exists] |
| `apps/ayokoding-www/src/features/content/core/content-url.test.ts`             | Modified                          | New `?path=` assertions only; the seven existing assertions stay **unchanged** (the URL shape does not move)                                                                 |
| `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/course-paths/`            | _New dir_                         | Gherkin companion + `README.md`                                                                                                                                              |
| `<PLAN>/syllabus/paths/manifest-immediately-effective-ai-engineer.md`          | Modified (one recorded exception) | R3 custody exception; Stage 0 ordered in [delivery.md Phase 1.4](./delivery.md#14-syllabus-custody-exception--ai-engineer-path-correction-r3)                                |
| `<PLAN>/syllabus/` (all other files)                                           | Unchanged                         | Custodied; **no delivery step edits any other file**                                                                                                                         |

## Dependencies

- **zod 4.3.6** [Repo-grounded — `apps/ayokoding-www/package.json`] — already a dependency of
  `ayokoding-www`. No new package is added by this plan.
- **No YAML parser is needed here.** `<MANIFESTS>` ships empty of `.yaml` files; the parser is
  `manifest-repository.ts`'s concern, in `ayokoding-learning-path-03-navigation-ui`.
- **Nx targets used** [Repo-grounded — `apps/ayokoding-www/project.json`]: `typecheck`, `lint`,
  `test:quick`, `test:unit`, `test:integration`, `test:e2e`, `specs:behavior:coverage`, `build`,
  `dev`.
- **rhino-cli** for `md links validate` and `md heading-hierarchy validate`, invoked as raw
  `cargo run --manifest-path apps/rhino-cli/Cargo.toml` commands, not Nx targets
  [Repo-grounded — `apps/rhino-cli/Cargo.toml` exists].

## Rollback

Every phase in this plan is additive and independently revertable:

- **Phase 1 and Phase 2** create a new feature directory and add one optional parameter to an
  existing function. `git revert` of the phase commits removes the feature wholesale; nothing else
  imports it yet, because the only importers are Wave-2 plans that have not started.
- **The `content-url.ts` edit** is the one change touching shipped code. It is additive (an optional
  parameter, with the `/c/` URL shape preserved) and reversible in isolation; the Phase 4
  no-regression sweep across both locales is what proves it is safe to keep.
- **The `syllabus/` corpus** is modified by exactly one delivery step — Phase 1.4's recorded R3
  custody exception, an in-place edit to
  `syllabus/paths/manifest-immediately-effective-ai-engineer.md`. Reverting that one commit restores
  the mirror; every other file in the corpus is untouched and has nothing to roll back.
- **The archival repoint** touches only markdown links in sibling plan folders. Reverting the
  archival commit restores both the folder location and the links atomically, because they land in
  the same commit.

## Testing and Verification Strategy

Per the repo's three-level testing standard and TDD mandate, every module here is built test-first.

- **Unit** (`test:unit`, pure core) — the entire substance of this plan: `resolvePathNav` (prev/next
  at both boundaries, course missing from the manifest), `parsePathContext` (valid / unknown /
  absent), `resolvePrerequisites` (declared IDs returned; missing course → empty),
  `checkPrerequisiteConsistency` (clean fixture passes; deliberately-violating fixture is reported),
  `checkManifestIntegrity` (clean fixture passes; unresolved-ID and duplicate-ID fixtures are
  reported), `PathManifest` schema validation, and `contentUrl` with `pathId`.
- **Integration** (`test:integration`) and **E2E** (`test:e2e`) — **neither tier is exercised by this
  plan, and neither can be.** Both targets are `echo` no-op stubs for `ayokoding-www`
  [Repo-grounded — `apps/ayokoding-www/project.json`: `test:integration` runs
  `echo 'no-op: integration tier not used for this content app'` and `test:e2e` runs
  `echo 'no-op: target not applicable for this project'`], so they always exit 0 and **prove
  nothing**. They are kept in the affected-target lists for completeness only; no acceptance clause
  in this plan derives evidence from them. The actual regression evidence for the `content-url.ts`
  change is `content-url.test.ts` (unit) plus the Phase 4 Playwright no-regression sweep. That the
  one tier which could catch a cross-page URL regression is a stub here is a real gap in
  `ayokoding-www`'s harness, not something this plan can close — it is raised as a Knowledge-Capture
  candidate in `learnings.md`.
- **`specs/` Gherkin companion** — authored RED under `<SPECS>` with every scenario tagged `@wip`, so
  `specs:behavior:coverage` exits 0 throughout; step bindings (and the `@wip` removal) land in
  `ayokoding-learning-path-03-navigation-ui`.
- **Manual behavioural verification** — a targeted **no-regression sweep**, not a feature walk-through:
  the `content-url.ts` change alters link generation across the site, so Phase 4 opens existing learn
  pages in **both** supported locales (`en` and `id` [Repo-grounded — `SUPPORTED_LOCALES` in
  `apps/ayokoding-www/src/features/i18n/core/config.ts`]) at three breakpoints via Playwright MCP,
  confirms the console is clean and links resolve, and commits screenshot evidence.
- **Rule-15 three-tester retest** — **exemption recorded**, with reasoning, in Phase 4. This plan
  ships no rendered surface, so there is no new UI for `web-exploratory-tester`,
  `web-usability-tester` or `web-design-tester` to explore. The no-regression sweep above is run
  instead, and is not a substitute claim.
- **Rule-16 API exploratory retest** — **not applicable**. This plan exposes no REST or GraphQL
  endpoint and adds no HTTP surface.
