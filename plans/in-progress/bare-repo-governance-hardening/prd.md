# Product Requirements — Bare-Repo Governance Hardening

## Product Overview

This plan ships **governance documentation only**. Its product is a set of seven coordinated
documentation changes (C1-C7) landed in `ose-public` and then propagated verbatim to `ose-primer`
and `ose-infra`.

The deliverable a reader can point at is one new document —
`repo-governance/development/workflow/bare-repo-landing-method.md` — plus six edits that make the
surrounding governance corpus consistent with it.

## Personas

Solo-maintainer repository: personas are hats the maintainer wears and the agents that read these
files.

| Persona                      | Reads / uses                                                 | Needs                                                                          |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **Parity Maintainer**        | C1 (the method), C2 (the safety cross-link)                  | An ordered, followable procedure that ends with local `main` reconciled        |
| **Cross-Repo Scoping Agent** | C1 (bareness check), C6 (`sdlc-gate-standard.md` refinement) | The right question to ask about topology, and an explicit ban on the wrong one |
| **Parity-Planning Workflow** | C3 (Delivery Mode table), C4 (grill question)                | A mode table and a grill question that agree with each other and with reality  |
| **Idea-Promotion Workflow**  | C6 (re-pointed cross-link)                                   | A "bare-repo git-ops method" link that resolves to a real method               |
| **PR-Merging Agent**         | C5 (saturation qualifier)                                    | To read "default 3" at the enumeration site without inferring a ceiling        |
| **Plan Checker**             | C3, C4                                                       | Mode-validity rules that do not contradict the workflow docs                   |

## User Stories

**US-1** — As a **Parity Maintainer**, I want the base-worktree landing method written down as an
ordered procedure, so that I stop reconstructing it from memory each parity cycle.

**US-2** — As a **Parity Maintainer**, I want the method's **last step** to reconcile local `main`
with `origin/main`, so that a bare sibling never silently accumulates a behind-count.

**US-3** — As a **Parity Maintainer**, I want the method to state the reconcile command **keyed by
repository topology**, so that I do not run a work-tree-requiring command in a repo that has no work
tree.

**US-4** — As a **Parity Maintainer**, I want an explicit rule that work lands **either** through
the worktree **or** through an already-reconciled local `main` but never both, so that no duplicate
stale-base commit creates an ahead-count.

**US-5** — As a **Parity Maintainer**, I want advisory guidance on parking long-lived WIP off the
shared index, so that `git status` reflects genuinely-active work — without any tool trying to
decide on my behalf what is stale.

**US-6** — As a **Cross-Repo Scoping Agent**, I want a prescribed bareness-verification method and
an explicit prohibition on `git rev-parse --is-bare-repository`, so that I never mistake a linked
worktree's correct `false` for a statement about the repository.

**US-7** — As a **Parity-Planning Workflow**, I want the Delivery Mode table to state that
`main-to-*` modes are unavailable in a bare repo, so that I never offer a mode the target cannot
execute.

**US-8** — As a **Parity-Planning Workflow**, I want my bare-repo grill question bound to the
**property** "bare repository with no primary checkout" rather than to the **name** `ose-primer`, so
that it also fires for `ose-infra`.

**US-9** — As a **PR-Merging Agent**, I want the floor-not-ceiling qualifier inline at both
`pr-merge-protocol.md` enumeration sites, so that "default 3" does not read as a sufficient stopping
condition.

**US-10** — As an **Idea-Promotion Workflow**, I want the "bare-repo git-ops method" cross-link to
resolve to a document that defines the method, so that following it answers the question it
promises to answer.

**US-11** — As a **Maintainer**, I want both source two-pagers deleted and de-indexed in the same
changeset that introduces this plan, so that no promoted idea lingers in two lifecycle stages at
once.

**US-12** — As a **Maintainer**, I want all seven changes propagated to both siblings **inside this
plan**, so that the three repos do not drift on the very rules that govern cross-repo work.

## Acceptance Criteria

Every scenario below is falsifiable in **both** directions: the stated command produces a different,
named result before the change than after it. Literal strings containing backticks or punctuation
are matched with `grep -F`.

