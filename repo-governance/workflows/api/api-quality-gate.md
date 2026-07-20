---
name: api-quality-gate
title: "api-quality-gate"
goal: Validate a live REST or GraphQL API against its contract and existing Gherkin specs, then fix every defect the tester finds and re-test until the defect set is empty
termination: "Zero outstanding in-threshold AET-### findings on two consecutive re-tests against the current deployed build — the double-zero confirmation (max-iterations defaults to 7, escalation warning at 5)"
inputs:
  - name: scope
    type: string
    description: 'Base URL or endpoint set to exercise, plus the contract to test against (e.g., "http://localhost:8302 with apps/ose-be/openapi.yaml")'
    required: true
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Quality threshold (lax: CRITICAL only, normal: CRITICAL/HIGH, strict: +MEDIUM, ocd: all levels)"
    required: false
    default: strict
  - name: min-iterations
    type: number
    description: Minimum test-fix cycles before allowing zero-finding termination
    required: false
  - name: max-iterations
    type: number
    description: Maximum test-fix cycles to prevent infinite loops
    required: false
    default: 7
  - name: max-concurrency
    type: number
    description: "Background agents run concurrently — the N in the N+1 model (1 main thread + N background agents = N+1 total). Raise only when independent work, machine capacity, and budget headroom all allow; lower under budget, runner, or disk pressure. Never self-promoted beyond the declared value."
    required: false
    default: 3
outputs:
  - name: final-status
    type: enum
    values: [pass, partial, fail]
    description: Final validation status
  - name: iterations-completed
    type: number
    description: Number of test-fix cycles executed
  - name: final-report
    type: file
    pattern: "the destination selected by the tester's output-mode: the plan folder (plan), the plan's delivery.md (delivery), or local-temp/<slug>/findings.md (local-temp)"
    description: Final findings record, written wherever the invoked output-mode directs
---

# API Quality Gate Workflow

**Purpose**: Exercise a **running** REST or GraphQL API against its contract (OpenAPI 3.x spec or
GraphQL SDL) and the repository's existing `specs/**` Gherkin, then fix every defect found and
re-test until none remain.

This gate is the API counterpart of the [UI Quality Gate](../ui/ui-quality-gate.md). The two differ
in kind, not only in surface: the UI gate is a **static** checker/fixer loop over component source,
while this gate is a **tester-driven** loop against a live deployment. Nothing here inspects source
in the abstract — every finding originates in an actual HTTP response.

## Shape: Tester-Driven, Not Checker/Fixer

There is deliberately **no `api-checker` / `api-fixer` agent pair**, and this workflow must never be
read as though there were. The loop is:

1. [`api-exploratory-tester`](../../../.claude/agents/api-exploratory-tester.md) drives the live API
   and emits `AET-###` findings.
2. The appropriate `swe-*-dev` agent — chosen by the implementing language of the service under
   test (`swe-fsharp-dev` for `ose-be` / `organiclever-be`, `swe-typescript-dev`, `swe-rust-dev`,
   and so on) — fixes each finding.
3. The tester re-runs against the rebuilt/redeployed service.

Repeat until the defect set is empty. Naming a non-existent `api-checker` or `api-fixer` agent is
anti-pattern **AP-7** (citing an agent that does not exist).

## Execution Mode

**Preferred Mode**: Agent Delegation — invoke `api-exploratory-tester` and the fixing `swe-*-dev`
agent via the Agent tool with `subagent_type` (see
[Workflow Execution Modes Convention](../meta/execution-modes.md)).

**Fallback Mode**: Manual Orchestration — drive the API directly with `curl` and apply fixes with
Read/Write/Edit when Agent Delegation is unavailable.

**How to Execute**:

```
User: "Run API quality gate for http://localhost:8302 against apps/ose-be/openapi.yaml"
User: "Run API quality gate for the organiclever-be GraphQL endpoint"
```

## Preconditions

- **The service is running and reachable** at the supplied base URL. This gate tests a deployment,
  not a codebase — an unreachable service is a `fail`, never a `pass`.
- **The contract is identified**: an OpenAPI 3.x document or a GraphQL SDL. Without ground truth,
  the tester can only find crashes, not contract violations.
- **Destructive operations are out of scope.** The tester is non-destructive by construction; it
  never issues requests intended to delete or corrupt persistent state.

## Steps

### 1. Test (Agent Delegation)

