# 🏗️ Technical Documentation: Repository Clean-Up

## Deletion Surface

### Applications

`apps/ayokoding-cli/` and `apps/ose-cli/` — two Rust binaries, each `Cargo.toml`, `Cargo.lock`,
`deny.toml`, `project.json`, `README.md`, `src/{cli,lib,main}.rs`, hexagonal `src/{application,
commons,domain,infrastructure}/mod.rs`, `src/commands/links.rs`, and `tests/{cli_smoke,
links_check}.rs`.

### Orphaned library — deleted

`libs/rust-commons/` exists solely to serve these two CLIs. Its only two consumers are
`apps/ayokoding-cli/Cargo.toml:20` and `apps/ose-cli/Cargo.toml:20`; `apps/rhino-cli/Cargo.toml`
contains **zero** references to it. Deleting both CLIs leaves it with no consumer.

| Item                                     | Size                                                         |
| ---------------------------------------- | ------------------------------------------------------------ |
| `libs/rust-commons/src/links/mod.rs`     | 820 lines                                                    |
| `libs/rust-commons/src/lib.rs`           | 8 lines                                                      |
| `libs/rust-commons/tests/check_links.rs` | test harness                                                 |
| `specs/libs/rust-commons/**`             | spec tree incl. `behavior/gherkin/links/check-links.feature` |

Its `project.json` carries a full Nx target set, including a `test:coverage` at `--fail-under-lines
90` and a `deps:audit` message naming all three CLIs. It is deleted with its consumers: an
unconsumed library whose coverage gate still runs on every affected build is exactly the cost this
plan exists to remove.

`libs/fsharp-crane-core` was checked and is **not** orphaned — `apps/crane-cli/crane-cli.fsproj:42`
holds a live `ProjectReference` to it. No other library under `libs/` loses a consumer.

### Empty application shell

`apps/beavernest-app-web/` contains exactly one tracked file, `LICENSE`. Its last content-bearing
commit is `964b6f8b3 feat(beavernest): complete Flutter hosted cutover (#183)`, which replaced the
React frontend with the Flutter `beavernest-app`; the directory was never removed.

It has no `project.json`, so Nx does not see it, and `repo-config.yml` registers
`beavernest-{be,be-e2e,app,app-e2e}` but not it. `infra/dev/beavernest-app/tests/
workflow-contract.sh:9` actively asserts the name is **absent** from the workflow, so the guard
already treats it as retired. Only `plans/ideas/**` index prose and published `apps/ose-www/content`
updates still mention it; the content is historical record and is not touched.

### Spec trees

`specs/apps/ayokoding/behavior/ayokoding-cli/**` and `specs/apps/ose/behavior/ose-cli/**`, plus the
parent README index entries in `specs/apps/{ayokoding,ose}/behavior/README.md`,
`specs/apps/{ayokoding,ose}/README.md`, `specs/apps/*/containers/`, `specs/apps/*/system-context/`,
and `specs/README.md`.

### Nx wiring

- `apps/ose-www/project.json` — the `links:check` target invoking
  `../../apps/ose-cli/dist/ose-cli links check --content content`. Not referenced by
  `ose-www:test:quick`.
- `apps/ayokoding-www/project.json:191` — `"implicitDependencies": ["ayokoding-cli"]`, with no
  target that invokes the binary.

### Registry and config

`repo-config.yml` — three project registry entries and two gate exclusions:

| Line | Entry                                         | Declared `specs:` root                 |
| ---- | --------------------------------------------- | -------------------------------------- |
| 105  | `ose-cli`, levels `[unit, integration]`       | `specs/apps/ose/behavior/cli/**`       |
| 142  | `ayokoding-cli`, levels `[unit, integration]` | `specs/apps/ayokoding/behavior/cli/**` |
| 174  | `rust-commons`, levels `[unit]`               | `specs/libs/rust-commons/behavior/**`  |

Note the first two `specs:` globs name `behavior/cli/**`, but the trees on disk are
`behavior/ose-cli/` and `behavior/ayokoding-cli/`. Those globs have matched nothing since the trees
were named — another instance of the same vacuous-check shape this plan is removing. Plus the
`md-links` exclusions at lines 931-932.

### Documenting surfaces

Roughly forty files name one or both CLIs outside `plans/done/**`. They fall into four classes:

1. **Live instructions that would break** — `repo-governance/development/quality/code/
14-ayokoding-www-link-validation.md` (documents `nx run ayokoding-www:links:check`, a target that
   does not exist), `apps/README.md`, `docs/reference/monorepo-structure.md`,
   `docs/how-to/setup-development-environment.md`.
