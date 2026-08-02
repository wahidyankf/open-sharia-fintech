---
title: "PRD — SDLC Gate Registry Enforcement"
description: Requirements and Gherkin acceptance criteria for the gate registry, surface rewire, and main-ci retirement
category: explanation
subcategory: plans
tags:
  - ci-cd
  - governance
  - requirements
created: 2026-08-02
---

# PRD — SDLC Gate Registry Enforcement

All requirements are numbered `R-n` and referenced by the delivery checklist. Every requirement
carries at least one Gherkin scenario. These scenarios are the source for the companion
`specs/apps/rhino/behavior/rhino-cli/gherkin/**` feature files that ship with Phase 1 — code under
`apps/` never lands without its Gherkin, per
[Feature-Change Completeness](../../../repo-governance/development/quality/feature-change-completeness.md).

## R-1 — A declared gate registry

`repo-config.yml` gains a `gates:` section declaring **everything any surface does** — every
pass/fail check (`type: check`) and every file-rewriting step (`type: mutation`) — each with a stable
`id`, its command, and the scope it carries **per surface**. Scope values are exactly the five
controlled values already ratified in the SDLC Gate Standard, plus the path-gated qualifier. Surfaces
are the four gate surfaces and only those: `commit-msg`, `pre-commit`, `pre-push`, `ci`. Scheduled
non-gating pipelines are outside the registry by design — see R-8.

The completeness property is the point: after this change, anything absent from `gates:` is run by no
surface. There is no third category living in prose.

```gherkin
Feature: Gate registry declaration

  Scenario: A check declares a different scope per surface
    Given repo-config.yml declares a gate "md-links" with command "md links validate"
    And that gate declares surface "pre-push" with scope "all-file-type"
    And that gate declares surface "ci" with scope "all-file-type"
    When "rhino-cli gate list --surface=pre-push --format=json" runs
    Then the output contains an entry with id "md-links"
    And that entry reports scope "all-file-type"

  Scenario: An unknown scope value is rejected at parse time
    Given repo-config.yml declares a gate with scope "sometimes"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the offending gate id and the allowed scope values

  Scenario: A duplicate gate id is rejected
    Given repo-config.yml declares two gates both with id "md-links"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the duplicated id

  Scenario Outline: Every surface step is declared, whatever its type
    Given the surfaces as shipped by this plan
    When "rhino-cli gate list --format=json" runs
    Then the output contains an entry with id "<id>"
    And that entry reports type "<type>"

    Examples:
      | id                        | type     |
      | env-staged-guard          | check    |
      | commitlint                | check    |
      | format-prettier           | mutation |
      | harness-bindings-generate | mutation |
      | lockfile-sync             | mutation |
      | test-quick                | check    |

  Scenario: An unknown type value is rejected at parse time
    Given repo-config.yml declares a gate with type "cleanup"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message names the allowed type values

  Scenario: A mutation may not declare a wiring value
    Given a gate declares type "mutation" and wiring "matrix"
    When "rhino-cli repo-config validate" runs
    Then it exits non-zero
    And the message states that wiring applies to checks only
```

## R-2 — Enumeration for the CI matrix

`gate list` emits a machine-readable surface projection so `pr-quality-gate.yml` can build a job
matrix rather than hand-listing jobs. Parallelism is preserved: one gate, one job.

```gherkin
Feature: Gate enumeration

  Scenario: JSON output drives a GitHub Actions matrix
    Given the registry declares gates on surface "ci"
    When "rhino-cli gate list --surface=ci --format=json" runs
    Then the output is a JSON array
    And every element carries "id", "command", and "scope" keys
    And the array contains exactly the gates declaring surface "ci"

  Scenario: A surface with no declared gates yields an empty array, not an error
    Given no gate declares surface "commit-msg"
    When "rhino-cli gate list --surface=commit-msg --format=json" runs
    Then it exits zero
    And the output is an empty JSON array

  Scenario: An unknown surface name is rejected rather than returning empty
    Given "cron" is not a valid surface name
    When "rhino-cli gate list --surface=cron --format=json" runs
    Then it exits non-zero
    And the message names the four valid surfaces
```

## R-3 — Execution from the hooks

