# Rhino CLI — Specification Corpus

Audience: engineers and technical product managers working on
[`apps/rhino-cli`](../../../../apps/rhino-cli/README.md) — the Repository Hygiene & INtegration
Orchestrator.

This corpus is the single source of truth for what `rhino-cli` does. A scenario here defines the
command's accepted arguments, its stdout, and its exit code; the implementation is correct when
every scenario it declares is green.

## Contents

- [Architecture](./architecture.md) — the current as-built system: its context, the one binary it
  ships, the five projects inside it, and the constraints that bind them.
- [Behaviours](./behaviours/README.md) — the recursive Gherkin corpus, one directory per command
  namespace.

## Adding a Scenario

1. Put the scenario in `behaviours/<namespace>/<namespace>-<action>.feature`, where `<namespace>` is
   the command's first argv segment.
2. Bind mandatory in-process proof in `apps/rhino-cli/tests/unit/Steps/`, using injected doubles
   for every OS-facing dependency.
3. Bind every applicable higher layer: `apps/rhino-cli/tests/integration/Steps/` for real
   non-networked local resources and the E2E adapter for the built CLI's public process boundary.
4. Run `nx run rhino-cli:test:quick`, which executes Unit and validates every applicable adapter
   statically without running Integration or E2E.

A scenario with no Unit binding fails `test:coverage:unit`; missing applicable higher-layer
bindings fail their matching static targets; and `test:coverage:behaviour` validates the corpus.
Only a genuine per-scenario Integration/E2E boundary mismatch may use the canonical exemption form
defined by the [BDD standard](../../../../repo-governance/development/behaviour-driven-development.md).

## Exit-Code Contract

Every command uses the same three values, and a scenario asserts one of them:

| Code | Meaning                                                               |
| ---- | --------------------------------------------------------------------- |
| `0`  | the command ran and the thing it checks holds                         |
| `1`  | the command ran and reported a finding                                |
| `2`  | the argv shape was wrong — an unknown flag, or a missing required one |

## Related

- [`apps/rhino-cli/README.md`](../../../../apps/rhino-cli/README.md) — how to build and run the CLI.
- [BDD Spec-to-Test Mapping Convention](../../../../repo-governance/development/infra/bdd-spec-test-mapping.md) —
  the repository-wide rule this corpus follows.