2. **Illustrative examples in convention docs** — the `bdd-spec-test-mapping/**`,
   `nx-targets/**`, `specs-directory-structure/**`, `hexagonal-architecture-cli/**`,
   `git-fixture-isolation/**`, and `three-level-testing-standard/**` families cite these CLIs as
   worked examples. Each needs a live substitute (`rhino-cli` in every case) rather than deletion of
   the surrounding guidance.
3. **Generated or descriptive inventories** — `docs/reference/project-dependency-graph.md`,
   `docs/reference/system-architecture/*.md`, `docs/explanation/software-engineering/licensing/
dependency-compatibility.md`, `.dockerignore`.
4. **Agent-harness instruction surfaces** — two `.claude/skills/` reference files state the CLIs
   as live fact:
   - `docs-validating-links/reference/internal-link-validation.md:16` — "Their content links are
     validated by their respective CLI tools (`ayokoding-cli links check`, `ose-cli links check`),
     **not by this Skill's link validation rules**." After this plan that sentence is inverted:
     `md-links` covers both trees. Left uncorrected it would steer a future validation run away
     from exactly the trees this plan just armed.
   - `docs-creating-by-example-tutorials/reference/checking-grouping-compliance-and-diagrams.md:49`
     — "If the link checker (`ayokoding-cli`) is wired to validate anchors…"

   Editing `.claude/**` obliges regenerating the `.opencode/`, `.cursor/`, and `.amazonq/` mirrors
   via `npm run generate:bindings` **in the same commit**; the mirrors are never hand-edited.

5. **Live forward-looking plan idea** — `plans/ideas/q2-not-urgent-important/
beavernest-first-deploy.md` proposes deploying `beavernest-app-web` to Vercel (9 mentions) and
   cites an `apps/beavernest-app-web/README.md` that does not exist. It is a substantive proposal,
   not index prose, and becomes unexecutable once the directory is deleted.
6. **Historical record — do not touch** — `apps/*/content/**` published articles,
   `social-media-posts/**`, `plans/done/**`. These describe what was true when written.

### Surfaces the family globs do not catch

These are named individually because they sit outside the six convention families in class 2 and
outside the inventory list in class 3:

- `repo-governance/conventions/structure/app-readme-vs-specs/07-standard-4-variants-creation-rules-and-migration.md:27`
- `repo-governance/development/quality/specs-application-sync/06-existing-patterns-to-follow.md:43`
- `repo-governance/development/workflow/worktree-setup/04-dependency-isolation-language-breadth-and-idempotency.md:29`
- `repo-governance/workflows/repo/repo-dependency-bump-planning/04-phase-1-inventory.md:15,22`
- `repo-governance/conventions/structure/licensing/02-standards.md:35,41` — live MIT rows
- `repo-governance/conventions/structure/licensing/03-applying-and-validating.md:51`
- `repo-governance/conventions/structure/file-naming/01-app-naming-types.md:25`
- `docs/explanation/software-engineering/programming-languages/typescript/README.md:228,682`
- `.claude/skills/swe-developing-applications-common/reference/nx-monorepo-integration.md:19` — a
  **third** agent-harness skill file, citing `rust-commons` as a live naming-convention example
- `docs/how-to/add-new-lib.md:32,40` — lists `rust-commons` twice, including a stale capability
  claim ("Shared Rust utilities (link-checking, HTTP)")
- `docs/explanation/software-engineering/architecture/ddd-hexagonal-in-practice/cross-context-integration-standards.md:208`
  — names `libs/rust-commons` as the "Current shared kernel location"
- `docs/explanation/software-engineering/architecture/ddd-hexagonal-in-practice/bounded-context-mapping-standards.md:54`
  — cites `libs/rust-commons` as the Shared Kernel worked example
- `repo-governance/development/infra/ci-conventions/05-test-manifestations-and-gherkin-consumption-matrix.md:24`
  — a `rust-commons` row in a live matrix
- `repo-governance/workflows/infra/development-environment-setup/09-phase-7-rust-ecosystem.md:11` —
  "Required for: `rhino-cli`, `rust-commons`"

The two DDD/shared-kernel docs need judgement, not deletion: `rust-commons` is their worked example
of a shared kernel, and removing it leaves the concept unillustrated. Substitute `libs/web-ui-token`
or `libs/ts-env-loader`, both live shared libraries, rather than striking the example.

The delivery does not rely on this list being exhaustive: its acceptance criterion is a repo-wide
grep returning zero outside the historical-record roots, so a surface missed here still fails the
step.

## The `md-links` Coverage Gap — Measured

`repo-config.yml`'s `md-links` gate excludes `plans/done`, `apps/ayokoding-www/content`, and
`apps/ose-www/content`. Dropping the two content exclusions was measured on this branch:

```
rhino-cli md links validate --exclude plans/done
```

**Result: exactly one pre-existing broken link in either content tree.**

