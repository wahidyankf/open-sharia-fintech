# BRD — Specs Tree Uniformity Pass

## Business Goal

Eliminate every divergence between `specs/` reality and the canonical layout codified in
[Specs Directory Structure Convention](../../../repo-governance/conventions/structure/specs-directory-structure.md)
so that:

1. The four `rhino-cli specs validate-*` Nx targets succeed across the full repo without per-app
   exemptions or `--apps` scoping workarounds. [Repo-grounded — verified in
   [specs-checker.md §Drift Detection](../../../.claude/agents/specs/specs-checker.md), lines 213–229]
2. The root `specs/README.md` is accurate for new contributors and PMs landing on GitHub —
   no documented layout contradicts the on-disk tree.
3. Specs-aware automation (`rhino-cli ddd bc/ul`, `spec-coverage`, pre-push validators)
   treats every in-scope app uniformly.

## Why This Matters

- **Validator gates lie when reality lies.** `validate-tree`, `validate-counts`, `validate-links`,
  and `validate-adoption` already run on every pre-push and PR per
  [specs-directory-structure.md §Pre-push + CI gating surfaces](../../../repo-governance/conventions/structure/specs-directory-structure/pre-push-ci-llm-validation-deterministic-offload-and-related-documentation.md#pre-push--ci-gating-surfaces).
  Apps outside the canonical layout silently slip past these checks because they live outside
  the `AppsWithDDD` allowlist or because the validators recognize "legacy flat" as a permitted
  shape. Either path lets drift accumulate. [Repo-grounded]
- **Discoverability cost.** The current root `specs/README.md` documents a `be/fe/fs/cli` flat
  pattern the repo replaced with the C4-aware five-folder tree. A new contributor reading the
  README and then opening `specs/apps/organiclever/` finds a different structure than promised.
  [Repo-grounded — `specs/README.md` lines 47–73 vs `specs/apps/organiclever/README.md` lines 12–43]
- **Three-Amigos contract.** Specs are the shared language between business, dev, and QA
  ([specs/README.md](../../../specs/README.md) lines 12–18). A non-uniform tree forces every
  reader to learn one layout per app — undermining the shared-language premise.
- **Migration debt compounds.** Each new app authored under the legacy flat layout adds another
  conversion ticket. Cleaning up the existing four cases (crane, rhino, ayokoding/build-tools,
  root README) blocks future drift via the established validator gate. [Judgment call]

## Affected Roles

- **Contributors authoring new feature files** — read root README first; need accurate layout
  documentation.
- **Maintainers running `rhino-cli specs validate-*`** — currently must scope with `--apps` to
  avoid noise from non-canonical trees.
- **PMs and TPMs onboarded to a new app's spec tree** — rely on the five-folder convention
  ([app-readme-vs-specs.md](../../../repo-governance/conventions/structure/app-readme-vs-specs.md))
  for navigation.
- **AI agents (`specs-checker`, `specs-maker`, `specs-fixer`)** — embed structural assumptions
  in their validation categories; divergence either produces false positives or hides real
  issues. [Repo-grounded — `.claude/agents/specs-checker.md` Categories 1, 8, 9]

## Success Metrics

- **`nx run rhino-cli:validate:specs-tree` exits 0 without `--apps` filtering.** This is the
  primary observable: today the default `AppsWithDDD` allowlist excludes `crane`, `rhino`,
  `apps-labs`, and the libs; broadening to "every app under `specs/apps/`" must remain green.
  [Judgment call — depends on allowlist policy decision in `tech-docs.md §Allowlist`]
- **`specs/README.md` references match on-disk structure** — zero broken cross-links from the
  root README into any app spec area (verified via `validate:specs-links`).
- **Zero `Out of scope for this spec tree` legacy-slug warnings** in any app README — every
  per-app README either documents the canonical five-folder tree or explicitly retires the
  legacy slug via a `git mv`. [Repo-grounded — `specs/apps/ayokoding/README.md` lines 45–53
  list `cli/` and `build-tools/` as legacy; `cli/` has already been retired but `build-tools/`
  has not]
- **One commit per app migration.** Per convention §Migration Path, atomic moves are required
  ([specs-directory-structure.md](../../../repo-governance/conventions/structure/specs-directory-structure.md) lines 250–281).
  Tracked as "number of multi-commit migrations: 0". [Judgment call]

## Non-Goals (Business Scope)

- **Authoring net-new Gherkin scenarios.** Coverage gaps in `ose-app` (every BC shows `--`
  counts in `specs/apps/ose-app/README.md`) are a separate authoring concern.
- **Archiving `libs/hugo-commons`.** Hugo agents are deprecated, but determining whether the
  Go shared lib still serves a purpose requires a separate decommissioning review.
- **Renaming `ose-platform` to `ose-web`.** The spec folder name is intentionally decoupled
  from the app slug per
  [specs/apps/ose-platform/README.md](../../../specs/apps/ose-platform/README.md) lines 1–7.
- **Cleaning up `archived/rhino-cli` Go references.** Out of scope; archive layout has its
  own retention rules.

## Business Risks

- **Path-reference sweep miss** during atomic-commit migrations breaks pre-push validators on
  `main` for every contributor. Mitigation: convention §Migration Path mandates updating "ALL
  path references in the same commit" — adhered to literally per app.
- **Allowlist broadening surfaces latent failures.** Adding `ose-app` to `AppsWithDDD` may
  expose previously masked findings in its DDD registry. Mitigation: validator runs are part
  of the plan's quality gate — surfacing latent failures is a feature, not a regression.
  [Judgment call]
- **Convention drift during execution.** Convention may be amended between authoring and
  execution. Mitigation: re-read both conventions at execution start (delivery.md Step 0).

## Out-of-Repo Dependencies

None. All migrations are local file moves and README rewrites within `ose-public`.