`gate run --surface=<name>` executes every gate declared for that surface, in declaration order,
stopping at the first failure. The hooks become invocation shims with no embedded check list.

```gherkin
Feature: Gate execution

  Scenario: Pre-push runs every gate declared for the pre-push surface
    Given the registry declares gates "md-links" and "env" on surface "pre-push"
    When "rhino-cli gate run --surface=pre-push" runs
    Then both gate commands are invoked
    And they are invoked in declaration order

  Scenario: Execution stops at the first failing gate
    Given the registry declares gates "first" then "second" on surface "pre-push"
    And gate "first" fails
    When "rhino-cli gate run --surface=pre-push" runs
    Then it exits non-zero
    And gate "second" is not invoked

  Scenario: A path-gated check is skipped when its trigger path is untouched
    Given gate "harness-bindings" declares surface "pre-push" with scope "path-gated"
    And its trigger paths do not intersect the changed set
    When "rhino-cli gate run --surface=pre-push" runs
    Then gate "harness-bindings" is not invoked
    And the run exits zero

  Scenario: A path-gated check runs when its trigger path is touched
    Given gate "harness-bindings" declares surface "pre-push" with scope "path-gated"
    And a file under ".claude/agents/" is in the changed set
    When "rhino-cli gate run --surface=pre-push" runs
    Then gate "harness-bindings" is invoked

  Scenario: Execution works identically from a linked worktree
    Given the current tree is a linked worktree under "worktrees/"
    When "rhino-cli gate run --surface=pre-push" runs
    Then repo-config.yml resolves from the current worktree toplevel
    And the run behaves identically to the primary checkout
```

## R-4 — Conformance enforcement (the core requirement)

`gate validate` is the mechanism that makes the Gate Composition Rule unbreakable. It fails when a
surface file does not invoke what the registry declares, when the registry omits a check a surface
actually runs, and when a gate violates the composition rule itself.

```gherkin
Feature: Gate conformance validation

  Scenario: A check declared for pre-commit but not for ci violates the composition rule
    Given a gate declares type "check" and surface "pre-commit"
    And that gate declares no surface "ci"
    And that gate carries no carve-out
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message cites the Gate Composition Rule
    And the message names the gate id and the missing surface

  Scenario: A mutation at pre-commit does not require a ci counterpart
    Given a gate declares type "mutation" and surface "pre-commit"
    And that gate declares no surface "ci"
    When "rhino-cli gate validate" runs
    Then it exits zero

  Scenario: The staged-only carve-out exempts a check that cannot have a CI counterpart
    Given gate "env-staged-guard" declares type "check" and surface "pre-commit" only
    And it carries carve-out "staged-only"
    When "rhino-cli gate validate" runs
    Then it exits zero
    And the exemption is reported in "gate list" output

  Scenario: A surface file that stops invoking the registry is caught
    Given the registry declares gates on surface "pre-push"
    And ".husky/pre-push" does not invoke "gate run --surface=pre-push"
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the surface file

  Scenario: A CI workflow that hardcodes a check instead of deriving it is caught
    Given "pr-quality-gate.yml" runs a check command that no registry gate declares
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the undeclared command

  Scenario: A hand-wired gate is asserted present but not matrix-derived
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    And "pr-quality-gate.yml" contains a job invoking "test:quick"
    When "rhino-cli gate validate" runs
    Then it exits zero

  Scenario: A hand-wired gate whose job was deleted is caught
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    And "pr-quality-gate.yml" contains no job invoking "test:quick"
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names the gate id and the surface file

  Scenario: A hand-wired gate produces no matrix row
    Given gate "test-quick" declares wiring "hand-wired" on surface "ci"
    When "rhino-cli gate list --surface=ci --format=json" runs
    Then the output contains no entry with id "test-quick"

  Scenario: A hand-edited lint-staged block is caught
    Given the "lint-staged" block in package.json differs from what the registry would emit
    When "rhino-cli gate validate" runs
    Then it exits non-zero
    And the message names package.json and instructs to run "gate emit --surface=pre-commit"

  Scenario: The shipped configuration passes
    Given the registry and surfaces as shipped by this plan
    When "rhino-cli gate validate" runs
    Then it exits zero
```

### R-4a — lint-staged is generated from the registry

