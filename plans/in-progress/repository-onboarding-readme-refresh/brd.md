# 🧭 Business Requirements: README and Onboarding Refresh

## Business Goal

Make `ose-public` understandable and runnable without requiring a new reader to reverse-engineer its
structure, reconcile contradictory documents, or already know Nx, polyglot toolchains, or repository
governance.

The program should help two kinds of reader reach a confident next step:

- A product person can understand the mission, product map, repository role, and sources of product
  truth without starting with build tooling.
- An early-level engineer can set up a clean checkout, run a representative product surface, and
  find the safe workflow for a small change.

## Current-State Evidence

Counts below were read-only verified on 2026-08-20 and are snapshots, not permanent collection
sizes. The defect findings come from a 2026-08-06 documentation audit; some may already be resolved.
**Phase 1 re-verifies every finding against the recorded `origin/main` revision before it justifies
an edit.** A finding that no longer reproduces is recorded as `verified-unchanged`, not rewritten to
create work.

| Finding                                                | Evidence                                                                                                                                                                    | Business impact                                                                                                    |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| The corpus is too large for an implicit sweep.         | [Repo-grounded] `git ls-files 'README.md' '**/README.md'` returned 1,004 files and `git ls-files '*.md'` returned 9,294 on 2026-08-20.                                      | A vague “update all READMEs” instruction would rewrite history, miss generated boundaries, or create review noise. |
| Onboarding routes dead-end.                            | [Audit 2026-08-06] `docs/README.md` pointed newcomers to `docs/tutorials/README.md`, which said the tutorials had moved away.                                               | Readers cannot complete a repository-specific learning journey.                                                    |
| Contribution guidance contradicts repository policy.   | [Audit 2026-08-06] Root READMEs closed or restricted external contributions while `CONTRIBUTING.md` described ordinary public contribution and stale direct-`main` flows.   | Readers receive incompatible expectations and unsafe workflow advice.                                              |
| Setup guidance has drifted from executable truth.      | [Audit 2026-08-06] Setup docs duplicated stale versions, contained mismatched clone directories, and advertised commands or languages that no longer matched configuration. | Early engineers fail before reaching a useful product outcome.                                                     |
| Nx examples cannot be trusted without live resolution. | [Audit 2026-08-06] Active docs named a nonexistent `specs:coverage` target while resolved projects used names such as `test:specs` and `specs:behavior:coverage`.           | Readers waste effort debugging documentation rather than learning the repository.                                  |
| Product navigation exists but is poorly routed.        | [Audit 2026-08-06] Product maps live in `roadmap.md` and `specs/`, while root onboarding foregrounded tooling with no explicit product-person path.                         | Product readers struggle to locate intent, status, and product truth.                                              |
| The voice is repetitive.                               | [Audit 2026-08-06] Repeated stock openings and frequent generic words such as “comprehensive” across living READMEs.                                                        | The documentation feels generated and makes distinct directories sound interchangeable.                            |

## Business Impact

The refresh turns repository documentation from a collection readers must reconcile into a guided
product surface with evidence-backed setup paths. The outcomes below describe business value without
inventing time-saved or conversion metrics the repository does not measure.

### Outcome 1: Faster orientation without time promises

“Quick” means the reader follows the shortest verified path with no contradictory branch, not that
the docs promise a duration. The product path reaches a clear product and repository map. The
engineering path reaches a visible local result.

### Outcome 2: One fact, one accountable source

Versions come from package manifests, project commands come from resolved Nx configuration, ports
come from project targets, repository relationships come from canonical ecosystem governance, and
behavior/architecture details stay in specifications rather than drifting across READMEs.

### Outcome 3: Honest repository positioning

`ose-public` explains its own job — build and research trustworthy, Sharia-compliant enterprise
products — and describes its sibling repositories accurately without claiming work in them.

### Outcome 4: Maintainable documentation rather than a one-time rewrite

The disposition ledger, source-of-truth matrix, command validation, README checker cycle, and
persona walkthroughs create a repeatable maintenance method. A file that is already good records
`verified-unchanged`; the program never manufactures an edit to prove activity.

## Affected Roles

- **Product reader** — needs mission, product map, maturity, terms, and a clear next document.
- **Early-level engineer** — needs prerequisites, expected outcomes, recovery guidance, and a safe
  first local run.
- **Authorized maintainer or invited contributor** — needs the actual worktree-to-PR workflow and
  exact quality gates without being mistaken for an open contribution invitation.
- **Documentation executor** — needs an exact corpus ledger, file ownership, commands, and
  acceptance criteria rather than “update related docs.”

## Business-Level Success Measures

- [Observable fact] Every tracked README appears exactly once in the disposition ledger and has a
  terminal disposition.
- [Observable fact] No living onboarding surface contains a command whose project, target, path, or
  flag fails its stated validation recipe.
- [Observable fact] The product walkthrough and the engineering walkthrough each reach their named
  outcome from a clean checkout on macOS and on Ubuntu.
- [Observable fact] A repository-wide search finds zero conflicting current statements about content
  parity, the `rhino-cli` byte-identity set, contribution status, supported operating systems, or
  delivery mode.
- [Observable fact] Secret scanners and an independent AI sensitivity review find no real secret
  copied into plan files, docs, evidence, commit messages, or GitHub metadata.
- [Observable fact] The GitHub About panel displays the approved description, homepage, and safe
  topic set after execution.
- [Observable fact] `git diff --stat` for every delivery unit shows zero changed paths inside
  `apps/rhino-cli/` or `specs/apps/rhino/behavior/rhino-cli/`.
- [Judgment call] Product readers and early-level engineers describe the prose as welcoming and
  natural in independent read-throughs; no numeric readability KPI is fabricated.

## Business Non-Goals

- Opening contribution intake to the public.
- Marketing launch, search-engine campaign, or social-media copy.
- Changing product behavior, UI design, APIs, or production infrastructure.
- Delivering documentation, metadata, or code into any sibling repository.
- Treating WSL2 as a supported platform before it receives its own verified plan.

## Business Risks and Mitigations

| Risk                                                               | Mitigation                                                                                                                |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| A large program becomes a mega-PR.                                 | Use a DAG with one branch and PR per independently shippable delivery unit.                                               |
| A thousand READMEs encourage mechanical templating.                | Require a disposition ledger, file-specific reader purpose, varied openings, and independent read-aloud review.           |
| A stale audit finding drives an unnecessary rewrite.               | Re-verify every finding against current `origin/main` in Phase 1; a non-reproducing finding becomes `verified-unchanged`. |
| A documentation edit opens a cross-repository byte-identity chore. | Treat `apps/rhino-cli/` and its bound Gherkin as out of scope and assert a zero-diff check at every delivery boundary.    |
| Setup docs pass lint but fail for newcomers.                       | Execute fresh-checkout journeys on macOS and Ubuntu and verify visible behavior.                                          |
| Metadata drifts from the repository's actual positioning.          | Apply exact contract values, then read them back and compare for equality.                                                |
| “Helpful” contribution prose reopens external intake accidentally. | Keep the closed policy explicit and test all contribution entry points as one acceptance scenario.                        |
| A prose sweep erases repository character.                         | Edit by reader purpose, require file-specific rationale, and run a distinct AI read-aloud review.                         |
