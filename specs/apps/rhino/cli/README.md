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
- [Behaviors](./behaviors/README.md) — the recursive Gherkin corpus, one directory per command
  namespace.

## Adding a Scenario

1. Put the scenario in `behaviors/<namespace>/<namespace>-<action>.feature`, where `<namespace>` is
   the command's first argv segment.
2. Bind it in `apps/rhino-cli/src/tests/unit/Steps/` for a pure in-process rule, or in
   `apps/rhino-cli/src/tests/integration/Steps/` when the scenario needs a real local resource.
3. Run `nx run rhino-cli:test:quick`, which executes the bound suites and then proves every
   scenario in this corpus is bound.

A scenario with no binding fails `specs:behavior:coverage`; a binding with no scenario fails the
same target from the other direction. Neither can be waived per file or per scenario.

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
