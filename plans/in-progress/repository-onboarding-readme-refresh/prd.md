# 📚 Product Requirements: Reader Journeys and Documentation Experience

> **Scope Amendment (2026-08-16)** — `ose-primer` left this repository's parity set and carries no
> sync obligation; see
> [Related Repositories §Repositories outside the parity set](../../../docs/reference/related-repositories.md#repositories-outside-the-parity-set).
> Its already-merged units stay as historical record; every unexecuted `ose-primer` unit is
> **descoped**, not deferred. References to `ose-primer` below are historical context, not
> outstanding scope. See `delivery.md` §Scope Amendment for the item-level disposition.

## Product Overview

This program produces three repository experiences that feel related but never interchangeable. A
shared product-first orientation explains why the ecosystem exists. Each repository then guides its
actual audience toward the next useful outcome with short, trustworthy navigation and a dedicated
guided onboarding document.

The documentation itself is the product surface in this plan. Success means a reader can choose a
path, follow commands with stated outcomes, understand failures, and return to a stable reference
without encountering contradictory claims.

## Personas

### 🧭 Product person

Understands enterprise products and business problems but may not know Nx, Rust, F#, monorepos,
Gherkin, or repository governance. Wants the mission, product map, maturity, repository roles, and
where product decisions live.

### 🧰 Early-level engineer

Can use a terminal and Git but needs prerequisites explained, commands prefixed correctly, expected
outcomes stated, and recovery steps near the failure they address.

### 🏗️ Primer adopter

Wants a reusable repository foundation, not a copy of OSE product-specific applications. Needs a
clear template-versus-product boundary and a representative starter application.

### 🔐 Authorized private maintainer

Needs to understand CoralPolyp and the private repository's role, run a local sandbox with
non-secret placeholders, and find the separate operator path without seeing or copying protected
production details.

### 🔄 Returning maintainer

Already knows the repository and wants a short route to exact project commands, quality gates,
architecture, plans, and source-of-truth references.

## Reader Journey Contract

### Shared opening

Every root README must answer, in this order:

1. What problem does this repository help solve?
2. Who is it for?
3. How does it differ from its sibling repositories?
4. What is its maturity and contribution posture?
5. Which reader path should I choose?

### `ose-public` paths

- **🧭 Understand the product** — mission → product/repository map → roadmap/specifications → next
  product document.
- **🧰 Run OSE locally** — supported platform → prerequisites → clone/bootstrap → project discovery →
  visible first run → optional authorized-contributor workflow.

### `ose-primer` paths

- **🧭 Understand the starter** — starter purpose → template/product boundary → reusable parts →
  reference architecture.
- **🧰 Run a reference app** — supported platform → prerequisites → clone/bootstrap → project
  discovery → visible reference-app run → adoption next steps.

### Private-repository paths

- **🧭 Understand CoralPolyp** — safe purpose statement → CoralPolyp overview → repository
  map → internal product specifications.
- **🧰 Run the local sandbox** — authorization note → safe prerequisites → local CoralPolyp sandbox →
  internal worktree-to-PR workflow for authorized maintainers.
- **🛠️ Operate infrastructure** — separate authorized route with non-destructive validation first;
  never part of the newcomer first-success path.

## Human Voice Contract

Every changed reader-facing document must satisfy all of these requirements:

- Lead with the reader's purpose or problem, not “This directory contains…”.
- Write in active voice and use second person where it sounds natural.
- Explain Nx, monorepo, Gherkin, BDD, TDD, and other niche terms on first use for the intended
  audience.
- Prefer concrete verbs and outcomes over claims such as “comprehensive,” “robust,” “seamless,” or
  “powerful.”
- Keep paragraphs short and vary sentence openings; do not stamp every README from one template.
- Use contractions when they make the sentence sound natural.
- Never use “just,” “simply,” or “obviously” to minimize a reader's difficulty.
- Place the expected outcome immediately after a command and the recovery route immediately after a
  likely failure.
- Use emojis only as supplementary wayfinding; pair every emoji with a text label.
- Keep READMEs as maps. Move lengthy procedures to tutorials/how-to guides and facts to reference
  docs.
- End each entry point with a clear next step, not a generic pile of links.
- Run an independent read-aloud/editorial pass that checks for repetitive cadence, stock filler,
  and text that sounds machine-assembled.

## README Disposition Contract

Every tracked README receives exactly one of these outcomes in its repository ledger:

| Disposition          | Meaning                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `rewrite`            | The document's purpose or structure no longer serves its reader.                                                                           |
| `targeted-fix`       | A bounded factual, command, link, tone, or navigation defect requires an edit.                                                             |
| `link-only`          | The README should stay short and route detail to a canonical document.                                                                     |
| `verified-unchanged` | It already meets the reader, fact, link, and voice checks.                                                                                 |
| `generated`          | A canonical source owns it; regenerate and validate instead of hand-editing.                                                               |
| `historical-exempt`  | It records completed work or archived material and remains untouched.                                                                      |
| `not-reader-doc`     | A non-README Markdown file is inventoried but is not living repository-facing documentation.                                               |
| `follow-up-required` | A blocking non-terminal state: the defect needs a separately scoped code, infrastructure, or governance change before this plan can close. |

No in-scope file may be absent from its owning repository's ledger. No file may receive two terminal
dispositions, and no `follow-up-required` state may remain at archival. The path-complete
`ose-private` ledger remains in private local execution storage;
the public plan receives only a repository revision, validation result, and opaque digest.

## GitHub About Metadata Contract

The values below are the exact all-AI mutation contract. Topic arrays are lowercase GitHub slugs;
execution may not improvise new wording or topics.

| Repository    | Exact description                                                                                    | Exact homepage             | Exact topic set                                                                                                                      |
| ------------- | ---------------------------------------------------------------------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `ose-public`  | Open source platform for researching and building trustworthy, Sharia-compliant enterprise products. | `https://oseplatform.com/` | `enterprise-software`, `erp`, `fsharp`, `islamic-finance`, `monorepo`, `nx`, `open-source`, `rust`, `sharia-compliant`, `typescript` |
| `ose-primer`  | A polyglot Nx starter with OSE governance, testing, automation, and reference apps already wired.    | `https://oseplatform.com/` | `automation`, `bdd`, `fsharp`, `nx`, `nx-monorepo`, `polyglot`, `repository-template`, `rust`, `tdd`, `testing`, `typescript`        |
| `ose-private` | Private product operations and infrastructure for authorized Open Sharia Enterprise maintainers.     | `https://oseplatform.com/` | `automation`, `infrastructure`, `nx`, `open-sharia-enterprise`, `private-repository`, `product-operations`, `rust`, `typescript`     |

Before mutation, the executor captures `gh repo view --json` output with sensitive fields excluded.
After mutation, the executor reads the same fields back and verifies exact intent.

## Package Metadata Contract

Each root `package.json` uses the exact description from its repository's GitHub About contract.
The executor applies the value through a repository-authoritative JSON update command, runs
formatting, and verifies exact equality with `jq -r '.description' package.json`.

## Product Scope

### In scope

- Reader routing, onboarding tutorials, living READMEs, and directly related current docs in all
  both parity repositories.
- Evidence-based disposition of every tracked README without forcing cosmetic edits.
- macOS and Ubuntu fresh-checkout journeys, with WSL2 described only as a possible unverified path.
- Complete GitHub About metadata for both parity repositories.
- Secret-safe public summaries of private delivery evidence.

### Out of scope

- Product behavior, UI, API, or infrastructure changes made only to make a tutorial pass.
- Public contribution intake or community-response commitments.
- Production credentials, production access, deployment, or operator runbooks in newcomer flows.
- Native Windows verification or a WSL2 support guarantee.
- Modernizing immutable historical plans and archived content.

## Product Risks

| Risk                                                             | Product response                                                                                                                |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| One template makes every repository sound interchangeable.       | Preserve the shared journey shape but write repository-specific openings, examples, and next steps.                             |
| A private path or evidence artifact exposes operational context. | Keep path-complete private evidence in `ose-private`; publish only a reviewed revision, result, and opaque digest.              |
| A polished tutorial masks a broken command.                      | Resolve commands from manifests and Nx configuration, then execute clean-checkout journeys on both supported operating systems. |
| Emojis become decoration or replace meaning.                     | Use a small purposeful wayfinding vocabulary and pair every emoji with a text label.                                            |
| Audience paths duplicate durable facts.                          | Keep shared facts in reference docs and let each path link instead of restating them.                                           |
| The private sandbox drifts toward production operations.         | Stop at local health/page proof and route authorized operators separately.                                                      |
| A prose sweep erases repository character.                       | Edit by reader purpose, require file-specific rationale, and run a distinct AI read-aloud review.                               |

## User Stories and Acceptance Criteria

### Story 1: Product orientation

As a product person, I want a plain-language product and repository map so that I can understand the
ecosystem without learning its build system first.

```gherkin
Scenario: Product reader finds the product map
  Given a reader opens an OSE root README without prior Nx knowledge
  When the reader follows the Understand the product path
  Then the reader can explain the repository's purpose and its relationship to the other OSE repositories
  And the reader reaches the current roadmap or product specification without entering setup instructions
```

### Story 2: Public platform first success

As an early-level engineer, I want a verified public-repository walkthrough so that I can see the OSE
website run locally and understand what succeeded.

```gherkin
Scenario: Engineer runs ose-public from a fresh checkout
  Given a supported macOS or Ubuntu environment with the documented prerequisites
  When the engineer follows the ose-public onboarding tutorial from clone through the ose-www development target
  Then the documented page loads at the configured local address without browser console errors
  And every command and expected outcome matches the live repository configuration
```

### Story 3: Primer first success

As a primer adopter, I want a verified starter walkthrough so that I can distinguish reusable
scaffolding from OSE product code and run a reference application.

```gherkin
Scenario: Adopter runs ose-primer from a fresh checkout
  Given a supported macOS or Ubuntu environment and no prior OSE repository knowledge
  When the adopter follows the ose-primer tutorial through the crud-fe-ts-nextjs development target
  Then the reference page loads at the configured local address without browser console errors
  And the tutorial explains which content is reusable scaffolding and which content is only an example
```

### Story 4: Private first success

As an authorized maintainer, I want a secret-free local CoralPolyp walkthrough so that I can verify
the private product surface without production access.

```gherkin
Scenario: Authorized maintainer runs the local CoralPolyp sandbox
  Given an authorized clean checkout with only documented non-secret development placeholders
  When the maintainer starts the local CoralPolyp backend and frontend through verified Nx targets
  Then the backend health behavior and frontend page succeed without a real credential
  And no committed documentation or evidence contains protected topology or secret values
```

### Story 5: Honest contribution posture

As a reader, I want contribution guidance to match repository policy so that I do not prepare a pull
request that the maintainer does not accept.

```gherkin
Scenario: Contribution entry points preserve closed external intake
  Given a reader opens any root README or CONTRIBUTING file in the two-repository delivery
  When the reader looks for contribution instructions
  Then external contributions are clearly described as closed or authorization-only
  And authorized contributors receive the current worktree-to-PR workflow without a response-time promise
```

### Story 6: Exhaustive but low-churn coverage

As a maintainer, I want every README reviewed without forcing cosmetic edits so that the refresh is
complete and reviewable.

```gherkin
Scenario: Every README receives one disposition
  Given the tracked README inventory for each repository is captured from Git
  When the executor completes the repository's disposition ledger
  Then every tracked README path appears exactly once with one allowed terminal disposition
  And the private path-complete ledger remains inside ose-private while public proof stays path-free
```

### Story 7: Executable commands

As an early-level engineer, I want commands tied to live configuration so that documentation does
not teach nonexistent projects, targets, paths, or flags.

```gherkin
Scenario: Documented repository commands resolve
  Given a living reader-facing document contains a shell command
  When the command is checked against its authoritative manifest help output or resolved Nx project configuration
  Then every referenced path project target and flag exists
  And unsafe or state-changing examples are excluded from the newcomer journey
```

### Story 8: Natural writing

As a reader, I want documentation that sounds like a thoughtful teammate so that I can trust it and
keep reading.

```gherkin
Scenario: Changed documentation passes the human voice review
  Given a changed reader-facing document has passed mechanical Markdown checks
  When an independent AI docs reviewer reads it aloud against the human voice contract
  Then the prose is specific welcoming and appropriate to its named audience
  And repetitive stock openings filler claims and template-like cadence are absent
```

### Story 9: Safe cross-repository knowledge

As a maintainer, I want the plan and public docs to remain secret-free so that documentation work
cannot leak private operational information.

```gherkin
Scenario: Cross-repository artifacts preserve sensitivity boundaries
  Given the executor has audited documentation in public and private repositories
  When plan files public docs evidence metadata and learnings are scanned and reviewed by an AI
  Then no real secret credential hostname username IP address connection string or private topology is present
  And private operational knowledge remains only in authorized private-repository documentation
```

### Story 10: Consistent repository relationships

As a reader, I want one accurate ecosystem model so that I can distinguish content parity from
byte identity.

```gherkin
Scenario: Repository relationship claims agree
  Given content parity covers ose-public and ose-private while Rhino byte identity covers both parity repositories
  When the reader compares living relationship documentation across the delivery
  Then each document states the same two boundaries without including beaver-nest in either one
  And repository-specific product content is not described as parity content
```

### Story 11: Complete repository metadata

As a GitHub visitor, I want each About panel to describe its repository accurately so that I can
choose the right starting point before opening a file.

```gherkin
Scenario: GitHub About metadata uses distinct safe positioning
  Given both parity repositories have approved About and package description contracts
  When the metadata changes are applied through the named GitHub and npm commands
  Then each repository displays its own approved purpose and homepage
  And each root package description matches its repository purpose
  And the private repository metadata contains no sensitive operational detail
```

### Story 12: Supported platform honesty

As an engineer, I want platform support stated honestly so that an unverified path is not presented
as guaranteed.

```gherkin
Scenario: Operating-system guidance distinguishes support from possibility
  Given macOS and Ubuntu Linux are the verified onboarding environments
  When a reader reviews platform guidance in any onboarding entry point
  Then macOS and Ubuntu are identified as supported paths
  And WSL2 is labeled as potentially workable but unsupported and unverified
```

## Product Scope Exemptions

- **UI-design funnel**: not applicable; no application screen or shared UI component changes.
- **Application Gherkin/spec binding**: not applicable to documentation-only edits. If execution
  discovers a code bug requiring a fix, that fix moves to a separate plan unless it blocks this
  program; any blocking fix follows the regression-test mandate.
- **Learning syllabus record**: not applicable. The new repository-onboarding documents are bounded
  operational walkthroughs, not a course, curriculum, or reusable learning-path corpus.
- **Rule-15/Rule-16 live product retests**: not triggered by docs-only changes. The explicit browser
  walkthroughs in this plan validate documented first-success behavior instead.
