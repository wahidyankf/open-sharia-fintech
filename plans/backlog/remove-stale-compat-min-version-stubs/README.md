# Remove Stale `compat:min-version` Echo-Only Stubs

## Context

`compat:min-version` is a real, meaningful Nx target for exactly two languages in this repo — Rust
(MSRV floor via `cargo hack check --rust-version`) and F#/C# (SDK-floor equivalent) — per
`repo-governance/development/infra/nx-targets/mandatory-targets-all-projects-six-and-required.md`'s
own Mandatory-Six and Required-Where-Applicable tables. Every other project's copy of this target is
a **no-op echo placeholder** (e.g. `"compat:min-version: no standard min-version floor for
<language>"`), evidently added at some point to satisfy an "every project should declare every
canonical target name" convention rather than because the target does anything.

`rewrite-rhino-cli-to-fsharp`'s Phase 9d discovered this while retiring `rhino-cli`'s own real
`compat:min-version` target: `grep -rl '"compat:min-version"' --include=project.json .` returned 26
other files at that time, every one a no-op echo, and reconfirmed at 27 during this plan's Phase 12
knowledge-capture triage. The governance docs already describe the real convention accurately — the
26-27 stubs are pre-existing debt that predates and is unrelated to the Rust→F# migration, explicitly
flagged in that plan's `learnings.md` as "a separate, unopened cleanup" rather than fixed inline.

## Scope

**In scope**: every `project.json` in `ose-public` whose `compat:min-version` target body is a
no-op echo (not a real `cargo hack`/SDK-floor check). Confirm the exact list via `grep -rl
'"compat:min-version"' --include=project.json .` and manually verify each hit's target body is
genuinely an echo before removing it (do not remove a real check by pattern-matching alone).

**Out of scope**: `ose-private`'s equivalent stubs (a separate, independently-scoped sweep in that
repo, since this plan's own single-sourcing convention does not extend to this unrelated cleanup);
adding `compat:min-version` to any project that lacks it (the mandatory-targets docs already say
this target is "Required-Where-Applicable," not universally mandatory).

## Business Rationale (condensed BRD)

**Why**: a no-op target that exists solely to satisfy a naming convention is worse than no target at
all — it looks like coverage that isn't there, and a future contributor reading `nx run <project>:
compat:min-version` and seeing it "pass" has no signal that nothing was actually checked.

**Affected roles**: any contributor relying on `nx affected -t compat:min-version` output, or
grepping for min-version enforcement across the repo.

**Success metric**: `grep -rl '"compat:min-version"' --include=project.json .` returns only the
projects where the target performs a real check (Rust and F#/C# projects with an actual floor to
enforce), matching the mandatory-targets documentation's own stated scope.

## Product Requirements (condensed PRD)

**User story**: As a contributor auditing which projects enforce a minimum toolchain version, I want
`compat:min-version` to exist only where it does real work, so that grepping for it is a trustworthy
signal.

**Acceptance criteria**:

```gherkin
Feature: compat:min-version exists only where it performs a real check

  Scenario: No-op echo stubs are removed
    Given a project's compat:min-version target body is a no-op echo string
    And that project is not one of the mandatory-targets docs' Rust or F#/C# exceptions
    When the cleanup runs
    Then the compat:min-version target is removed from that project's project.json
    And the project's mandatory-target set otherwise remains unchanged

  Scenario: Real checks are preserved
    Given a project's compat:min-version target performs a real cargo hack or SDK-floor check
    When the cleanup runs
    Then that project's target is left untouched
```

**Product scope**: in — removing genuinely no-op targets. Out — changing what the real targets
check, or adding new min-version enforcement anywhere.

## Technical Approach

1. `grep -rl '"compat:min-version"' --include=project.json .` to enumerate current holders.
2. For each hit, read the target body. If it is a bare `echo "..."` (or equivalent no-op) with no
   real command, mark it for removal. If it invokes a real toolchain-version check, leave it.
3. Remove the target key from each no-op project's `project.json`.
4. Cross-check against `repo-governance/development/infra/nx-targets/mandatory-targets-all-projects-six-and-required.md`'s
   tables — if this sweep finds a project the docs claim SHOULD have a real check but only has an
   echo, flag it as a separate finding rather than silently removing it (that would be a genuine gap,
   not stale debt).
5. Re-run `nx affected -t test:quick` / the full mandatory-target validator to confirm no project
   loses required-target coverage it actually needs.

No new mechanism is introduced — this is a subtractive cleanup only.

## Worktree

Worktree path: `worktrees/remove-stale-compat-min-version-stubs/` — to be provisioned at execution
start per [Worktree Specification](../../../.claude/skills/plan-creating-project-plans/reference/worktree-specification.md).
Not yet provisioned; this is a backlog-stage plan.

## Delivery Mode: worktree-to-pr

Mandatory default in `ose-public` (branch-protected `main`).

## Parallelization Model

Phase 1 is read-only classification and feeds the single change-producing Phase 2 node; no parallel
delivery unit exists.

### Delivery Boundaries

| Phase(s) | Natural cohesive seam                                                                                                                 | Worktree                                           | Branch                                  | Delivery opportunity | Exact resulting `main` / rollback / feature-flag evidence                                                                                                                                                                                                                                                                                                                                                                      |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2        | Remove every confirmed no-op `compat:min-version` target while preserving real checks, project configuration, and validation evidence | `worktrees/remove-stale-compat-min-version-stubs/` | `remove-stale-compat-min-version-stubs` | PR at Phase 2        | The exact resulting `main` state contains only genuine minimum-version checks, retains all applicable mandatory targets, and passes configuration and affected-project gates, so it is immediately production-deployable. A feature flag is not applicable because this subtractive build-metadata cleanup creates no incomplete user-reachable behaviour; rollback is a PR revert. Integrate promptly after the Phase 2 gate. |

The classification, removals, validation, and rollback evidence stay together because splitting them
would leave misleading partial target discovery. LOC and file counts never define this boundary.

## Delivery Checklist

Executor legend: `[AI]` = autonomous agent action, `[HUMAN]` = requires human judgment or approval.

### Phase 1: Enumerate and classify

- [ ] [AI] Run the enumerating grep; produce a per-file verdict (echo-stub vs. real-check) with the
      exact target body quoted for each.
- [ ] [HUMAN] Spot-check the verdict table before any file is edited (a false "echo" classification
      would silently remove real enforcement).

### Phase 2: Remove and verify

- [ ] [AI] Remove the target key from every confirmed echo-stub project's `project.json`.
- [ ] [AI] Confirm `git diff` touches only the target-removal lines, nothing else.
- [ ] [AI] `nx affected -t test:quick` clean across every touched project.
- [ ] [AI] Re-run the enumerating grep; confirm the surviving hit list matches only real-check
      projects.

### Phase 2 Gate

- [ ] [AI] `rtk npm run validate:sync` (or the repo's mandatory-target validator, if a standalone
      one exists) still passes.

> **Pause Safety**: each project's edit is independent and reversible via `git diff`; safe to stop
> after any subset of projects and resume with the remaining ones.

## Quality Gates

`rtk nx affected -t typecheck,lint,test:quick` across every touched project.

## Verification

`grep -rl '"compat:min-version"' --include=project.json .` returns only genuine Rust/F#/C#
min-version-check projects, cross-checked against the mandatory-targets documentation's own stated
scope.