```gherkin
Feature: Generated lint-staged block

  Scenario: The emitter reproduces the registry's per-file entries
    Given the registry declares per-file gates on surface "pre-commit"
    When "rhino-cli gate emit --surface=pre-commit" runs
    Then the "lint-staged" block in package.json contains one glob key per declared glob
    And each key lists that glob's commands in declaration order

  Scenario: Re-running the emitter is idempotent
    Given "rhino-cli gate emit --surface=pre-commit" has already run
    When it runs a second time
    Then package.json is byte-identical to the first result
    And the block appears exactly once
```

## R-5 — `main-ci.yml` retired without losing checks

Every check that exists **only** in `main-ci.yml` today reaches the PR gate before `main-ci.yml` is
deleted. Deletion follows the fold-in, never precedes it.

```gherkin
Feature: main-ci retirement

  Scenario: Mermaid validation reaches the PR gate before main-ci is deleted
    Given "md mermaid validate" runs only in main-ci.yml
    When the fold-in step completes
    Then "md mermaid validate" is declared on surface "ci"
    And it appears in "gate list --surface=ci --format=json"

  Scenario: Heading-hierarchy validation reaches the PR gate before main-ci is deleted
    Given "md heading-hierarchy validate" runs only in main-ci.yml
    When the fold-in step completes
    Then "md heading-hierarchy validate" is declared on surface "ci"

  Scenario: The specs job stops being pinned to a single project
    Given the PR gate ran "specs:structure-validation" with "--projects=rhino-cli"
    When the rewire completes
    Then the PR gate runs the structural specs validator over the affected project set
    And no surface passes "--projects=rhino-cli" to that target

  Scenario: main-ci.yml is absent and unreferenced
    Given the fold-in is complete
    When the retirement step completes
    Then ".github/workflows/main-ci.yml" does not exist
    And no tracked markdown file references "main-ci"
```

## R-6 — `harness bindings validate` reaches CI

```gherkin
Feature: Binding parity enforced server-side

  Scenario: An unsynced mirror pushed without hooks is caught by CI
    Given a commit changes ".claude/agents/" without regenerating ".opencode/agents/"
    And the commit is pushed with hooks bypassed
    When the PR gate runs
    Then the gate declaring "harness bindings validate" fails
```

## R-7 — Formatting is verified, not silently rewritten

The ratified standard exempts formatters from being _checks_ at pre-commit, where they auto-fix.
This plan expresses that structurally rather than as an exemption: formatters are declared
`type: mutation`, and the composition rule applies only to `type: check`. That exemption does not
justify a `main` branch carrying unformatted files, so a `format-verify` check is added on the CI
surface — an ordinary check, needing no carve-out, since the rule runs pre-commit/pre-push ⇒ ci and
never the reverse.

```gherkin
Feature: Formatting verification

  Scenario: An unformatted file fails the CI surface
    Given a tracked file is not formatted per its language formatter
    And the commit is pushed directly to main with hooks bypassed
    When the PR gate runs on the push event
    Then the formatting verify gate fails
    And the failure names the offending file

  Scenario: Formatters still auto-fix at pre-commit
    Given an unformatted file is staged
    When the pre-commit surface runs
    Then the file is rewritten in place and re-staged
    And the commit is not aborted for formatting alone
```

## R-8 — `deps:audit` excluded from the registry, given its own named workflow

`deps:audit` is **not** a gate and is **not** in `gates:`. It is non-hermetic — it reads a remote
advisory database that moves independently of the code — so a green commit can turn red with no
repository change. Ratified rule 3 already keeps it out of every gate; this plan keeps it out of the
registry too, because a scheduled job that no composition rule governs, that emits no CI matrix row,
and that no hook invokes is not a surface.

