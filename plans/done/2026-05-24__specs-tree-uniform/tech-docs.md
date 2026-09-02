# Tech Docs — Specs Tree Uniformity Pass

## Gap Inventory

Numbered references trace back to acceptance criteria in [prd.md](./prd.md).

| ID    | Location                                                                | Current state                                                                                                                               | Target state                                                                                                                                                                                 | Severity | Source                                                                                                                                                                                       |
| ----- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GAP-1 | `specs/README.md` "Standard Folder Pattern" section                     | Documents flat `be/fe/fs/cli/gherkin/`                                                                                                      | Canonical five-folder tree + `behavior/<surface>/gherkin/`                                                                                                                                   | HIGH     | [Repo-grounded — `specs/README.md` lines 46–73]                                                                                                                                              |
| GAP-2 | `specs/README.md` "App Specs" + "Library Specs" + "Standards" lists     | Missing: ose-app, wahidyankf, crane. Lib list partially correct                                                                             | Lists every app present under `specs/apps/`                                                                                                                                                  | HIGH     | [Repo-grounded — `specs/README.md` lines 29–45 vs `find specs/apps -maxdepth 1 -type d`]                                                                                                     |
| GAP-3 | `specs/README.md` line 67                                               | "Contracts live at `specs/apps/{domain}/contracts/`"                                                                                        | Contracts live at `specs/apps/{domain}/containers/contracts/`                                                                                                                                | HIGH     | [Repo-grounded — `specs-directory-structure.md` line 271 + `specs/apps/organiclever/containers/contracts/README.md`]                                                                         |
| GAP-4 | `specs/apps/crane/`                                                     | Flat `gherkin/<feature>.feature` at app root                                                                                                | `behavior/cli/gherkin/<feature>.feature`                                                                                                                                                     | HIGH     | [Repo-grounded — `specs/apps/crane/README.md` lines 16–31 vs `specs-directory-structure.md` lines 184–193]                                                                                   |
| GAP-5 | `specs/apps/rhino/`                                                     | Only `behavior/cli/gherkin/` populated                                                                                                      | CLI-only surface profile: `product/`, `system-context/`, `containers/`, `components/cli/`, `behavior/cli/gherkin/`                                                                           | MEDIUM   | [Repo-grounded — `specs/apps/rhino/README.md` lines 18–24 vs `specs-directory-structure.md` line 151]                                                                                        |
| GAP-6 | `specs/apps/ayokoding/build-tools/`                                     | Legacy flat-root slug containing `gherkin/index-generation/`                                                                                | Migrated under `behavior/build-tools/gherkin/` OR documented as permanent slug                                                                                                               | MEDIUM   | [Repo-grounded — `specs/apps/ayokoding/README.md` lines 45–53]                                                                                                                               |
| GAP-7 | `apps/rhino-cli/src/internal/allowlist.rs` `AppsWithDDD`                | Lists `organiclever`, `wahidyankf`, `ose-platform`, `ayokoding`                                                                             | Inline-commented rationale for include/exclude per app; ose-app evaluated                                                                                                                    | LOW      | [Repo-grounded — `apps/rhino-cli/src/internal/allowlist.rs` exists per `find` output]                                                                                                        |
| GAP-8 | `specs/apps/ose-app/README.md` "For Product / Project Managers" section | Absent (organiclever has equivalent section)                                                                                                | Present with reading-order guidance                                                                                                                                                          | LOW      | [Repo-grounded — `specs/apps/ose-app/README.md` lines 1–66 vs `specs/apps/organiclever/README.md` lines 168–197]                                                                             |
| GAP-9 | CLI `gherkin/` trees across 4 apps                                      | Flat `.feature` files at root of `behavior/cli/gherkin/` (crane=11 files in flat `gherkin/`; rhino=44; ayokoding-cli=3; ose-platform-cli=1) | Domain subdirs everywhere: `behavior/cli/gherkin/<domain>/<feature>.feature` matching organiclever BE/web pattern. Convention §Domain Subdirectory Rules updated to drop CLI-flat exception. | HIGH     | [Repo-grounded — `ls` of each CLI gherkin folder vs `specs/apps/organiclever/behavior/be/gherkin/<domain>/` pattern, plus current carve-out at `specs-directory-structure.md` lines 184–193] |

## Target Structure per App