> **Verification note (verified empirically 2026-07-21)** — in this repo `grep` routes to **ugrep**,
> not ripgrep. `-c` prints `0` and **exits 1** when a pattern has zero matches; scenarios state that
> exit code explicitly where it is the pre-change result. `-L` means _files-without-match_ here and
> **exits 0** when it finds one, so a `-L` clause reads as passing almost unconditionally — **no
> scenario below uses `-L`**. Ripgrep's `--glob '!…'` is unavailable; use `--exclude-dir`. See the
> fuller caveat in [delivery.md](./delivery.md).

### C1 — The landing method exists as a document

```gherkin
Scenario: The bare-repo landing method is a real governance document
  Given the repository has no file at repo-governance/development/workflow/bare-repo-landing-method.md
  When the C1 authoring step completes
  Then `test -f repo-governance/development/workflow/bare-repo-landing-method.md` exits 0
  And `grep -Fc "git worktree add" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1
  And `grep -Fc "HEAD:main" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1
  But the same test command exits 1 before the step, because the file does not exist
```

### C1 — The terminal reconcile step is topology-keyed

```gherkin
Scenario: The method prescribes both reconcile forms, keyed by topology
  Given no file in repo-governance/ contains the string "fetch origin main:main"
  When the C1 authoring step completes
  Then `grep -Fc "git fetch origin main:main" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1
  And `grep -Fc "merge --ff-only origin/main" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1
  And the document states which form applies to a bare repo and which applies to a repo with a work tree
  But `grep -rFc "git fetch origin main:main" repo-governance/` exits 1 before the step
```

### C1 — The no-double-landing rule is stated

```gherkin
Scenario: The method forbids landing through both the worktree and local main
  Given the base-worktree method is undocumented and states no landing-path exclusivity rule
  When the C1 authoring step completes
  Then repo-governance/development/workflow/bare-repo-landing-method.md contains a rule naming the worktree path and the reconciled-local-main path as mutually exclusive for one unit of work
  And the rule names the duplicate stale-base commit as the failure it prevents
```

### C1 — The WIP-parking rule is advisory and tool-free

```gherkin
Scenario: The WIP-parking rule is advisory prose with no automated gate
  Given DD-2 forbids proposing a checker for long-lived staged WIP
  When the C1 authoring step completes
  Then repo-governance/development/workflow/bare-repo-landing-method.md recommends an ordinary refs/heads/wip/* branch for long-lived WIP
  And it states that no tool can distinguish recently-staged from long-staged content
  And it states that staged blobs survive a hard reset as dangling objects within gc.pruneExpire's default window
  But it prescribes no checker, hook, or rhino-cli subcommand for the rule
```

### C1 + C6 — Bareness verification is prescribed and the trap is forbidden

```gherkin
Scenario: Both bareness checks are prescribed with provenance labels
  Given no file under repo-governance/ or docs/ mentions core.bare
  When the C1 and C6 steps complete
  Then `grep -Fc "git worktree list" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1
  And `grep -Fc "core.bare" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1
  And the core.bare form is labelled as derived from documented mechanics rather than upstream-prescribed
  And `grep -Fc "is-bare-repository" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1 in a prohibiting sentence
  But `grep -rFc "core.bare" repo-governance/ docs/` exits 1 before the steps
```

```gherkin
Scenario: The prohibition is framed as scoping semantics, not as a git defect
  Given F3 establishes that --is-bare-repository returning false from a linked worktree is documented, intentional behaviour
  When the C1 and C6 steps complete
  Then the prohibiting sentence attributes the false result to per-worktree scoping rather than to a git bug
  And it cites git-worktree(1)'s CONFIGURATION FILE section as the source of the scoping rule
  But no sentence in the changeset calls the behaviour a bug, a defect, or broken
```

### C2 — The safety convention links to the method

```gherkin
Scenario: no-destructive-git-operations.md points at the new method document
  Given `grep -Fc "bare-repo-landing-method" repo-governance/development/workflow/no-destructive-git-operations.md` exits 1
  When the C2 step completes
  Then `grep -Fc "bare-repo-landing-method.md" repo-governance/development/workflow/no-destructive-git-operations.md` prints at least 1
  And `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md links validate --exclude plans/done --exclude apps/ayokoding-www/content --exclude apps/ose-www/content` reports no broken link for that target