It gets visibility the honest way instead: a dedicated workflow whose name says what it does.
`deps-audit.yml` is replaced by `dependency-vulnerability-audit.yml`
(`name: Dependency Vulnerability Audit`) in all four repos. See
[tech-docs §2.2.3](./tech-docs.md#223-what-is-deliberately-outside-the-registry).

```gherkin
Feature: Dependency audit lives outside the gate registry

  Scenario: deps:audit is absent from the registry entirely
    Given the registry as shipped by this plan
    When "rhino-cli gate list --format=json" runs
    Then the output contains no entry with id "deps-audit"
    And the output contains no entry whose command is "deps:audit"

  Scenario: Excluding it does not weaken the completeness claim
    Given the registry declares no gate for "deps:audit"
    When "rhino-cli gate validate" runs
    Then it exits zero
    And no gate surface invokes "deps:audit"

  Scenario: The old workflow is gone and the new one carries a descriptive name
    Given the rename is complete
    Then ".github/workflows/deps-audit.yml" does not exist
    And ".github/workflows/dependency-vulnerability-audit.yml" exists
    And its "name:" field is "Dependency Vulnerability Audit"
    And its schedule and dispatch triggers are unchanged from the workflow it replaces

  Scenario: The new name satisfies the mechanical filename derivation
    Given the workflow "name:" is "Dependency Vulnerability Audit"
    When the naming convention's transformation is applied
    Then the result is "dependency-vulnerability-audit.yml"
    And that matches the filename exactly

  Scenario: One identical name across all four repos
    Given each repo ships the scheduled dependency-audit workflow
    When the "name:" fields are compared across the four repos
    Then they are identical
    And ose-primer no longer ships "Nightly Dependency Audit" inside a file named deps-audit.yml

  Scenario: The naming convention is amended to make the new name legal
    Given "dependency" is not in the cross-cutting domain list
    And "audit" is not in the verb vocabulary
    When the amendment lands
    Then the convention lists both
    And the Cross-cutting workflows table registers the new workflow
    And that table no longer lists main-ci.yml
```

## R-9 — Documentation agrees with the implementation

```gherkin
Feature: Standard and implementation agree

  Scenario: The Gate Composition Rule reflects the retired main gate
    Given main-ci.yml is deleted
    When the SDLC Gate Standard is read
    Then the composition rule reads "(pre-commit ∪ pre-push) == PR gate"
    And the lifecycle stage table lists no main quality gate stage

  Scenario: The stale hook-lifecycle doc is corrected
    Given git-hook-lifecycle.md described a pre-push that no longer exists
    When the rewrite completes
    Then it names no target that does not exist
    And it names no workflow file that does not exist
    And its check list is generated from or verified against the registry

  Scenario: ose-private gains the hook-lifecycle doc it lacks
    Given ose-private has no git-hook-lifecycle.md
    When propagation completes
    Then the document exists in ose-private
```

## R-10 — Cross-repo parity preserved

The `apps/rhino-cli` byte-identity boundary spans `ose-public`, `ose-primer`, and `ose-private` with
zero carve-outs. The registry is **data**, not source: gate entry _sets_ may differ per repo (they
follow each repo's actual app and tool set), while the schema and the engine are identical.

```gherkin
Feature: Byte-identity and schema parity

  Scenario: The engine is byte-identical across the three bound repos
    Given the gate engine lands in apps/rhino-cli
    When src/, Cargo.toml, Cargo.lock, project.json and LICENSE are compared
    Then ose-public, ose-primer and ose-private are byte-identical

  Scenario: Registry values may differ per repo but the schema may not
    Given ose-private declares an "iac-lint" gate that ose-public does not
    When "rhino-cli repo-config validate" runs in each repo
    Then each exits zero
    And each gate entry conforms to the same schema

  Scenario: beaver-nest carries the same guarantee through its fork
    Given beaver-nest carries a fork of rhino-cli
    When the fork port completes
    Then "rhino-cli gate validate" exits zero in beaver-nest
```

## Out of Scope

| Excluded                                              | Rationale                                                                                                                         |
| ----------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Emitting per-language CI jobs from the registry       | They need per-language toolchain setup actions; `gate validate` asserts their presence instead                                    |
| Adding `test:integration` / `test:e2e` to any gate    | Ratified rule 3 — uncacheable tiers stay cron-only                                                                                |
| Adding `deps:audit` to a gate surface or the registry | Non-hermetic; excluded by decision — see R-8 and [tech-docs §2.2.3](./tech-docs.md#223-what-is-deliberately-outside-the-registry) |
| Restoring a full-repo sweep                           | Deliberately declined; see [brd.md §Accepted Risk](./brd.md#accepted-risk)                                                        |
| Changing the five controlled scope values             | Ratified vocabulary reused verbatim                                                                                               |