| File                                                                                          | Line | Broken target                   | Cause                                                                                                            |
| --------------------------------------------------------------------------------------------- | ---- | ------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `apps/ayokoding-www/content/en/learn/courses/chart-of-accounts-and-data-modeling/overview.md` | 10   | `../sql-essentials/overview.md` | The `sql-essentials` course has no course-level `overview.md`; it has `_index.md`, `learning/`, and `drilling/`. |

`apps/ose-www/content/**` produced **zero** broken links.

The link was a lone outlier. Measured with
`grep -rl 'sql-essentials/learning/overview\.md' apps/ayokoding-www/content`: **23 files** use the
prevailing `../sql-essentials/learning/overview.md` form, and after the fix **zero** files use the
broken `../sql-essentials/overview.md` form. (A wider grep for the bare string `sql-essentials`
matches 47 files, but most of those are `_index.md` `prerequisites:` keys and `/en/learn/...`
absolute site links, not relative file links — the 23 is the number that matters here.) **Fixed in
this plan** by retargeting line 10 to the prevailing form.

Related but deliberately out of scope: 23 of 181 course directories lack a course-level
`overview.md`. Only `sql-essentials` was linked as though it had one, so only that one link broke.
Authoring the missing overviews is content work, not clean-up — it is filed as a `plans/ideas/`
two-pager so the observation is not lost.

## File-Impact Analysis

```text
.
├── apps/
│   ├── ayokoding-cli/ [D] — dormant Rust link-checker, whole project
│   ├── ose-cli/ [D] — dormant Rust link-checker, whole project
│   ├── beavernest-app-web/ [D] — one LICENSE file, orphaned by the Flutter cutover
│   ├── ayokoding-www/project.json [E] — drop implicitDependencies
│   ├── ose-www/project.json [E] — drop the dead links:check target
│   ├── README.md [E] — drop both CLI rows
│   └── ayokoding-www/content/en/learn/courses/chart-of-accounts-and-data-modeling/overview.md [E] — retarget the one broken link (already applied)
├── libs/
│   ├── rust-commons/ [D] — orphaned once its only two consumers go
│   └── README.md [E] — drop the rust-commons entry
├── specs/
│   ├── apps/ayokoding/behavior/ayokoding-cli/ [D]
│   ├── apps/ose/behavior/ose-cli/ [D]
│   ├── libs/rust-commons/ [D]
│   ├── apps/{ayokoding,ose}/behavior/README.md [E] — drop index entries
│   ├── apps/{ayokoding,ose}/README.md [E] — drop index entries
│   ├── apps/{ayokoding,ose}/{containers,system-context}/*.md [E] — drop C4 references
│   ├── libs/rust-commons-adjacent indexes: specs/README.md [E], specs/libs/*/README.md [E]
│   └── libs/rust-commons/behavior/gherkin/links/check-links.feature [D]
├── repo-config.yml [E] — remove 3 registry entries (lines 105, 142, 174) and 2 md-links exclusions (931-932)
├── .dockerignore [E] — remove the two CLI paths
├── repo-governance/
│   ├── development/quality/code/14-ayokoding-www-link-validation.md [D] — documents a target that never existed
│   ├── development/quality/code/{15,16,17,18}-*.md [E] — git mv renumber to 14-17
│   ├── development/quality/code/README.md [E] and development/quality/code.md [E] — index entries
│   ├── development/infra/bdd-spec-test-mapping/*.md [E] — worked examples → rhino-cli
│   ├── development/infra/nx-targets/*.md [E] — worked examples → rhino-cli
│   ├── conventions/structure/specs-directory-structure/*.md [E] — worked examples → rhino-cli
│   ├── development/pattern/hexagonal-architecture-cli/*.md [E] — worked examples → rhino-cli
│   ├── development/quality/git-fixture-isolation/*.md [E] — worked examples → rhino-cli
│   ├── development/quality/three-level-testing-standard/*.md [E] — worked examples → rhino-cli
│   ├── conventions/structure/licensing/{02-standards,03-applying-and-validating}.md [E]
│   ├── conventions/structure/file-naming/01-app-naming-types.md [E]
│   ├── conventions/structure/app-readme-vs-specs/07-*.md [E]
│   ├── development/quality/specs-application-sync/06-*.md [E]
│   ├── development/workflow/worktree-setup/04-*.md [E]
│   └── workflows/repo/repo-dependency-bump-planning/04-phase-1-inventory.md [E]
├── docs/
│   ├── reference/{monorepo-structure,project-dependency-graph}.md [E]
│   ├── reference/system-architecture/{applications,components,technology-stack}.md [E]
│   ├── how-to/setup-development-environment.md [E]
│   └── explanation/{lint-safety-parity-decisions,standardize-app-spec-trees-parity-decisions}.md [E]
│       plus software-engineering/{licensing/dependency-compatibility,programming-languages/README,
│       programming-languages/typescript/README,architecture/c4-architecture-model/nx-workspace-visualization}.md [E]
├── .claude/skills/
│   ├── docs-validating-links/reference/internal-link-validation.md [E]
│   └── docs-creating-by-example-tutorials/reference/checking-grouping-compliance-and-diagrams.md [E]
├── .opencode/ [G], .cursor/ [G], .amazonq/ [G] — regenerated by npm run generate:bindings, same commit
├── plans/
│   ├── ideas/q4-not-urgent-not-important/simplify-ayokoding-ose-cli.md [D] — superseded
│   ├── ideas/q2-not-urgent-important/beavernest-first-deploy.md [E] — retire or rebase off the deleted app
│   ├── ideas/<new>-ayokoding-course-overview-gaps.md [N] — the 22 missing course overviews
│   ├── ideas/README.md [E] — index
│   └── in-progress/repo-clean-up/** [E] — this plan's own evidence and learnings
└── apps/rhino-cli/** — deliberately UNTOUCHED (parity boundary; see the section below)
```