```

### C3 — The Delivery Mode table states the bare-repo restriction

```gherkin
Scenario: The Delivery Mode table names the bare-repo restriction on main-to-* modes
  Given `grep -Fc "bare repo" repo-governance/conventions/structure/plans.md` exits 1
  When the C3 step completes
  Then `grep -Fc "bare repo" repo-governance/conventions/structure/plans.md` prints at least 1
  And the restriction sits adjacent to the four-mode table rather than in an unrelated section
  And it states that a bare repository has no primary checkout and therefore cannot use main-to-origin-main or main-to-pr
```

### C4 — The bare-repo grill question is property-bound

```gherkin
Scenario: The parity-planning grill question binds to the bare property, not the repo name
  Given `grep -Fc "any bare repo" repo-governance/workflows/plan/plan-multi-repo-parity-planning.md` exits 1
  When the C4 step completes
  Then `grep -Fc "any bare repo" repo-governance/workflows/plan/plan-multi-repo-parity-planning.md` prints at least 1
  And the question text no longer scopes the bare-repo condition to ose-primer by name alone
  And the question's option list no longer offers main-to-origin-main for a bare target
```

```gherkin
Scenario: The workflow no longer contradicts its own bare-repo note
  Given the workflow states at one point that a bare repo cannot use main-to-* modes while offering main-to-origin-main at another
  When the C4 step completes
  Then every delivery-mode option list in that workflow that applies to a bare target omits both main-to-* modes
  And the surviving note and the option lists make the same claim
```

### C5 — The saturation qualifier is inline at both enumeration sites

```gherkin
Scenario: pr-merge-protocol.md carries the floor-not-ceiling qualifier at both (a) sites
  Given `grep -Fc "floor" repo-governance/development/workflow/pr-merge-protocol.md` exits 1
  When the C5 step completes
  Then `grep -Fc "floor" repo-governance/development/workflow/pr-merge-protocol.md` prints exactly 2
  And each occurrence sits in the precondition-(a) sentence of its own enumeration
  And each occurrence cross-links the pr-review-quality-gate.md saturation section
```

### C6 — The dangling cross-link resolves

```gherkin
Scenario: The bare-repo git-ops method link points at a document defining the method
  Given plan-idea-promotion-planning.md links the phrase "bare-repo git-ops method" to no-destructive-git-operations.md, which defines no such method
  When the C6 step completes
  Then `grep -Fc "bare-repo-landing-method.md" repo-governance/workflows/plan/plan-idea-promotion-planning.md` prints at least 1
  And `grep -Fc "bare-repo git-ops method" repo-governance/development/workflow/bare-repo-landing-method.md` prints at least 1
  But `grep -Fc "bare-repo git-ops method" repo-governance/development/workflow/no-destructive-git-operations.md` exits 1 both before and after, confirming the phrase was never defined there
```

### C7 — Both two-pagers are retired atomically

```gherkin
Scenario: Promotion retires both source briefs in the same changeset
  Given plans/ideas/bare-repo-worktree-landing-hygiene.md and plans/ideas/bare-repo-delivery-mode-governance-hardening.md both exist
  When the C7 step completes
  Then `test -f plans/ideas/bare-repo-worktree-landing-hygiene.md` exits 1
  And `test -f plans/ideas/bare-repo-delivery-mode-governance-hardening.md` exits 1
  And `grep -Fc "bare-repo-worktree-landing-hygiene" plans/ideas/README.md` exits 1
  And `grep -Fc "bare-repo-delivery-mode-governance-hardening" plans/ideas/README.md` exits 1
  But both test commands exit 0 before the step
```

```gherkin
Scenario: The siblings need no brief deletion
  Given neither brief slug appears anywhere in ose-primer or ose-infra
  When the sibling propagation phases run
  Then no deletion step for either brief appears in the ose-primer or ose-infra phases
  And tech-docs.md records the zero-hit search as a verified fact so a later reader does not re-check