Invoke `api-exploratory-tester` with the `scope` input and `output-mode: delivery` when running
inside a plan, or `local-temp` for a throwaway pass.

The tester exercises, at minimum: contract conformance (status codes, response shapes, error
envelopes), auth/authz boundaries, pagination, idempotency, boundary and edge-case payloads, and —
for GraphQL — nullability, partial errors, and query depth. It compares observed behaviour against
both the contract and existing `specs/**` Gherkin.

**Output**: `AET-###` findings, written to the destination the selected `output-mode` directs — an
existing plan's `delivery.md` under `delivery`, or `local-temp/<slug>/findings.md` under
`local-temp`. The tester writes nowhere else; in particular it does not emit to `generated-reports/`.

### 2. Triage Against Mode

Filter findings by the `mode` threshold. Findings below the threshold are reported but do not block
termination.

`api-exploratory-tester` rates findings on the **ISTQB severity scale** (Blocker / Critical / Major /
Minor / Trivial), which is not the CRITICAL/HIGH/MEDIUM/LOW vocabulary the `mode` input names. Map
severity to threshold as follows — Priority is a separate axis and never substitutes for severity:

| `mode`   | In-threshold ISTQB severities            | Equivalent named level |
| -------- | ---------------------------------------- | ---------------------- |
| `lax`    | Blocker, Critical                        | CRITICAL only          |
| `normal` | Blocker, Critical, Major                 | CRITICAL + HIGH        |
| `strict` | Blocker, Critical, Major, Minor          | + MEDIUM               |
| `ocd`    | Blocker, Critical, Major, Minor, Trivial | all levels             |

### 3. Fix (Agent Delegation)

Route each in-threshold finding to the `swe-*-dev` agent matching the service's language. Every fix
lands with a **reproducing test** that fails before the fix and passes after, per the
[Regression Test Mandate](../../development/quality/regression-test-mandate.md).

Where the tester proposes Gherkin for behaviour that is correct but unspecified, add those scenarios
to `specs/**` — a missing spec is a real gap, not a false positive.

### 4. Re-Test

Rebuild and redeploy the service, then re-run step 1 against the **current** build. A fix verified
only against source, never against a live response, does not count as verified.

### 5. Double-Zero Confirmation

A single zero-finding pass does not terminate the loop. When step 4 returns zero in-threshold
findings, run **one more** full test pass against the same deployed build:

- Still zero → the double-zero holds; proceed to step 6 with status `pass`.
- Findings appeared → the first zero was a false negative; return to step 3.

This mirrors the [UI Quality Gate](../ui/ui-quality-gate.md) and is mandated by the
[Workflow Identifier Convention](../meta/workflow-identifier.md): a gate
terminates on two consecutive clean validations, never one.

### 6. Iteration Control

Repeat steps 1-5 until the double-zero holds, or `max-iterations` is reached. Warn at
iteration 5 that the loop is approaching its ceiling.

- **`pass`** — zero in-threshold findings on **two consecutive** re-tests against the current build.
- **`partial`** — findings remain but iterations are exhausted.
- **`fail`** — the service could not be reached, or the contract could not be resolved.

## Relationship to Other Gates

This gate is **surface-conditional**: it applies to a plan that ships an API or backend surface. A
UI-bearing plan runs the two UI gates instead; a plan bearing both runs both; a plan bearing neither
**states that exemption explicitly** in its `tech-docs.md` rather than leaving it implicit.

It is also a **merge precondition** — clause (e) of the hardened preconditions in the
[PR Review Quality Gate](../pr/pr-review-quality-gate.md).

## Related Documentation

- [API Workflows Index](./README.md) - This category's index
- [UI Quality Gate](../ui/ui-quality-gate.md) - The static component-source counterpart to this gate
- [Web UX Test Fixing Planning](../web/web-ux-test-fixing-planning.md) - The running-UI tester triad; this gate is its API-side analogue
- [PR Review Quality Gate](../pr/pr-review-quality-gate.md) - Consumes this gate as merge precondition clause (e)
- [Manual Behavioral Verification](../../development/quality/manual-behavioral-verification.md) - Why behaviour is verified against a running surface rather than inferred from source
- [Regression Test Mandate](../../development/quality/regression-test-mandate.md) - Every fix ships with a reproducing test
- [Workflow Naming Convention](../../conventions/structure/workflow-naming.md) - Basename `api-quality-gate` parses as scope=`api`, type=`quality-gate`
