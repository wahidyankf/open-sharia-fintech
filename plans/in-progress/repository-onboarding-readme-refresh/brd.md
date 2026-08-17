# 🧭 Business Requirements: README and Onboarding Refresh

> **Scope Amendment (2026-08-16)** — `ose-primer` left this repository's parity set and carries no
> sync obligation; see
> [Related Repositories §Repositories outside the parity set](../../../docs/reference/related-repositories.md#repositories-outside-the-parity-set).
> Its already-merged units stay as historical record; every unexecuted `ose-primer` unit is
> **descoped**, not deferred. References to `ose-primer` below are historical context, not
> outstanding scope. See `delivery.md` §Scope Amendment for the item-level disposition.

## Business Goal

Make the Open Sharia Enterprise repository family understandable and runnable without requiring a
new reader to reverse-engineer its structure, reconcile contradictory documents, or already know Nx,
polyglot toolchains, repository governance, or the boundary between public and private work.

The program should help three kinds of reader reach a confident next step:

- A product person can understand the mission, product map, repository roles, and sources of product
  truth without starting with build tooling.
- An early-level engineer can set up a clean checkout, run a representative product surface, and
  find the safe workflow for a small change.
- An authorized private maintainer can understand and run the local private product surface without
  exposing or requiring production secrets.

## Current-State Evidence

All claims below were read-only verified on 2026-08-06. Counts are snapshots, not permanent
collection sizes.

| Finding                                                    | Evidence                                                                                                                                                                   | Business impact                                                                                                    |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| The corpus is too large for an implicit sweep.             | [Repo-grounded] `git ls-files 'README.md' '**/README.md'` returned 524 files in `ose-public` and 233 in `ose-primer`; the private count remains private.                   | A vague “update all READMEs” instruction would rewrite history, miss generated boundaries, or create review noise. |
| Public onboarding dead-ends.                               | [Repo-grounded] `docs/README.md` points newcomers to `docs/tutorials/README.md`, which says the tutorials moved away.                                                      | Readers cannot complete a repository-specific learning journey.                                                    |
| Contribution guidance contradicts repository policy.       | [Repo-grounded] Root READMEs close or restrict external contributions while `CONTRIBUTING.md` files describe ordinary public contribution and stale direct-`main` flows.   | Readers receive incompatible expectations and unsafe workflow advice.                                              |
| Setup guidance has drifted from executable truth.          | [Repo-grounded] Setup docs duplicate stale versions, contain mismatched clone directories, and advertise commands or languages that no longer match project configuration. | Early engineers fail before reaching a useful product outcome.                                                     |
| Nx examples cannot be trusted without live resolution.     | [Repo-grounded] Active docs name a nonexistent `specs:coverage` target, while resolved project targets use names such as `test:specs` and `specs:behavior:coverage`.       | Readers waste effort debugging documentation rather than learning the repository.                                  |
| Product navigation exists but is poorly routed.            | [Repo-grounded] Product maps live in `roadmap.md` and `specs/**`, while root onboarding foregrounds tooling and does not provide an explicit product-person path.          | Product readers struggle to locate intent, status, and product truth.                                              |
| The private repository describes removed showcase content. | [Repo-grounded] Its root and architecture documents still describe removed polyglot demos and an old infrastructure-only identity.                                         | Authorized collaborators form the wrong mental model of the private product surface.                               |
| The voice is repetitive.                                   | [Repo-grounded] The audit found repeated stock openings and frequent generic words such as “comprehensive” across living READMEs.                                          | The documentation feels generated and makes distinct directories sound interchangeable.                            |
| GitHub metadata is uneven.                                 | [Repo-grounded] All three About panels need coordinated positioning; `ose-private` currently has no description, homepage, or topics.                                      | Repository purpose is unclear before a reader opens any file.                                                      |

## Business Impact

The refresh turns repository documentation from a collection readers must reconcile into a guided
product surface with evidence-backed setup paths. The outcomes below describe the business value
without inventing time-saved or conversion metrics that the repositories do not measure.

### Outcome 1: Faster orientation without time promises

“Quick” means the reader follows the shortest verified path with no contradictory branch, not that
the docs promise a duration. The product path reaches a clear product/repository map. The engineering
path reaches a visible local result. The private path reaches a safe local result without real
credentials.

### Outcome 2: One fact, one accountable source

Versions come from package manifests, project commands come from resolved Nx configuration, ports
come from project targets, repository relationships come from canonical ecosystem governance, and
behavior/architecture details stay in specifications rather than drifting across READMEs.

### Outcome 3: Honest repository positioning

Each repository explains its own job:

- `ose-public`: build and research trustworthy, Sharia-compliant enterprise products.
- `ose-primer`: start a new product repository with proven OSE scaffolding and reference apps.
- `ose-private`: support authorized private product operations and infrastructure without disclosing
  protected implementation details.

### Outcome 4: Maintainable documentation rather than a one-time rewrite

The disposition ledgers, source-of-truth matrix, command validation, README checker cycle, and
persona walkthroughs create a repeatable maintenance method. A file that is already good records
`verified-unchanged`; the program never manufactures an edit to prove activity.

## Affected Roles

- **Product reader** — needs mission, product map, maturity, terms, and a clear next document.
- **Early-level engineer** — needs prerequisites, expected outcomes, recovery guidance, and a safe
  first local run.
- **Authorized maintainer or invited contributor** — needs the actual worktree-to-PR workflow and
  exact quality gates without being mistaken for an open contribution invitation.
- **Primer adopter** — needs to understand template versus product, then run a representative
  starter application.
- **Private operator** — needs a separate, access-aware route that keeps production operations and
  real secrets outside the newcomer journey.
- **Documentation executor** — needs an exact corpus ledger, file ownership, commands, and acceptance
  criteria rather than “update related docs.”

## Business-Level Success Measures

- [Observable fact] Every tracked README appears exactly once in its owning repository's disposition
  ledger and has a terminal disposition; the path-complete private ledger stays inside
  `ose-private`, while the public plan retains only a revision, validation result, and opaque digest.
- [Observable fact] No living onboarding surface contains a command whose project, target, path, or
  flag fails its stated validation recipe.
- [Observable fact] The product, engineering, primer-adopter, and private-maintainer walkthroughs
  each reach their named outcome from a clean checkout.
- [Observable fact] A cross-repository search finds zero conflicting current statements about
  content parity, the `rhino-cli` byte-identity set, contribution status, supported operating
  systems, or delivery mode.
- [Observable fact] Secret scanners and an independent AI sensitivity review find no real secret or
  protected private topology copied into plan files, public docs, evidence, commit messages, or
  GitHub metadata.
- [Observable fact] Each repository's GitHub About panel displays its approved description,
  homepage, and safe topic set after execution.
- [Judgment call] Product readers and early-level engineers describe the prose as welcoming and
  natural in independent read-throughs; no numeric readability KPI is fabricated.

## Business Non-Goals

- Opening contribution intake to the public.
- Marketing launch, search-engine campaign, or social-media copy.
- Changing product behavior, UI design, APIs, or production infrastructure.
- Making both parity repositories sound identical.
- Publishing private operational knowledge into either public repository.
- Treating WSL2 as a supported platform before it receives its own verified plan.

## Business Risks and Mitigations

| Risk                                                               | Mitigation                                                                                                                   |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| A megaplan becomes a mega-PR.                                      | Use a DAG with one worktree/branch/PR per independently shippable repository and document family.                            |
| Hundreds of READMEs encourage mechanical templating.               | Require a disposition ledger, file-specific reader purpose, varied openings, and independent read-aloud review.              |
| Public and private facts cross the wrong boundary.                 | Apply the secret/sensitivity gate before writing, before committing, before metadata mutation, and during knowledge capture. |
| Shared Rhino files drift across repositories.                      | Serialize their delivery and prove byte identity after every relevant merge.                                                 |
| Setup docs pass lint but fail for newcomers.                       | Execute fresh-checkout journeys on macOS and Ubuntu and verify visible behavior.                                             |
| Metadata exposes private details.                                  | Use only purpose-level language and safe topics; prohibit topology, vendor account, host, credential, and access details.    |
| “Helpful” contribution prose reopens external intake accidentally. | Keep the closed policy explicit and test all contribution entry points as one acceptance scenario.                           |