The five-folder tree row in
[specs-directory-structure.md §Per-Surface Variants](../../../repo-governance/conventions/structure/specs-directory-structure/canonical-app-spec-tree.md#per-surface-variants)
is authoritative. Mapping every in-scope app to its declared profile:

| App          | Surface profile              | Required folders                                                                                         | Has today                                 | Action                                                                               |
| ------------ | ---------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------- | ------------------------------------------------------------------------------------ |
| ayokoding    | Multi-CLI                    | `product/`, `system-context/`, `containers/`, `components/{web,api}/`, `behavior/{web,api,cli}/gherkin/` | All present + legacy `build-tools/`       | Resolve `build-tools/` per Decision D1 below; otherwise no structural action         |
| crane        | CLI-only                     | `product/`, `system-context/`, `containers/`, `components/cli/`, `behavior/cli/gherkin/`                 | `gherkin/<feature>.feature` only          | Full migration + new product/system-context/containers/components READMEs            |
| organiclever | Full-stack                   | All five plus `containers/contracts/`, `components/{be,web}/`, `behavior/{be,web}/gherkin/`              | Compliant                                 | No structural action                                                                 |
| ose-app      | Full-stack                   | Same as organiclever                                                                                     | Compliant                                 | Add "For Product / Project Managers" section (GAP-8); evaluate allowlist add (GAP-7) |
| ose-platform | Web-only + perspective `api` | `product/`, `system-context/`, `containers/`, `components/{web,api}/`, `behavior/{web,api}/gherkin/`     | Compliant (legacy `cli/` already retired) | No structural action                                                                 |
| rhino        | CLI-only                     | `product/`, `system-context/`, `containers/`, `components/cli/`, `behavior/cli/gherkin/`                 | Only `behavior/cli/gherkin/`              | Add four missing folders, each with `README.md` skeleton                             |
| wahidyankf   | Web-only                     | `product/`, `system-context/`, `containers/`, `components/web/`, `behavior/web/gherkin/`                 | Compliant                                 | No structural action                                                                 |

## Target Final `specs/` Tree (ASCII)

The full post-migration tree. Every leaf path here MUST exist (or be a directory containing
≥1 `.feature`) at plan completion. Per-domain `README.md` files are required at every
directory level but omitted from this rendering for brevity except where they sit at a
non-obvious depth.

```
specs/
├── README.md                                           # rewritten per Phase 1
├── LICENSE
├── apps/
│   ├── ayokoding/
│   │   ├── README.md
│   │   ├── product/README.md
│   │   ├── system-context/{README.md,context.md}
│   │   ├── containers/{README.md,container.md}
│   │   ├── components/
│   │   │   ├── README.md
│   │   │   ├── api/{README.md,component-api.md}
│   │   │   └── web/{README.md,component-web.md}
│   │   ├── ddd/
│   │   │   ├── README.md
│   │   │   ├── bounded-contexts.yaml
│   │   │   ├── bounded-context-map.md
│   │   │   └── ubiquitous-language/{README.md,<bc>.md}
│   │   └── behavior/
│   │       ├── README.md
│   │       ├── api/gherkin/
│   │       │   └── <domain>/<feature>.feature          # existing
│   │       ├── web/gherkin/
│   │       │   └── <domain>/<feature>.feature          # existing
│   │       ├── cli/gherkin/
│   │       │   └── links/links-check.feature           # NEW (Phase 6.a — only 1 feature exists)
│   │       └── build-tools/gherkin/                    # NEW (Phase 4.A, if D1==A)
│   │           └── index-generation/<feature>.feature
│   ├── crane/                                          # FULLY MIGRATED (Phase 2)
│   │   ├── README.md
│   │   ├── product/README.md                           # NEW skeleton
│   │   ├── system-context/README.md                    # NEW skeleton
│   │   ├── containers/README.md                        # NEW skeleton
│   │   ├── components/cli/README.md                    # NEW skeleton
│   │   └── behavior/cli/gherkin/
│   │       ├── README.md
│   │       ├── pdf/pdf-commands.feature
│   │       ├── content/{text-check,heading-check,nesting-check}.feature
│   │       ├── media/{table-check,figure-check,mermaid-validate,ocr-quality}.feature
│   │       ├── reporting/{report-management,skiplist-management}.feature
│   │       └── system/{check-all,version}.feature          # NEW (Phase 2)
│   ├── organiclever/                                   # ALREADY COMPLIANT
│   │   ├── README.md
│   │   ├── product/                                    # existing
│   │   ├── system-context/                             # existing
│   │   ├── containers/{contracts/,container.md,deployment.md}
│   │   ├── components/{be,web}/                        # existing
│   │   ├── ddd/                                        # existing
│   │   └── behavior/{be,web}/gherkin/<domain>/<feature>.feature
│   ├── ose-app/                                        # ALREADY COMPLIANT (+ PM section added Phase 5)
│   │   ├── README.md                                   # NEW PM section
│   │   ├── product/                                    # existing
│   │   ├── system-context/                             # existing
│   │   ├── containers/{contracts/,...}
│   │   ├── components/                                 # existing
│   │   ├── ddd/                                        # existing
│   │   └── behavior/{be,web}/gherkin/<domain>/<feature>.feature
│   ├── ose-platform/                                   # ALREADY COMPLIANT (+ cli regrouped Phase 6.b)
│   │   ├── README.md
│   │   ├── product/                                    # existing
│   │   ├── system-context/                             # existing
│   │   ├── containers/                                 # existing
│   │   ├── components/{api,web}/                       # existing
│   │   ├── ddd/                                        # existing
│   │   └── behavior/
│   │       ├── api/gherkin/<domain>/<feature>.feature  # existing
│   │       ├── web/gherkin/<domain>/<feature>.feature  # existing
│   │       └── cli/gherkin/
│   │           └── links/links-check.feature           # NEW (Phase 6.b — single-feature domain)
│   ├── rhino/                                          # FILLED OUT + REGROUPED (Phase 3)
│   │   ├── README.md
│   │   ├── product/README.md                           # NEW skeleton
│   │   ├── system-context/README.md                    # NEW skeleton
│   │   ├── containers/README.md                        # NEW skeleton
│   │   ├── components/cli/README.md                    # NEW skeleton
│   │   └── behavior/cli/gherkin/
│   │       ├── README.md
│   │       ├── agents/{agents-detect-duplication,agents-sync,agents-validate-claude,agents-validate-naming}.feature
│   │       ├── ddd/{ddd-bc,ddd-ul}.feature
│   │       ├── docs/{docs-validate-frontmatter,docs-validate-heading-hierarchy,docs-validate-links,docs-validate-mermaid,docs-validate-naming}.feature
│   │       ├── env/{env-backup,env-init,env-restore}.feature
│   │       ├── git/git-pre-commit.feature
│   │       ├── repo-governance/{repo-governance-agents-md-size,repo-governance-audit,repo-governance-emoji-audit,repo-governance-frontmatter-audit,repo-governance-layer-coherence,repo-governance-license-audit,repo-governance-readme-index-audit,repo-governance-traceability-audit,repo-governance-vendor-audit}.feature
│   │       ├── spec-coverage/spec-coverage-validate.feature
│   │       ├── test-coverage/{test-coverage-diff,test-coverage-merge,test-coverage-validate}.feature
│   │       ├── workflows/workflows-validate-naming.feature
│   │       └── system/{doctor,version,check-all}.feature   # singletons land here
│   └── wahidyankf/                                     # ALREADY COMPLIANT
│       └── ...                                         # unchanged
├── apps-labs/
│   └── README.md                                       # placeholder, empty
└── libs/
    ├── golang-commons/
    │   └── gherkin/<package>/<feature>.feature         # already domain-grouped
    ├── hugo-commons/
    │   └── gherkin/links/check-links.feature           # already grouped; lib retention TBD
    └── web-ui/
        └── gherkin/<component>/<component>.feature     # already grouped
```

**Universal invariant** (post-plan): `find specs -type f -name '*.feature'` must return zero
results matching `behavior/<surface>/gherkin/<feature>.feature` — every feature lives at
`behavior/<surface>/gherkin/<domain>/<feature>.feature` or
`gherkin/<package>/<feature>.feature` (libs).

## Decisions

### D1 — Ayokoding `build-tools/` slug fate

**Options**:

- **D1.A — Migrate under `behavior/build-tools/gherkin/`.** Mechanically simplest; consistent with the
  "all Gherkin under `behavior/<surface>/gherkin/`" rule. Risk: `build-tools` is not in the canonical
  surface enum (`be`, `web`, `cli`) so `validate-tree` may reject it as a non-canonical surface.
  Requires rhino-cli code change to accept `build-tools` as a valid surface.
- **D1.B — Promote to permanent perspective slug in convention.** Update
  [specs-directory-structure.md](../../../repo-governance/conventions/structure/specs-directory-structure.md)
  to list `build-tools` alongside `api` as a permitted perspective slug at app root. No code change needed.
  Risk: deviates from the "all behavior under `behavior/`" rule and re-opens the precedent the
  Migration Path section explicitly closed.
- **D1.C — Inline migration into existing `behavior/cli/gherkin/`** since build-tools scripts execute as
  CLI invocations under the same `ayokoding-cli` binary. Risk: conflates two different test surfaces
  (binary CLI command behavior vs build-time index generation).

**Recommendation**: **D1.A**. Add `build-tools` to the canonical surface enum in `rhino-cli`'s
`validate-tree` (one line change in surface allowlist; locate via
`grep -rn 'be\|web\|cli' apps/rhino-cli/src/specs`). The "behavior cuts across all C4 levels"
principle from [specs-directory-structure.md line 143](../../../repo-governance/conventions/structure/specs-directory-structure.md)
extends naturally to a build-time surface. [Judgment call]

**Resolution required before Step 2 of delivery.md.** Default to D1.A unless validator-runner objects
during execution.

### D2 — Allowlist policy for `AppsWithDDD`

**Options**:

- **D2.A — Add `ose-app` to allowlist.** Surfaces any latent findings. Aligned with "every full-stack
  app with a DDD registry is validated".
- **D2.B — Exclude `ose-app` until BC content lands.** Avoids noise from empty BCs (all four show
  `--` feature counts).

**Recommendation**: **D2.A** — add ose-app to the allowlist BUT in a separate commit AFTER all
other migrations land, so any latent findings can be triaged in isolation. Add inline `//`
comment in `allowlist.rs` documenting both included apps' rationale.
[Repo-grounded — `specs/apps/ose-app/README.md` lines 46–52 show all BCs at `--`]

**Resolution required at delivery.md Phase 5.**

### D3 — Crane's missing C4 layers

CLI-only profile requires `product/`, `system-context/`, `containers/`, `components/cli/`. Crane has
none. Authoring full content for these is out of scope per BRD Non-Goals.

**Recommendation**: Create each folder with a `README.md` skeleton that:

1. States the folder's purpose per convention.
2. Cites the canonical convention link.
3. Marks content as `_To be populated in a follow-up authoring plan_` per
   [plan-anti-hallucination.md](../../../repo-governance/development/quality/plan-anti-hallucination.md)
   refuse-on-uncertainty rule.

This satisfies `validate-counts` (folders exist) and `validate-tree` (canonical shape) without
forcing this structural plan to author technical content. [Judgment call]

### D4 — Rhino's missing C4 layers

Same recommendation as D3. Skeleton READMEs only; behavior preserved as the source of truth for
rhino-cli command contracts.

### D5 — Domain groupings for CLI gherkin trees

Per US-8 / AC-8, every flat CLI `gherkin/` tree must adopt domain subdirectories matching
organiclever's BE/web pattern. The domain choice for each app is delegated to execution-time
maintainer judgment, but the plan supplies a default mapping inferred from current filename
prefixes so execution has a starting point.

**Default groupings (apply unless maintainer overrides at execution time):**

| App                                             | Source files                                                                                                                                                                                                                                                                                                                                                                                                                                              | Proposed domain subdirs                                                                                                                                                                                                                            |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `specs/apps/crane/behavior/cli/gherkin/`        | `pdf-commands`, `text-check`, `heading-check`, `nesting-check`, `table-check`, `figure-check`, `mermaid-validate`, `ocr-quality`, `report-management`, `skiplist-management`, `check-all`, `version` (12 features, after migration from flat `gherkin/` — verified 2026-05-23)                                                                                                                                                                            | `pdf/`, `content/` (text + heading + nesting), `media/` (table + figure + mermaid + ocr), `reporting/` (report + skiplist), `system/` (check-all + version) — collapses 12 files into 5 domains                                                    |
| `specs/apps/rhino/behavior/cli/gherkin/`        | 34 features total: 30 domain-prefixed files at root + 4 already in `specs/` subdomain (`validate-adoption`, `validate-counts`, `validate-links`, `validate-tree`). Domain prefixes: `agents-*` (4), `ddd-*` (2), `docs-*` (5), `env-*` (3), `git-*` (1), `repo-governance-*` (9), `spec-coverage-*` (1), `test-coverage-*` (3), `workflows-*` (1), plus `doctor` as the only standalone singleton. (Re-verify count at execution start — `ls` may drift.) | `agents/`, `ddd/`, `docs/`, `env/`, `git/`, `repo-governance/`, `spec-coverage/`, `test-coverage/`, `workflows/`, `specs/` (already grouped — leave in place), plus `system/` for `doctor`. One-feature singletons fold into their natural domain. |
| `specs/apps/ayokoding/behavior/cli/gherkin/`    | `links-check` (1 feature; `check-all` and `version` do NOT exist on disk — verified 2026-05-23)                                                                                                                                                                                                                                                                                                                                                           | `links/` (links-check)                                                                                                                                                                                                                             |
| `specs/apps/ose-platform/behavior/cli/gherkin/` | `links-check`                                                                                                                                                                                                                                                                                                                                                                                                                                             | `links/` (single feature; one-feature domain is allowed per convention)                                                                                                                                                                            |

**Severity escape hatch**: For one-feature domains (e.g., `ose-platform/links/`), the convention
update must explicitly permit single-file domain folders so `validate-tree` does not flag them.
[Judgment call]

**Resolution required at delivery.md Phase 0** (before Phase 2 crane migration begins).
Default to the table above unless maintainer overrides per app.

## Migration Recipes

### R1 — Crane: flat `gherkin/` → `behavior/cli/gherkin/<domain>/`

Migrates crane to the CLI-only five-folder tree AND groups every `.feature` under a domain
subdir per [§D5](#d5--domain-groupings-for-cli-gherkin-trees).

```bash
# All commands run inside the worktree at worktrees/specs-tree-uniform/
cd worktrees/specs-tree-uniform

# Step 1 — create destination tree with domain subdirs
mkdir -p specs/apps/crane/behavior/cli/gherkin/{pdf,content,media,reporting,system}
mkdir -p specs/apps/crane/product
mkdir -p specs/apps/crane/system-context
mkdir -p specs/apps/crane/containers
mkdir -p specs/apps/crane/components/cli

# Step 2 — git mv every .feature into its domain folder per D5 grouping
# pdf/
git mv specs/apps/crane/gherkin/pdf-commands.feature       specs/apps/crane/behavior/cli/gherkin/pdf/pdf-commands.feature
# content/ (text + heading + nesting)
git mv specs/apps/crane/gherkin/text-check.feature         specs/apps/crane/behavior/cli/gherkin/content/text-check.feature
git mv specs/apps/crane/gherkin/heading-check.feature      specs/apps/crane/behavior/cli/gherkin/content/heading-check.feature
git mv specs/apps/crane/gherkin/nesting-check.feature      specs/apps/crane/behavior/cli/gherkin/content/nesting-check.feature
# media/ (table + figure + mermaid + ocr)
git mv specs/apps/crane/gherkin/table-check.feature        specs/apps/crane/behavior/cli/gherkin/media/table-check.feature
git mv specs/apps/crane/gherkin/figure-check.feature       specs/apps/crane/behavior/cli/gherkin/media/figure-check.feature
git mv specs/apps/crane/gherkin/mermaid-validate.feature   specs/apps/crane/behavior/cli/gherkin/media/mermaid-validate.feature
git mv specs/apps/crane/gherkin/ocr-quality.feature        specs/apps/crane/behavior/cli/gherkin/media/ocr-quality.feature
# reporting/ (report + skiplist)
git mv specs/apps/crane/gherkin/report-management.feature  specs/apps/crane/behavior/cli/gherkin/reporting/report-management.feature
git mv specs/apps/crane/gherkin/skiplist-management.feature specs/apps/crane/behavior/cli/gherkin/reporting/skiplist-management.feature
# system/ (check-all + version — verified present 2026-05-23)
git mv specs/apps/crane/gherkin/check-all.feature          specs/apps/crane/behavior/cli/gherkin/system/check-all.feature
git mv specs/apps/crane/gherkin/version.feature            specs/apps/crane/behavior/cli/gherkin/system/version.feature
# README
git mv specs/apps/crane/gherkin/README.md                  specs/apps/crane/behavior/cli/gherkin/README.md

# Step 3 — sweep all path references in the same commit. Two sweeps needed because
# files moved from a flat layout into different domain subdirs — a single sed can't
# rewrite filename-aware paths. Most references use directory paths only.
grep -rln 'specs/apps/crane/gherkin' apps libs .github .husky docs repo-governance \
  | xargs -I {} sed -i.bak 's|specs/apps/crane/gherkin|specs/apps/crane/behavior/cli/gherkin|g' {}
find . -name '*.bak' -delete
# Hand-verify any per-file refs (e.g., direct .feature path imports in step files).
# `grep -rn 'pdf-commands.feature\|text-check.feature\|...' apps/crane-cli/` and
# rewrite per the D5 grouping table.

# Step 4 — author skeleton READMEs (see R3 template) for product/, system-context/,
# containers/, components/cli/. Also a one-paragraph index README in each new domain
# subdir (pdf/, content/, media/, reporting/, system/) listing its features.

# Step 5 — update specs/apps/crane/README.md "Structure" block to show domain subdirs

# Step 6 — verify
nx run rhino-cli:validate:specs-tree --apps crane
nx run rhino-cli:validate:specs-counts --apps crane
nx run rhino-cli:validate:specs-links --apps crane
nx run crane-cli:test:unit
nx run crane-cli:test:integration

# Step 7 — atomic commit
git add -A
git commit -m "refactor(specs/crane): migrate to canonical CLI tree with domain subdirs"
```

**Pre-flight verification** (mandatory before `git mv`): confirm the exact feature-file list
with `ls specs/apps/crane/gherkin/`. The list above is from a 2026-05-23 `find` and may drift
before execution. If new features have appeared, assign each to a D5 domain at migration time.
[Repo-grounded — verify at execution start]

### R2 — Rhino: add missing top-level folders AND regroup `.feature` files into domain subdirs

Two changes in one atomic commit: (a) create the four missing CLI-only top-level folders,
(b) regroup the 34 existing `.feature` files under `behavior/cli/gherkin/<domain>/` per
the D5 grouping table.

```bash
# Step 1 — create missing C4 folders
mkdir -p specs/apps/rhino/product
mkdir -p specs/apps/rhino/system-context
mkdir -p specs/apps/rhino/containers
mkdir -p specs/apps/rhino/components/cli

# Step 2 — create CLI-gherkin domain subdirs
mkdir -p specs/apps/rhino/behavior/cli/gherkin/{agents,ddd,docs,env,git,repo-governance,spec-coverage,test-coverage,workflows,system}

# Step 3 — regroup features by prefix.
# Idiom: for every `<domain>-*.feature` file at the gherkin root, git mv into <domain>/.
# Execute these one domain at a time so each line is auditable:
for f in specs/apps/rhino/behavior/cli/gherkin/agents-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/agents/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/ddd-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/ddd/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/docs-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/docs/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/env-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/env/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/git-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/git/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/repo-governance-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/repo-governance/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/spec-coverage-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/spec-coverage/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/test-coverage-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/test-coverage/"$(basename "$f")"
done
for f in specs/apps/rhino/behavior/cli/gherkin/workflows-*.feature; do
  git mv "$f" specs/apps/rhino/behavior/cli/gherkin/workflows/"$(basename "$f")"
done
# system/ catches the singletons that have no domain prefix.
# Verified 2026-05-23: only doctor.feature exists as a standalone singleton at root.
# version.feature and check-all.feature are NOT present in rhino gherkin root.
git mv specs/apps/rhino/behavior/cli/gherkin/doctor.feature       specs/apps/rhino/behavior/cli/gherkin/system/doctor.feature
# Re-verify nothing left at the root via `find specs/apps/rhino/behavior/cli/gherkin -maxdepth 1 -name '*.feature'`
# — output must be empty before commit.
# NOTE: 4 features already live under a specs/ subdomain (validate-adoption, validate-counts,
# validate-links, validate-tree) and must also be handled: they are already domain-grouped
# under behavior/cli/gherkin/specs/ and do NOT need to be moved.

# Step 4 — sweep path references for rhino integration tests + Nx inputs
grep -rln 'specs/apps/rhino/behavior/cli/gherkin/' apps libs .github .husky docs repo-governance \
  > /tmp/rhino-spec-refs.txt
# Inspect /tmp/rhino-spec-refs.txt — each match must be rewritten by hand or scripted
# per the new domain layout. Pre-push will fail loudly if any reference is stale.

# Step 5 — author skeleton READMEs at product/, system-context/, containers/,
# components/cli/ and a one-paragraph index README in each new domain subdir.

# Step 6 — update specs/apps/rhino/README.md and behavior/cli/gherkin/README.md
# "Structure" blocks to show the domain layout.

# Step 7 — verify
nx run rhino-cli:validate:specs-tree --apps rhino
nx run rhino-cli:validate:specs-counts --apps rhino
nx run rhino-cli:validate:specs-links --apps rhino
nx run rhino-cli:test:quick
nx run rhino-cli:test:integration

# Step 8 — atomic commit
git add -A
git commit -m "refactor(specs/rhino): fill out CLI tree and regroup features into domains"
```

### R3 — Skeleton README template

Verbatim contents for each placeholder `README.md` created in R1 and R2. Replace `<APP>` and
`<FOLDER>` per file.

```markdown
# <APP> — <FOLDER>

<one-line description of this C4 level for <APP>>

> _Skeleton placeholder. Substantive content to be authored in a follow-up plan._

See [Specs Directory Structure Convention](../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for the canonical purpose of this folder.
```

Relative-link depth (`../../../../`) assumes the folder is one level below the app spec root.
For deeper folders (e.g., `components/cli/`) adjust to `../../../../../`. Verify resolution with
`validate:specs-links`.

### R4 — Ayokoding `build-tools/` migration (assuming D1.A)

```bash
# Add 'build-tools' to rhino-cli surface enum first (one-line edit)
# Locate via: grep -rn '"cli"\|"be"\|"web"' apps/rhino-cli/src/specs
# Add entry to the surface-allowlist constant; re-build rhino-cli; re-run validator

mkdir -p specs/apps/ayokoding/behavior/build-tools/gherkin
git mv specs/apps/ayokoding/build-tools/gherkin/* specs/apps/ayokoding/behavior/build-tools/gherkin/
rmdir specs/apps/ayokoding/build-tools/gherkin
rmdir specs/apps/ayokoding/build-tools

# Sweep references
grep -rln 'specs/apps/ayokoding/build-tools' apps libs .github .husky docs repo-governance \
  | xargs -I {} sed -i.bak 's|specs/apps/ayokoding/build-tools/gherkin|specs/apps/ayokoding/behavior/build-tools/gherkin|g' {}
find . -name '*.bak' -delete

# Update specs/apps/ayokoding/README.md — remove the "Out of scope" note for build-tools

# Verify
nx run rhino-cli:validate:specs-tree --apps ayokoding
nx run rhino-cli:validate:specs-counts --apps ayokoding
nx run rhino-cli:validate:specs-links --apps ayokoding
```

### R5 — Root README rewrite

In-place rewrite of `specs/README.md` Sections "Standard Folder Pattern", "App Specs",
"Experimental App Specs", "Library Specs". New content sketched in
[delivery.md Phase 1](./delivery.md#phase-1--root-readme-rewrite).

### R6 — Allowlist update

The allowlist is implemented as a function, not a constant. The actual API (confirmed via
`apps/rhino-cli/src/internal/allowlist.rs`):

```rust
pub fn apps_with_ddd() -> &'static [&'static str] {
    &["organiclever", "wahidyankf", "ose-platform", "ayokoding"]
}
```

To add `ose-app`, extend the array literal inside the function body:

```rust
// apps/rhino-cli/src/internal/allowlist.rs
// Apps with a populated DDD bounded-context registry.
// Inclusion criterion: specs/apps/<app>/ddd/bounded-contexts.yaml exists AND has ≥1
// BC entry whose `code:` path resolves to actual layered source.
// ose-app: included as of <commit-sha> — BC content authoring tracked separately.
pub fn apps_with_ddd() -> &'static [&'static str] {
    &[
        "organiclever",
        "wahidyankf",
        "ose-platform",
        "ayokoding",
        "ose-app",  // added by specs-tree-uniform plan
    ]
}
```

**Important**: The `#[cfg(test)]` block in the same file contains a `membership` test that
asserts `v.len() == 4`. After adding `"ose-app"`, update that assertion to `v.len() == 5`
and add `assert!(v.contains(&"ose-app"));`.

[Repo-grounded — `apps/rhino-cli/src/internal/allowlist.rs` confirmed: function `apps_with_ddd()`
returning `&'static [&'static str]`; existing test at line 13 asserts `.len() == 4`.]

### R7 — Domain regrouping for ayokoding-cli, ose-platform-cli, and validator enforcement

Two short atomic commits — one per app — plus a third commit that hardens the validator and
the convention so future flat CLI gherkin layouts are rejected at the gate.

```bash
# Commit 7.a — ayokoding-cli domain regrouping (1 feature)
# Verified 2026-05-23: only links-check.feature exists. check-all.feature and
# version.feature are NOT present — do not attempt git mv for those.
mkdir -p specs/apps/ayokoding/behavior/cli/gherkin/links
git mv specs/apps/ayokoding/behavior/cli/gherkin/links-check.feature specs/apps/ayokoding/behavior/cli/gherkin/links/links-check.feature
# Sweep refs in step files + Nx inputs
grep -rln 'ayokoding/behavior/cli/gherkin/' apps libs .github .husky docs repo-governance > /tmp/ayko-cli-refs.txt
# Inspect and rewrite each match by hand (per-file paths only)
nx run rhino-cli:validate:specs-tree --apps ayokoding
nx run rhino-cli:validate:specs-counts --apps ayokoding
nx run ayokoding-cli:test:quick
git add -A
git commit -m "refactor(specs/ayokoding): regroup cli features into domain subdirs"

# Commit 7.b — ose-platform-cli domain regrouping (1 feature, single-feature domain)
mkdir -p specs/apps/ose-platform/behavior/cli/gherkin/links
git mv specs/apps/ose-platform/behavior/cli/gherkin/links-check.feature specs/apps/ose-platform/behavior/cli/gherkin/links/links-check.feature
grep -rln 'ose-platform/behavior/cli/gherkin/' apps libs .github .husky docs repo-governance > /tmp/osep-cli-refs.txt
# Inspect and rewrite
nx run rhino-cli:validate:specs-tree --apps ose-platform
nx run rhino-cli:validate:specs-counts --apps ose-platform
nx run ose-cli:test:quick
git add -A
git commit -m "refactor(specs/ose-platform): regroup cli features into domain subdirs"

# Commit 7.c — validator enforcement (Rust) + convention update
# ADD a new check (no carve-out exists to remove — this is a net-new rule).
# Locate the validate_spec_tree function in apps/rhino-cli/src/internal/specs.rs and
# apps/rhino-cli/src/commands/specs_validate_tree.rs. Neither file currently checks for
# flat .feature files under behavior/<surface>/gherkin/. The task is to write this check
# from scratch as a new helper that walks behavior/<surface>/gherkin/ and emits HIGH for
# any .feature found at depth 0 (directly under gherkin/, not inside a domain subdir).
# Add a unit test covering the new rule.
cargo check --manifest-path apps/rhino-cli/Cargo.toml
nx run rhino-cli:test:quick
# Edit repo-governance/conventions/structure/specs-directory-structure.md:
#   - drop "CLI specs use a flat structure under `gherkin/` with NO domain subdirectories"
#     (current lines 184–193)
#   - replace with "Every surface (BE, web, CLI) uses domain subdirectories under `gherkin/`.
#     Single-feature domains are permitted when the CLI surface area is small."
#   - append a §Migration Path retirement note dated YYYY-MM-DD documenting the change.
git add -A
git commit -m "feat(rhino-cli): enforce domain subdirs under every behavior/<surface>/gherkin/"
```

This commit triplet is the structural-side counterpart to the Phase 7 propagation step that
`repo-rules-maker` reflects into all other governance/agent surfaces.

## File Impact

| File                                                                                                                         | Action                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `specs/README.md`                                                                                                            | Rewrite Standard Folder Pattern, App Specs, Library Specs sections                                                       |
| `specs/apps/crane/README.md`                                                                                                 | Update Structure block + Running the Tests paths                                                                         |
| `specs/apps/crane/gherkin/`                                                                                                  | Deleted via `git mv`                                                                                                     |
| `specs/apps/crane/behavior/cli/gherkin/**`                                                                                   | New location for every feature file                                                                                      |
| `specs/apps/crane/{product,system-context,containers,components/cli}/README.md`                                              | New skeleton files                                                                                                       |
| `specs/apps/rhino/{product,system-context,containers,components/cli}/README.md`                                              | New skeleton files                                                                                                       |
| `specs/apps/rhino/README.md`                                                                                                 | Update Structure block to show full CLI-only tree                                                                        |
| `specs/apps/ayokoding/README.md`                                                                                             | Remove "Out of scope" legacy slug warning for `build-tools/`                                                             |
| `specs/apps/ayokoding/build-tools/`                                                                                          | Deleted via `git mv` (if D1.A chosen)                                                                                    |
| `specs/apps/ayokoding/behavior/build-tools/gherkin/**`                                                                       | New location (if D1.A chosen)                                                                                            |
| `specs/apps/ose-app/README.md`                                                                                               | Add "For Product / Project Managers" section                                                                             |
| `apps/rhino-cli/src/internal/allowlist.rs`                                                                                   | Add `ose-app` to allowlist + inline rationale comment                                                                    |
| `apps/rhino-cli/src/specs/<surface-enum>.rs` (if D1.A)                                                                       | Add `build-tools` to canonical surface enum                                                                              |
| `apps/rhino-cli/src/specs/validate_tree.rs`                                                                                  | Add HIGH finding for flat `.feature` directly under any `behavior/<surface>/gherkin/`; add unit test for the rule        |
| `repo-governance/conventions/structure/specs-directory-structure.md`                                                         | Drop CLI-flat exception (lines 184–193); add domain-subdir-for-all-surfaces rule; append §Migration Path retirement note |
| `apps/crane-cli/tests/unit/steps/**`                                                                                         | Update any hardcoded `specs/apps/crane/gherkin` path references plus per-file domain-subdir paths                        |
| `apps/crane-cli/project.json`                                                                                                | Update Nx target `inputs` referencing the spec path                                                                      |
| `apps/ayokoding-cli/**` (step files + project.json)                                                                          | Update path references to the new `behavior/cli/gherkin/<domain>/` layout                                                |
| `apps/ose-cli/**` (step files + project.json)                                                                                | Update path references to the new `behavior/cli/gherkin/links/` layout                                                   |
| `specs/apps/{crane,rhino,ayokoding,ose-platform}/behavior/cli/gherkin/<domain>/README.md`                                    | New one-paragraph domain index README per domain subdir created                                                          |
| `docs/reference/monorepo-structure.md`                                                                                       | Update spec tree references to canonical layout                                                                          |
| `docs/how-to/add-new-app.md`                                                                                                 | Teach domain-subdir layout to every new app added going forward                                                          |
| `docs/reference/project-dependency-graph.md`                                                                                 | Update any stale spec path references                                                                                    |
| `docs/explanation/software-engineering/automation-testing/tools/playwright/{bdd,configuration}.md`                           | Update spec path examples                                                                                                |
| `docs/explanation/software-engineering/development/test-driven-development-tdd/integration-testing-standards.md`             | Update spec path examples                                                                                                |
| `docs/explanation/software-engineering/programming-languages/typescript/testing.md`                                          | Update spec path examples                                                                                                |
| `repo-governance/development/infra/{ci-conventions,nx-targets,bdd-spec-test-mapping,temporary-files}.md`                     | Update spec tree references                                                                                              |
| `repo-governance/development/quality/{three-level-testing-standard,specs-application-sync,feature-change-completeness}.md`   | Update spec tree references                                                                                              |
| `repo-governance/workflows/specs/specs-quality-gate.md`                                                                      | Update workflow references                                                                                               |
| `repo-governance/workflows/repo/repo-ose-primer-extraction-execution.md`                                                     | Update extraction-scope references                                                                                       |
| `repo-governance/conventions/structure/{README,deterministic-vs-ai-validation-split,app-readme-vs-specs,ose-primer-sync}.md` | Update convention cross-refs                                                                                             |
| `repo-governance/conventions/writing/{dynamic-collection-references,readme-quality}.md`                                      | Update examples if stale                                                                                                 |
| `repo-governance/principles/general/simplicity-over-complexity.md`                                                           | Update spec-tree example if it cites flat CLI                                                                            |
| `apps/{crane-cli,rhino-cli,ayokoding-cli,ose-cli}/README.md`                                                                 | Per-app READMEs reflect post-migration spec paths                                                                        |
| `.claude/agents/{specs-checker,specs-maker,specs-fixer,web-researcher,repo-ose-primer-propagation-maker}.md`                 | Update example paths and validation rules                                                                                |
| `.claude/skills/repo-syncing-with-ose-primer/{SKILL,reference/extraction-scope,reference/transforms}.md`                     | Update extraction scope and transforms                                                                                   |
| `.claude/skills/apps-organiclever-web-developing-content/SKILL.md`                                                           | Update spec-path examples if stale                                                                                       |

The exact set of step-definition files and Nx config files touched by path sweeps is determined
by `grep -rln 'specs/apps/crane/gherkin' .` AND `grep -rln 'specs/apps/ayokoding/build-tools' .`
at execution start. Both greps are part of delivery.md Step 0.

## Path-Reference Sweep Discipline

Per [Specs Directory Structure Convention §Migration Path](../../../repo-governance/conventions/structure/specs-directory-structure/migration-path.md#migration-path-five-folder-to-logical-owner-corpus):

> The atomic commit is mandatory — splitting the move and the path updates causes test failures
> between commits.

Mechanical rule: in any commit that runs `git mv` on a spec path, **the same commit MUST contain
all `sed`-driven path updates** for that path. Do not push between `git mv` and the sed sweep.

## Rollback

Each migration commit is atomic, so rollback is `git revert <commit-sha>` for any one of:

- Root README rewrite
- Crane migration (with domain subdirs)
- Rhino fill-out (with domain regrouping)
- Ayokoding build-tools migration
- Ayokoding-cli domain regrouping (R7.a)
- ose-platform-cli domain regrouping (R7.b)
- Validator enforcement + convention update (R7.c)
- Allowlist update

Reverting one commit does not require touching the others. Validator state returns to pre-commit
baseline because each commit's path references are self-contained. [Judgment call — assumes
sed sweep is exhaustive]

## Verification

Per AC-6 in [prd.md](./prd.md):

```bash
nx run rhino-cli:validate:specs-adoption
nx run rhino-cli:validate:specs-tree
nx run rhino-cli:validate:specs-counts
nx run rhino-cli:validate:specs-links
```

All four must exit 0. If any emits HIGH findings, fix the offending app inside the worktree
before moving to the next phase.

Additionally:

```bash
npm run lint:md
npx nx affected -t typecheck lint test:quick spec-coverage
```

Both must exit 0 before push (pre-push hook also enforces).

## Open Questions

- _Should `apps-labs/README.md` move to a different location or be deleted entirely now that it
  documents itself as empty?_ — `_Unverified — confirm with maintainer at execution start._`
- _Is `libs/hugo-commons` still actively used by any Nx target?_ — `_Unverified — out of scope
for this plan; opened as a follow-up if specs/libs/hugo-commons cross-references break._`