```

### Propagation — all three repos agree

```gherkin
Scenario: Every repo carries the landing method after propagation
  Given only ose-public has bare-repo-landing-method.md after Phase 3
  When the ose-primer and ose-infra propagation phases complete
  Then each sibling contains repo-governance/development/workflow/bare-repo-landing-method.md
  And each sibling's copy differs from ose-public's only where a repo-specific fact requires it
  And each sibling's index entries in repo-governance/development/README.md and repo-governance/development/workflow/README.md list the new document
```

```gherkin
Scenario: The propagation self-applies the documented method
  Given ose-primer and ose-infra are bare repositories with no primary checkout
  When a sibling propagation phase lands its changeset
  Then the phase performs the base-worktree method exactly as C1 documents it
  And the phase's final step runs the topology-appropriate reconcile
  And `git -C <sibling> rev-list --left-right --count origin/main...main` prints 0 and 0
```

### Quality gates

```gherkin
Scenario: The changeset passes every applicable repo gate
  Given the plan touches only markdown under repo-governance/, docs/, and plans/
  When the local quality gates run
  Then `npx nx affected -t typecheck lint test:quick specs:coverage` exits 0
  And markdown link validation reports zero broken links across the changed files
  And markdownlint reports zero violations across the changed files
  And no Gherkin scenario in this plan uses a repeated primary Given, When, or Then keyword
```

## Product Scope

### In scope

- C1 — a new governance document defining the bare-repo base-worktree landing method end to end,
  including the terminal reconcile, the no-double-landing rule, the advisory WIP-parking rule, and
  the bareness-verification prescription.
- C2 — a cross-link from the No Destructive Git Operations Convention to C1.
- C3 — a bare-repo restriction note adjacent to the Delivery Mode table.
- C4 — a property-bound bare-repo grill question with a corrected option list.
- C5 — the inline floor-not-ceiling qualifier at both `pr-merge-protocol.md` enumeration sites.
- C6 — a refinement of the existing `sdlc-gate-standard.md` worktree-agnostic rule, plus the
  re-pointed `plan-idea-promotion-planning.md` cross-link.
- C7 — deletion of both two-pagers and their index lines.
- Index registration of C1 in `repo-governance/development/README.md` and
  `repo-governance/development/workflow/README.md`.
- Verbatim propagation of all of the above to `ose-primer` and `ose-infra`.

### Out of scope

- Any checker, hook, wrapper script, or `rhino-cli` subcommand — for the lag rule or the WIP rule
  (**DD-2**; git has no `post-push` hook at all).
- Redesigning the base-worktree method.
- Changing what any delivery mode does.
- Adopting any third-party branch-sync tool.
- Migrating a sibling away from the bare layout.
- Any change under `apps/`, `libs/`, or `specs/`.

## Product Risks

| Risk                                                                                     | Impact | Mitigation                                                                                                                       |
| ---------------------------------------------------------------------------------------- | ------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Line-number anchors drift between authoring and execution                                | HIGH   | Every delivery step **re-anchors by content**, never by line number; the known-drifted `plans.md` citation is called out by name |
| An acceptance grep matches zero lines both before and after, making the check vacuous    | HIGH   | Every scenario names its pre-change result explicitly; `grep -F` is used for literals                                            |
| A sibling copy silently diverges from `ose-public`'s wording during propagation          | MEDIUM | Propagation phases diff the sibling copy against `ose-public`'s and justify every intentional difference                         |
| The new document duplicates content already in the cleanup or no-destructive conventions | MEDIUM | C1 owns the **procedure**; the existing conventions keep the **prohibitions** and link across (rationale in `tech-docs.md`)      |
| The advisory WIP rule is read as enforceable and an agent stashes another actor's work   | MEDIUM | C1 states the rule as advisory and explicitly warns that an automated stash of foreign WIP is itself destructive                 |
| `pr-merge-protocol.md` gains a second qualifier location and the two drift apart later   | LOW    | Both occurrences cross-link the single source note in `pr-review-quality-gate.md` rather than restating it independently         |
