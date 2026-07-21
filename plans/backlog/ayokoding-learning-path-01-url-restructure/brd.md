# Business Requirements — ayokoding-www Learning-Path URL Restructure

## Business Goal

Give the ayokoding-www learn section **one explainable shape**. Today `/{locale}/c/learn/` lists
seven subject domains and nothing that tells a reader what kind of thing each child is. The shared
course library the sibling plans build needs a **flat, path-neutral `courses/` namespace** and a
**`paths/` home** to render into; everything not yet a course or a path needs a home that says so.
This plan delivers exactly that boundary work:

- a **flat `courses/` namespace** holding the 33 shipped topics + 4 existing capstones, re-homed out
  of `fundamentally-strong/software-engineer/` with a **per-course 308 redirect** each, so one course
  has one canonical body at one canonical URL (DD-2);
- a **`paths/` content home** whose 2×2-grid landing has room for all four paths, populated as each
  ships;
- a **`legacy/` bucket** holding the six remaining `en/learn/` domains (**1,148** `.md`
  [Repo-grounded]) as a **prefix relocation, not a rewrite**, behind per-domain 308 prefix rules; and
- the section closed at **exactly three** structural buckets plus its own two hub files (DD-40).

The change is **architecture and URL topology only**. No page body is rewritten, no course is
authored, no manifest is composed, no navigation component is built. Those belong to the four sibling
plans named in [README §Depends-on](./README.md#depends-on).

## Why finish the section instead of half-converting it

The source plan converted **one** of the seven domains under `en/learn/` and left six in place. That
would ship a learn section whose top level mixes two structural buckets (`paths/`, `courses/`) with
six subject domains — an IA that is neither the old one nor the new one, and that cannot be explained
to a reader in a sentence [Judgment call]. Three consequences follow, and each is a business cost:

- **A reader arriving at `/en/c/learn` cannot tell what kind of thing each child is.** "Follow a
  path", "browse the library", and "dig into the older material" are three understandable choices;
  "paths, courses, artificial-intelligence, business, information-security, it-governance,
  personal-development, software-engineering" is a list with no rule behind it.
- **A future author has no rule for where new material belongs.** Every new page becomes a judgment
  call, and judgment calls made one at a time drift.
- **The half-converted state is more expensive to finish later than now.** The relocation is a pure
  `git mv` while the tree is otherwise untouched. Once path landings, manifests, and 90 authored
  course bodies sit on top of it, the same move has to be reasoned about against all of them.

## Why the re-home and the relocation belong in one plan

Both are URL-topology changes over the same section, and they interact in exactly one place that a
split across two plans would get wrong: **`fundamentally-strong/` must be excluded from the
per-domain bucket rules** (DD-43). A `fundamentally-strong` prefix rule in the bucket module would
shadow the per-course rules for all 37 already-built directories and silently send every re-homed
course to a legacy URL holding nothing. That negative assertion can only be written by the plan that
owns **both** rule sets — which is why this plan owns both redirect modules, and why the per-course
redirect table was moved here at split time rather than left with the navigation plan (see
[README §Provenance](./README.md#provenance--where-this-plan-came-from)).

## Business Impact

**Pain points addressed**:

- The learn section would be left **half-converted** — `/en/c/learn/` listing two structural buckets
  beside six subject domains, so a reader cannot tell what kind of thing each child is and a future
  author has no rule for where new material belongs.
- The 33 shipped topics have **no path-neutral home**. While they live under
  `fundamentally-strong/software-engineer/`, the section name is both a library brand and a path ID,
  and the four path manifests the sibling plans compose have nothing to reference by stable course ID.
- **There is no home for material that is neither a course nor a path.** Six domains totalling 1,148
  `.md` currently occupy the section's top level with no statement of their status.
- A reader who bookmarked or search-landed on any of those pages has **no guarantee their URL keeps
  working** through a reorganization of this size.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- **One explainable learn section**: `/{locale}/c/learn/` offers three understandable choices —
  follow a path, browse the course library, dig into the older material — instead of a hybrid
  taxonomy, and every future page has an unambiguous home.
- **A populated, flat, path-neutral course namespace** that the manifest plan can reference by stable
  course ID and the authoring plan can extend without slug collisions.
- **Zero URL breakage across a 1,148-file move plus a 37-directory collapse**, because every old
  address 308s to its new one in both inbound forms.
- **A reviewable change**: the relocation lands as a pure rename diff, so a 1,148-file commit stays
  readable and carries no content risk.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns the three-bucket IA and the `legacy/`-as-staging-pen framing (Q-A).
- **Frontend engineer** — writes both redirect modules, wires `next.config.ts`, authors the bucket
  landing.
- **Content author** — rewrites `en/learn/overview.md` and authors `legacy/_index.md`.
- **Content reviewer** — validates links, headings, and the relocated tree.

Consuming agents: `swe-typescript-dev` (redirect modules + `next.config.ts` wiring), `swe-e2e-dev`
(redirect e2e), `specs-maker` (the `<NAVSPECS>` feature file), and
`apps-ayokoding-www-content-fixer` (the two hub-file rewrites) [Repo-grounded — each has a definition
file under `.claude/agents/`].

## Business-Level Success Metrics

- **The learn section closes at three buckets** (observable):
  `ls apps/ayokoding-www/content/en/learn` lists exactly `_index.md`, `courses`, `legacy`,
  `overview.md`, `paths` — the three structural buckets plus the section's two hub files
  (DD-40/DD-45). Falsifiable in both directions: it lists seven domain directories today, and it would
  list eight or more if a domain were missed.
- **Zero content rewritten in the relocation** (observable): the relocation commit's diff shows every
  one of the 1,148 relocated files as a pure rename (`git diff --cached --summary -M`), with the only
  edited content files being `en/learn/overview.md` and the new `legacy/_index.md` (DD-41).
- **No relocated URL 404s** (observable): every relocated domain's old URL — in both its bare and
  `/c` inbound forms — 308s to its `legacy/` address, and `courses/` and `paths/` URLs are provably
  **not** rewritten; verified by the redirect unit test and e2e (DD-42).
- **No re-homed course URL 404s** (observable): every legacy
  `fundamentally-strong/software-engineer/<slug>` URL 308s to `/en/c/learn/courses/<course-id>` for
  all 37 re-homed bundles, verified by the per-course redirect unit test (DD-43). Falsifiable in both
  directions: the test asserts each of the 37 mappings resolves **and** that no bucket rule matches
  the `fundamentally-strong` prefix.
- **Every re-homed course declares its prerequisites** (observable): all 37 re-homed `_index.md`
  files carry a `prerequisites: [course-id, ...]` frontmatter key (an empty list is valid for roots),
  in the shape owned by `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- **The old-way browse still resolves** (observable): after re-homing, every entry in the legacy
  `fundamentally-strong/**` `_index.md` tree links to live content at its canonical course URL or
  through the redirect layer — no dead links, no orphaned section (DD-19).
- **The `id` locale is provably untouched** (observable):
  `find apps/ayokoding-www/content/id/belajar -name '*.md' | wc -l` still returns **53** and
  `test -e apps/ayokoding-www/content/id/belajar/legacy` returns non-zero (DD-45).
- **No regressions** (observable): `nx run ayokoding-www:build` renders green; `test:unit`,
  `specs:behavior:coverage`, the paired `ayokoding-www-fe-e2e:test:e2e`, heading-hierarchy,
  markdownlint, and link validation all pass across the app and the section.

## Business-Scope Non-Goals

- **Rewriting, re-titling, merging, or re-sequencing any relocated legacy page** — the move preserves
  each domain's sub-taxonomy verbatim (DD-41).
- **Promoting legacy material into real courses** — later work, tracked per
  [Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive); this plan files no
  per-page migration backlog.
- **Extending the three-bucket shape to the `id` locale** — deferred and recorded explicitly (DD-45).
  `id/belajar/` is left untouched — no `legacy/` bucket, no relocation, no `id` redirect rules —
  because `id` has zero courses and zero paths, so two of the three buckets would ship empty.
  Recorded as a decision, not an omission; reversal conditions in
  [Q-B](./tech-docs.md#q-b--does-the-id-locale-get-the-same-three-bucket-shape-now) and
  [Q-C](./tech-docs.md#q-c--if-id-is-in-scope-are-the-bucket-segments-translated).
- **Building the `course-paths` feature** — the pure core belongs to
  `ayokoding-learning-path-02-schema-and-prerequisite-dag` and the rendering layer to
  `ayokoding-learning-path-03-navigation-ui`.
- **Authoring or composing any path manifest** — every file under
  `apps/ayokoding-www/src/features/course-paths/manifests/` belongs to
  `ayokoding-learning-path-05-manifests`. This plan creates the `paths/_index.md` **content home**
  only; it publishes no manifest and populates no path card.
- **Authoring any course body** — including the 61 transferred topics, the net-new courses, and the
  capstones. Those belong to `ayokoding-learning-path-04-course-authoring`.
- **Implementing the Screen 0 landing hero** — the hero funnel and its implementation belong to
  `ayokoding-learning-path-03-navigation-ui`. This plan owns Screen 4 only.

## Business Risks and Mitigations

| Risk                                                                                                       | Mitigation                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Re-homing the 33 shipped topics + 4 capstones to `courses/` breaks ~37 live production URLs.               | Every re-home lands **in the same phase** as its redirect (`apps/ayokoding-www/src/redirects/`), from the legacy `fundamentally-strong/software-engineer/<slug>` URL to `/en/c/learn/courses/<course-id>`, asserted by a unit test over all 37 mappings before the phase gate closes.              |
| Relocating 1,148 pages breaks live URLs at scale.                                                          | Per-domain 308 prefix rules cover every descendant via one `:path*` each (DD-42), asserted by a unit test mirroring `content-namespace.unit.test.ts` and by e2e on both inbound forms; the relocation is a pure `git mv`, so `git revert` restores everything atomically.                          |
| A blanket redirect rule swallows the `courses/` and `paths/` buckets or self-recurses.                     | A blanket `/en/c/learn/:path*` rule is explicitly FORBIDDEN (DD-42); the six domains are enumerated, and the unit test asserts no blanket source and no `courses`/`paths`/`fundamentally-strong` source prefix exists.                                                                             |
| A `fundamentally-strong` bucket rule shadows the 37 per-course rules and strands every re-homed course.    | DD-43 states the exclusion as a boundary rule, and the same unit test that asserts the 12 bucket rules asserts the **absence** of any `fundamentally-strong`-prefixed source. Both rule sets live in this one plan, so the negative assertion is writable.                                         |
| The `next.config.ts` redirect ordering regresses, stranding historical renames or restoring a 3-hop chain. | DD-42 states the required order (`learnReorg` → `learnThreeBucket` → `contentNamespace`) plus e2e coverage of both inbound forms and of the `learn-reorg` → bucket chain (URL-mapping row 9); Phase 4 re-asserts the ordering as a standing regression check.                                      |
| Search traffic to the six relocated domains (~1,148 pages, ~67% of the `en/learn/` corpus) collapses.      | 308s preserve link equity, and [Q-D](./tech-docs.md#q-d--seo-treatment-of-legacy)'s recommended answer keeps the bucket **indexed**; `noindex` is explicitly rejected as the default because the replacement courses do not exist yet (~37 of 127 bodies built).                                   |
| Legacy material and canonical courses cover the same subject, and a reader studies the superseded one.     | Q-D's per-page "superseded by" banner plus recording the supersession in the surviving course's `overview.md` ([Q-A](./tech-docs.md#q-a--is-legacy-a-staging-pen-or-a-permanent-archive)); the bucket is a staging pen expected to shrink, not a permanent parallel library.                       |
| A missing `legacy/_index.md` makes the bucket sort **first** in the sidebar, ahead of `courses/`/`paths/`. | Authoring `legacy/_index.md` with an explicit `weight` is a delivery step and a phase-gate check (DD-44): `generate-indexes` only rewrites `_index.md` files that already exist, and `buildTreeForLocale` would otherwise synthesize a `weight: 0` "Legacy" node.                                  |
| The `id` locale silently diverges from `en`'s IA in a bilingual app.                                       | The deferral is a recorded decision (DD-45) with stated reversal conditions, surfaced in Non-Goals, in the delivery checklist, and in the AFTER content tree — not an unstated omission a later reader would read as a bug, and re-asserted at archival against the Phase-0 `id/belajar` baseline. |
| Feed churn: every relocated item's RSS `<guid>` changes with its URL, re-surfacing ~1,148 items as new.    | Accepted as a one-time cost of the move and called out in the IA-consequence table; no mitigation exists short of not moving the content.                                                                                                                                                          |
| Navigation regresses for readers who never use a path (the relocation is one of two ways the sidebar can). | The IA is entirely tree-derived (DD-44), so the relocation needs zero production code edits; Phase 5 runs a no-path sweep at all three breakpoints. The **other** way — the path rail sharing `ResizableSidebar` — is guarded by `ayokoding-learning-path-03-navigation-ui`, which owns that risk. |
| The 37-slug namespace collides with a natively-authored slug from the sibling authoring plan.              | The wave order is the mitigation: `ayokoding-learning-path-04-course-authoring` starts only after this plan merges, so its collision check runs against a **populated** namespace rather than passing vacuously against an empty one.                                                              |
| The six Open Questions (Q-A…Q-F) are silently resolved by whoever executes first.                          | Every Phase-3 step executes its governing question's **recommended default** and names the alternative inline, so an overturned ruling is a bounded edit rather than a rewrite; Phase 8 asserts all six are recorded as rulings, not left as "RECOMMENDED".                                        |
