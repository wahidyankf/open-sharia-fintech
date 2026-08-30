# Add Test Coverage for the Simplified `rhino-bin.sh` Resolver Shim

## Context

`apps/rhino-cli/scripts/rhino-bin.sh` originally resolved the rhino-cli binary through a three-tier
Rust-era mechanism (`RHINO_CLI_BIN` override → prebuilt `target/gate/rhino-cli` → `cargo build
--profile gate` on demand), and `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-binary-resolution.feature`
carried four scenarios exercising exactly that logic. `rewrite-rhino-cli-to-fsharp`'s Phase 9a
retired the whole file when Phase 9c's crate deletion made every one of those scenarios describe a
mechanism that would no longer exist. Phase 9c then simplified the shim to one resolution path:
`RHINO_CLI_FSHARP_BIN` override → `apps/rhino-cli/src/dist/rhino-cli-fsharp` → `dotnet run`
fallback — real, live behavior with **zero scenario-level test coverage**. Phase 9a's own verdict
table flagged this ("may still warrant fresh, F#-only-tier scenarios for 'explicit override takes
precedence' and 'invalid override falls through to discovery'") and Phase 9c explicitly declined to
author it in-plan, recording the decision rather than silently dropping it: "authoring that coverage
belongs to 9c, not to this retire-only sub-phase... net-new test-authoring scope beyond
delete/simplify, not a like-for-like port." That deferred coverage was never picked up by any later
phase — this item is that pickup.

Confirmed during Phase 12 triage: `find specs -iname "gate-binary-resolution.feature"` returns
nothing (correctly deleted), and no current test file drives `rhino-bin.sh`'s three resolution
branches directly — `GateEmissionSteps.fs`, `GateValidationSteps.fs`, and `ParityManifestSteps.fs`
reference the script only as a black-box invocation target, not as the subject under test.

## Scope

**In scope**: `apps/rhino-cli/scripts/rhino-bin.sh`'s three resolution tiers (`RHINO_CLI_FSHARP_BIN`
override → dist binary → `dotnet run` fallback) in both `ose-public` and `ose-private` (the script is
inside the byte-identity boundary, so it is identical in both repos).

**Out of scope**: any change to the shim's actual resolution behavior — this item adds coverage for
existing, shipped behavior, it does not change that behavior.

## Business Rationale (condensed BRD)

**Why**: the binary-resolution shim is the entry point every hook, Nx target, and CI job uses to
invoke rhino-cli. A silent regression here (e.g., the override stops taking precedence, or the
fallback chain breaks) would be caught late — at the point some other tool's invocation fails — not
at the source. This is exactly the class of subject the migration's own `gate-binary-resolution.feature`
existed to guard, and the guard rail was removed without a replacement.

**Affected roles**: any contributor debugging why `rhino-bin.sh` picked (or didn't pick) a given
binary.

**Success metric**: a scenario-level test exists for each of the shim's three tiers and their
precedence order, matching the coverage shape the retired Rust-era feature file had for the
equivalent Rust-side mechanism.

## Product Requirements (condensed PRD)

**User story**: As a contributor relying on `rhino-bin.sh` to invoke the correct rhino-cli binary, I
want its resolution precedence to be tested, so that a regression in override handling or fallback
behavior is caught by CI rather than by a confusing downstream failure.

**Acceptance criteria**:

```gherkin
Feature: rhino-bin.sh resolver shim precedence

  Scenario: An explicit override takes precedence
    Given RHINO_CLI_FSHARP_BIN is set to an existing, executable file
    When rhino-bin.sh is invoked
    Then it executes the file named by RHINO_CLI_FSHARP_BIN
    And it does not fall through to the dist binary or dotnet run

  Scenario: An invalid override falls through to the dist binary
    Given RHINO_CLI_FSHARP_BIN is set to a path that does not exist or is not executable
    And apps/rhino-cli/src/dist/rhino-cli-fsharp exists and is executable
    When rhino-bin.sh is invoked
    Then it executes apps/rhino-cli/src/dist/rhino-cli-fsharp
    And it does not report the invalid override as an error

  Scenario: No override and no dist binary falls through to dotnet run
    Given RHINO_CLI_FSHARP_BIN is unset
    And apps/rhino-cli/src/dist/rhino-cli-fsharp does not exist
    When rhino-bin.sh is invoked
    Then it runs `dotnet run --project apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj`
```

**Product scope**: in — the three scenarios above, as `.feature` text plus TickSpec bindings or a
plain `xunit.v3` test if TickSpec cannot express shell-script invocation cleanly (per this repo's own
established TickSpec-fallback precedent). Out — any coverage of `rhino-bin.sh`'s callers (hooks, CI
jobs), which are already exercised by their own existing tests.

