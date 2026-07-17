# Business Requirements — Rhino speccoverage multi-line scenario scan

## Business goal

Eliminate a class of **false-positive spec-coverage failures** caused by the `speccoverage` scanner
reading TypeScript/JavaScript `Scenario(...)` titles one physical line at a time. When a scenario
title is wrapped onto a following line (routinely done by Prettier at `printWidth: 120`), the scanner
misses it and reports a covered scenario as an uncovered gap, blocking CI on a phantom problem.

## Business rationale

The `speccoverage` engine is a **shared quality gate** exercised in all three sibling repos
(`ose-public`, `ose-primer`, `ose-infra`) through the byte-identical `apps/rhino-cli`
[Repo-grounded — `docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary`]. A gate
that fails on legal, auto-formatted code:

- forces contributors to hand-collapse `Scenario(` calls onto one line and guard them with
  `// prettier-ignore` — a manual annotation every author must remember
  [Repo-grounded — hacks present at `libs/web-ui/src/primitives/code-block/code-block.steps.tsx:155,190`
  and `copy-button.steps.tsx:45`];
- couples the correctness of a coverage gate to a code-formatting accident, which is brittle: a
  future Prettier or ESLint change can silently re-introduce the wrap and re-break the gate;
- erodes trust in the gate — a gate that cries wolf on well-formatted code trains contributors to
  bypass or ignore it.

Fixing the scanner removes the root cause once, across all three repos, and lets the existing
`// prettier-ignore` workarounds be deleted.

## Business impact

**Pain points addressed**

- Spurious `specs:behavior:coverage` CI failures on correctly-formatted step files.
- Ongoing maintenance tax of `// prettier-ignore` + hand-collapsed lines that must be preserved by
  every future editor of the affected files.
- Formatting-coupled fragility: the gate's correctness currently depends on line layout.

**Expected benefits**

- Coverage results become independent of where Prettier chooses to wrap a `Scenario(` title
  [Judgment call: this is the direct, intended consequence of scanning whole-content].
- The two existing hacks are removed and no new ones are needed.
- The fix lands byte-identical in all three repos, keeping the shared gate consistent.

## Affected roles

Solo-maintainer repo — no sign-off ceremonies. The maintainer wears these hats:

- **Platform/tooling maintainer** — owns `apps/rhino-cli` and the `speccoverage` engine.
- **Frontend maintainer** — owns `libs/web-ui` step files where the hacks live.
- **Release/parity maintainer** — propagates the byte-identical rhino-cli change to `ose-primer`
  and `ose-infra`.

**Consuming agents**: `plan-execution` (executes this plan), `plan-checker` (gates it), the CI
`specs:behavior:coverage` job (consumes the fixed scanner), and `swe-rust-dev` (implements the
Rust change).

## Business-level success metrics

- **Observable**: after the fix, a step file containing a `Scenario(` whose title is on the next
  physical line passes `nx run rhino-cli:specs:behavior:coverage` with zero reported scenario gaps
  attributable to line wrapping [Repo-grounded — verified by the new fixtures and Gherkin scenario].
- **Observable**: `grep -rn "prettier-ignore" libs/web-ui/src/primitives/code-block/` returns no
  matches after hack removal [Repo-grounded — current matches enumerated above].
- **Observable**: `apps/rhino-cli/src/application/speccoverage/checker.rs` is byte-identical across
  `ose-public`, `ose-primer`, `ose-infra` after propagation (verified by diff).

## Business-scope non-goals

- Not a redesign of the coverage engine or its matching strategy.
- Not a change to how any other language's scenario titles are extracted.
- Not a change to any `libs/web-ui` runtime component behavior.

## Business risks and mitigations

| Risk                                                                      | Likelihood | Mitigation                                                                                                                 |
| ------------------------------------------------------------------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------- |
| Whole-content scan changes extraction results for existing files          | Low        | Regression fixtures assert same-line extraction is preserved; full `rhino-cli` unit + specs suites run in the phase gate.  |
| Byte-identity drift between the three repos after the change              | Medium     | Dedicated parity phase diffs `checker.rs` + behavior tree across repos; propagation is a gated step, not optional.         |
| Removing `// prettier-ignore` reintroduces a real coverage gap            | Low        | Hack removal is verified by re-running `specs:coverage` / `specs:behavior:coverage` green **after** the scanner fix lands. |
| Scenario-count tables in the gherkin README drift after adding a scenario | Low        | Delivery step recounts and updates the affected README table(s) as a byte-identity-boundary concern.                       |

See [`prd.md`](./prd.md) for the testable acceptance scenarios that verify each claim above.