### More Detail

The six convention families under `repo-governance/` are edited as bounded sets: their exact members
are discovered with
`grep -rln 'ayokoding-cli\|ose-cli\|rust-commons' repo-governance/development/infra/bdd-spec-test-mapping repo-governance/development/infra/nx-targets ...`
and recorded in `evidence/file-touch-ledger.md` before any edit, so the `*` in the tree resolves to a
named list at execution time rather than an open-ended sweep.

`.opencode/`, `.cursor/`, and `.amazonq/` are marked `[G]`: they are never hand-edited. They change
only as output of `npm run generate:bindings`, and must land in the same commit as the `.claude/`
edits that cause them.

## GitHub Actions

Searched: `grep -rn 'ayokoding-cli|ose-cli|rust-commons|beavernest-app-web' .github/` returns
**zero matches** across all 21 workflow files. No workflow is named for, triggered by, or filtered
on any retired project.

Every workflow that would otherwise touch them derives its work from `nx affected` or from
`repo-config.yml`, so removing the project registry entries is the only Actions-side change needed —
there is no workflow file to delete or edit. The delivery re-runs this search as a falsifiable check
rather than relying on this paragraph.

## Vercel Capability Declaration

`apps/ayokoding-www/vercel.json` and `apps/ose-www/vercel.json` exist, so the Vercel MCP capability
rule is triggered. **No Vercel capability is required by this plan and none is used.** The plan
touches those trees only to remove an Nx target, drop an `implicitDependencies` entry, and retarget
one content link — none of which affects build output, routing, headers, or deployment
configuration. No Vercel MCP availability probe is needed, and no deployment step appears in
`delivery.md`.

## Verification Strategy

Removal is proven by absence of invocation, not by inspection alone. Before deleting, a repo-wide
search for any execution path — Nx target `command`, npm script, `.husky/` hook, workflow step, or
`repo-config.yml` gate — must return zero for both binary names. After deleting, the full affected
graph must build and test clean, and `md-links` must run with no content exclusions.

The coverage claim is proven by a negative test: deliberately break a link inside each content tree
and confirm the gate fails. A gate that passes because it looked at nothing is the defect being
fixed; the same shape must not be reintroduced.

## Resolved Decisions

1. **`libs/rust-commons` is deleted** with its two consumers, along with `specs/libs/rust-commons/`
   and its `repo-config.yml` registry entry. Nothing else consumes it.
2. **`crane-cli` is out of scope.** It is live, not dormant, and its library dependency is real.
3. **The CLI Gherkin trees are deleted outright, not salvaged.** Their scenarios describe
   `links check` on a per-domain content root. `md links validate` already has its own spec
   coverage for the same behaviour at repository scope, so folding them in would duplicate, not add.

## The Parity Boundary Is Deliberately Not Touched

`apps/rhino-cli/**` is byte-identical across four repositories. **Four** of its files mention the
deleted paths, and **all four are inert**:

| File                                                                           | Nature                                                                                                                            |
| ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- |
| `src/application/doctor/checker.rs:1044,1059,1088`                             | Inside `#[cfg(test)]`. The strings name directories the test itself creates in a `TempDir`; they never touch the real repository. |
| `src/application/docs/links.rs:1091-1115`                                      | Same — `TempDir` fixture paths.                                                                                                   |
| `src/commands/specs_validate_counts.rs:5` and `tests/cargo_target_share.rs:38` | `//!` doc comments citing examples.                                                                                               |

None of them reads the real `libs/rust-commons`, so the deletion cannot break a rhino-cli test.
Editing them for tidiness would change the parity boundary and open a four-repo propagation
obligation for zero functional gain. They are left alone, and this paragraph is the record of why —
so a later reader does not mistake the stale names for an oversight.