## Technical Approach

Add a new `.feature` file (e.g.
`specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-binary-resolution-fsharp.feature`, naming it
distinctly from the retired Rust-era file since it covers a different mechanism) with the three
scenarios above. Given the subject is a shell script's environment-variable and filesystem-based
branching, a subprocess-driven test (spawn `rhino-bin.sh` with controlled env vars and a temp
directory standing in for the dist path) is the natural test shape — the same pattern
`DispatchUnitTests.fs`'s `runCaptured`/`newTempDir` harness already uses elsewhere in this test
suite. No production code changes; this is purely additive test coverage.

## Worktree

Worktree path: `worktrees/rhino-bin-resolver-shim-coverage/` — to be provisioned at execution start
per [Worktree Specification](../../../.claude/skills/plan-creating-project-plans/reference/worktree-specification.md).
Not yet provisioned; this is a backlog-stage plan.

## Delivery Mode: worktree-to-pr

Mandatory default in `ose-public`; repeated identically in `ose-private` since the script and its
resolution logic are inside the byte-identity boundary.

## Delivery Checklist

Executor legend: `[AI]` = autonomous agent action, `[HUMAN]` = requires human judgment or approval.

### Phase 1: Author and prove (ose-public)

- [ ] [AI] Write the three Gherkin scenarios above into a new `.feature` file under
      `specs/apps/rhino/behavior/rhino-cli/gherkin/gate/`.
- [ ] [AI] Implement step bindings (TickSpec if expressible; otherwise a plain `xunit.v3` test per
      this repo's TickSpec-fallback protocol, recorded as such if invoked).
- [ ] [AI] Prove each scenario fails against a deliberately-broken shim (e.g., swap the precedence
      order) and passes against the real, unmodified `rhino-bin.sh`.
- [ ] [AI] `rhino-cli:specs:behavior:coverage` reports the new scenarios covered.

### Phase 1 Gate

- [ ] [AI] Full `nx affected -t test:quick` clean.
- [ ] [AI] `rhino-cli:test:coverage` unaffected (shell-script coverage is out of scope for the .NET
      line-coverage gate; this only needs the new xunit/TickSpec test itself to pass).

### Phase 2: Repeat in ose-private

- [ ] [AI] Since `rhino-bin.sh` and its resolution logic are inside the byte-identity boundary, copy
      the identical `.feature` file and step bindings (not re-author from scratch — this is a
      byte-identical script, unlike the descriptive-documentation sweeps elsewhere in this repo's
      history, which do differ per repo).
- [ ] [AI] Confirm the parity manifest is unaffected or regenerate it if the new files fall inside
      the tracked boundary.

### Phase 2 Gate

- [ ] [AI] Full `nx affected -t test:quick` clean in `ose-private`.

> **Pause Safety**: the new scenarios are purely additive; safe to stop after Phase 1 and resume
> Phase 2 independently, since nothing in Phase 1 depends on Phase 2 completing.

## Quality Gates

`rtk nx affected -t typecheck,lint,test:quick,specs:behavior:coverage` in both repos.

## Verification

`rhino-cli:specs:behavior:coverage` scenario count increases by exactly 3 (or however many scenarios
the final Gherkin authoring produces) in both repos, and each new scenario demonstrably fails against
a deliberately-broken shim before the fix/coverage is proven correct.
